# F368 — CL303's own falsifier 4, run against the actual Kaloper–Padilla base action: PPN/F178-vacuum/induced-$G$ are not in tension (CL303 stays contingent), but the base mechanism itself — not only its "why now" extension — requires spatial closure and non-eternal dark energy, neither excluded by current data and the latter directionally aligned with DESI DR2

**Date:** 2026-09-05 - 02:15
**Numbering:** **F368**, taken as `NEXT FREE NUMBER` (max was F367, no gaps).
**Status:** **Falsifier 4 checked and NOT met (structural, cited + one algebraic identity, sympy-verified): CL303 stays `contingent`.** Two new, previously-unnamed adoption costs surfaced and independently checked: sequestering's own base action (not merely its "why now" extension) requires a spatially closed (k>0) cosmology and non-eternal ("transient") dark energy. Both are shown here by direct citation of Padilla's 2015 review (arXiv:1502.05296 §7, consulted directly rather than through F367's abridged local-consequence citation) to be base-mechanism requirements. Neither is excluded by current data, and the transience requirement is directionally — not quantitatively — aligned with DESI DR2's own current $w_0>-1,\,w_a<0$ preference. 5/5 checks PASS, 3/3 declared controls verified red-and-only-there.
**Checked:** 2026-09-05 - 02:45 -- 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN -- **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/interactions/cosmology_lambda_sequestering_consistency.py`
**Registry record:** `F368-cc-sequestering-consistency` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, 3 controls verified red-and-only-there)
**Results:** `test-results/F368_cc_sequestering_consistency.json`
**Claim:** updates `docs/claims/CL303-sequestering-selectivity-identity-not-adopted.md` in place (`status: contingent`, unchanged) — falsifier 4 is now marked checked-and-not-met, and two new named costs (spatial closure, transience) are added to the card's body as inherited, undischarged requirements of the (still un-adopted) mechanism.
**Addresses:** rubric row **K9**, ledger **G1** — CL303's own falsifier 4, left explicitly unattempted by F367 §9/§10. Also touches rubric **K10** (dark-energy $w$ vs DESI) via C3, without absorbing or promoting it — see §6.
**Cross-references:** [[F367-cc-sequestering]] (built the identity this falsifier check targets, named falsifier 4, did not attempt it), [[F332-cc-dynamics-two-channels-excluded]] (named the sequestering channel type), [[F178-gravity-full-tensor-adoption]] (the vacuum-scope restriction falsifier 4 names), [[F79-structural-newton-constant]] (the induced-$G$ derivation falsifier 4 names), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] / [[F241-omega-lambda-o1-residual-anthropic]] (the residual this mechanism targets and inherits, untouched here), [[F182-friedmann-pressure-cosmology]] (this model's own flat-FRW cosmology, the working assumption C2's curvature cost sits against). External: Padilla, A., "Lectures on the Cosmological Constant Problem", arXiv:1502.05296 (2015) §7 (the base sequestering action, its local field equation eq.7.10, and its own closure/transience derivations — consulted directly, not re-derived in full); Kaloper, N. & Padilla, A., *Phys. Rev. Lett.* **112**, 091304 (2014); *Phys. Rev. D* **90**, 103523 (2014) (the mechanism, per F367); Planck Collaboration, arXiv:1807.06209 (2018 cosmological parameters); Di Valentino, E., Melchiorri, A. & Silk, J., *Nature Astronomy* **4**, 196 (2020), arXiv:1911.02087 ("Planck evidence for a closed Universe..."); Efstathiou, G. & Gratton, S., arXiv:2002.06892 (2020) (the counter-argument that the CMB-alone curvature preference is a prior-volume artefact, cited to avoid overclaiming C2); DESI Collaboration, arXiv:2503.14738 (2025) (DR2 BAO + CMB/SNe dark-energy constraints).

---

## 1. What F367 left unattempted, precisely

F367 (2026-09-04) built and sympy-verified sequestering's local *consequence* — a spacetime-constant piece of the matter trace cancels exactly under Kaloper–Padilla spacetime averaging — and used it to argue F164's $\rho_\text{vac}$ is exactly the eliminable source class. It explicitly declined to check the mechanism's *base action* against this model's other decision-4 content, naming that check as its own falsifier 4: *"a worked construction showing sequestering's global Lagrange-multiplier sector is inconsistent with the model's other decision-4 content (PPN, the F178 vacuum-scope restriction, the induced-$G$ derivation) would close the adoption question in the negative, converting this card's status from contingent to withdrawn."* This finding runs that check, against Padilla's review §7 directly rather than the abridged form F367 cited.

## 2. C1 — the PPN/vacuum leg: not in tension

Padilla §7's local field equation for the minimal (base) sequestering mechanism is

$$M_\text{Pl}^2\,G_{\mu\nu} = \tau_{\mu\nu} - \tfrac14\,g_{\mu\nu}\langle\tau^\alpha_\alpha\rangle,$$

where $\tau_{\mu\nu}$ is the ordinary matter stress tensor and $\langle\tau\rangle$ is its spacetime average (a single global number, not a function of position). In a vacuum region, $\tau_{\mu\nu}=0$ pointwise, and this equation reduces — checked here algebraically (sympy, `vacuum_reduces_to_gr_plus_lambda_eff`) — to

$$G_{\mu\nu} = -\Lambda_\text{eff}\,g_{\mu\nu}, \qquad \Lambda_\text{eff} := \frac{\langle\tau\rangle}{4M_\text{Pl}^2}.$$

This is *ordinary* GR vacuum plus a cosmological constant — the Kottler/Schwarzschild–de Sitter form — not a new tensor structure, and $\Lambda_\text{eff}$ is a single global constant, the same everywhere in space at any fixed cosmic epoch. It is therefore the *same qualitative object* (a small $\Lambda$ term) this model's own decision 4 already needs to explain — K9's entire subject — so it is not a *new* tension with F178's exact-vacuum $K=\exp(2GM/rc^2)$ construction any more than ordinary $\Lambda$CDM's own $\Lambda$ already is: PPN corrections from a nonzero $\Lambda$ scale as $\Lambda r^2$, utterly negligible at solar-system distances (a standard, textbook GR fact, cited rather than re-derived). The Einstein–Hilbert coefficient ($1/G$) is untouched by construction, exactly as F367 §S1 already established (reused verbatim, not re-derived here): the multiplier sector couples to $\int\sqrt{-g}\,\Lambda$ alone. **Falsifier 4's PPN and induced-$G$ legs are therefore not met** — the check the module runs (`C1-vacuum-reduces-to-ordinary-GR-plus-Lambda_eff`) passes, and passing is the *negative* result for falsifier 4 (no inconsistency found).

## 3. C2 — the spatial-curvature leg (a new cost, not named by F367)

Padilla §7, consulted directly (not merely the abridged eq.7.10 form F367 cited), derives that the sequestering mechanism's own global integral constraint $\langle R\rangle=0$, combined with the Friedmann pair implied by eq.(7.10), forces the cosmology to be spatially closed: *"suitable sequestering solutions do exist, ... constrained to be spatially closed."* This is stated by the review as a feature of the **base** mechanism — the derivation (its own eq.7.23, not reproduced here) does not invoke the additional scalar potential Padilla later adds to address the "why now" coincidence; that potential concerns *when* the universe recollapses, not *whether* $k>0$ is required at all.

This finding does not re-derive Padilla's own multiplier-level eq.(7.23). It independently verifies, by direct sympy integration, the more elementary fact underlying it: KP's own requirement that the total spacetime 4-volume $V_4$ be finite (needed for the global multiplier $\lambda$ to remain well-defined, cited from Padilla §7's own eq.7.5-level construction) is

- **violated** by eternal ($w=-1$-forever) de Sitter expansion: $a(t)=e^{Ht}$ gives $V_4(T)=\int_0^T a(t)^3\,dt=(e^{3HT}-1)/(3H)\to\infty$ as $T\to\infty$ (`eternal_de_sitter_v4_diverges`, exact sympy limit);
- **also violated** by ordinary flat/open matter-only eternal expansion with no $\Lambda$ at all: $a(t)\sim t^{2/3}$ gives $V_4(T)\sim T^3\to\infty$ (`flat_open_matter_only_v4_diverges`) — included as a genuine control, not a cherry-picked comparison, to show that finite $V_4$ is not a generic property of merely-decelerating expansion;
- **satisfied** by the ordinary closed ($k>0$) matter-dominated FRW recollapse — the textbook cycloid solution $a(\eta)=A(1-\cos\eta)$ over one full bang-to-crunch cycle $\eta\in[0,2\pi]$ (cited, e.g. Weinberg or MTW; not re-derived) — whose 4-volume is a manifestly finite integral of a bounded, continuous integrand over a finite domain, $V_4 = \tfrac{35\pi}{4}A^4$ exactly (`closed_recollapse_v4_finite`, sympy).

Of the three histories checked, only the closed recollapsing one gives finite $V_4$ — consistent with, and independently supporting, Padilla's own stronger multiplier-level result that $k>0$ specifically (not just "eventually decelerating") is what the self-consistent solution set requires.

**Is this excluded by data?** Not currently, and the honest answer is more interesting than a flat no. Planck 2018 CMB temperature+polarization data *alone* (TT,TE,EE+lowE) shows a well-known preference for *positive* curvature at (widely reported) more than 99% C.L. (Planck Collaboration 2018, arXiv:1807.06209; the same reading, with the "closed universe" framing and a discussion of its cosmological consequences, is given independently by Di Valentino, Melchiorri & Silk, *Nature Astronomy* **4**, 196 (2020), arXiv:1911.02087). This is a **live, disputed** tension in mainstream cosmology, not a settled result: Efstathiou & Gratton (arXiv:2002.06892, 2020) argue it is a parameter-volume/prior-choice artefact of the CMB-alone analysis rather than physical curvature, and the tension is resolved to consistency with flat once BAO data is added to the fit. This finding takes **no side** in that dispute — it is not resolved here either way — and reports only the narrow, defensible fact: sequestering's own $k>0$ requirement is *not* currently excluded by data, and (not claimed as evidence, only noted as a live and curious alignment) it sits on the same side of flat that CMB-alone's own contested preference does.

## 4. C3 — the transient-dark-energy leg (a new cost, touching K10)

Padilla §7, again consulted directly, also derives that eternal $w=-1$ is *"incompatible with the sequestering proposal"* — for the same reason as C2's divergence: it gives infinite spacetime volume, violating the finite-$V_4$ requirement the multiplier field needs. This is, again, a feature of the base mechanism, not only its "why now" extension.

Compared against current data: DESI DR2 BAO combined with CMB prefers $w_0>-1$, $w_a<0$ over $\Lambda$CDM at $3.1\sigma$ (rising to $2.8$–$4.2\sigma$ depending on the supernova sample added; DESI Collaboration 2025, arXiv:2503.14738). In the CPL parametrisation $w(a)=w_0+w_a(1-a)$, `desi_w_evolution_direction` computes (sympy, exact for the rational inputs used) $dw/da = -w_a$; since $w_a<0$, $dw/da>0$ — **$w$ is increasing (becoming less negative) toward the future** in this fit's own extrapolation. That is the qualitative *direction* a transient, eventually-non-accelerating dark energy needs, and it is *not* the eternal-$w=-1$ direction sequestering's base mechanism forbids.

This is reported as a **qualitative, not quantitative**, alignment, for reasons stated as plainly as F367 stated its own §5 caveat: CPL is a low-redshift phenomenological fit with no claim to describe the asymptotic future of the universe, and sequestering's own recollapse timescale depends on a free parameter (Padilla's linear-potential coefficient, his $m^3$) this model does not fix or constrain. **This is not offered as a derived prediction, and it does not promote or resolve rubric row K10** — K10's own residual (magnitude of $w$'s departure from $-1$, and the model's own vacuous-sign caveat under Amendment 4) is completely untouched; only the *direction* of one candidate mechanism's own requirement is checked against the *direction* of current data, and found not contradicted.

## 5. Falsifier-4 verdict

Falsifier 4, as literally worded by CL303, names three legs: PPN, the F178 vacuum-scope restriction, and the induced-$G$ derivation. §2 checks all three (the induced-$G$ leg via F367's own already-established S1, reused not re-derived) and finds no inconsistency. **Falsifier 4 is therefore NOT met** — CL303's `status` stays `contingent`, and does not convert to `withdrawn`. What this finding adds is not a failure of falsifier 4's own three legs, but two *additional* costs (§3, §4) that F367's narrower identity-only check did not surface, because F367 only used sequestering's local *consequence* rather than consulting the base action's own accompanying requirements.

## 6. What this does and does not do

**Does:** runs CL303's own stated falsifier 4 against the actual KP base action (Padilla §7, direct citation) rather than F367's abridged form; finds the PPN/F178-vacuum/induced-$G$ legs are not in tension (§2, one algebraic sympy check); surfaces two previously-unnamed adoption costs — spatial closure and dark-energy transience — and shows both are base-mechanism features via citation (§3, §4); independently verifies (sympy, not merely cited) the elementary finite-$V_4$ fact underlying the closure requirement, with a genuine control showing divergence is not generic to deceleration (§3); compares both new costs to current, live data (Planck curvature, DESI DR2 $w$) with appropriate hedging about disputed/contested status (§3) and phenomenological/qualitative scope (§4).

**Does not:** adopt sequestering (unchanged from F367); re-derive Padilla's own multiplier-level eq.(7.23) proof that $k>0$ specifically (not just "non-eternal $w$") is forced — that step is cited, not reproduced; resolve the sequestering literature's own free "why now" timescale parameter or derive $\Omega_\Lambda$ (F241's residual is untouched); take a side in the Planck-curvature-tension dispute; or promote, absorb into, or otherwise move rubric row K10 — the DESI alignment in §4 is reported as "not contradicted, directionally aligned," the same epistemic register F367 used for its own $0.036$-dex number, and Amendment 4's explicit instruction that K10 must not yet absorb any of K9's candidate mechanisms stands untouched.

## 7. Falsifiers

1. **A demonstration that Padilla §7's eq.(7.10) vacuum reduction is wrong** — e.g. that $\tau_{\mu\nu}=0$ pointwise does not in fact eliminate the inhomogeneous term, or that $\Lambda_\text{eff}$ is not actually a spacetime constant — would remove §2's basis for saying falsifier 4's PPN leg is unmet. This is a pure algebraic identity (sympy-verified, §2), independently re-checkable by hand in two lines.
2. **A demonstration that PPN corrections from $\Lambda_\text{eff}$ are not, in fact, negligible at solar-system scales for the specific $\Lambda_\text{eff}$ this model's own $\langle\tau\rangle$ would produce** — this finding cites the standard $\Lambda r^2$ scaling generically and does not compute this model's own specific $\langle\tau\rangle$ numerically; a computation showing an anomalously large value would reopen the PPN leg.
3. **A demonstration that Padilla §7's closure/transience derivations are specific to the extended "why now" model after all**, contrary to this finding's reading of the review — would remove §3/§4's basis for calling these base-mechanism costs; the passages cited are quoted in the module's own docstring for direct re-checking.
4. **A recomputed $V_4$ integral (any of the three histories in §3) disagreeing with the closed-form sympy results reported** — checkable independently by hand for the two elementary cases (de Sitter, flat matter power-law) and against any GR textbook for the closed cycloid case.
5. **A resolution of the Planck curvature tension in the "flat, no closed preference" direction** (e.g. a definitive systematic-error identification) would remove even the weak, contested alignment noted in §3 — already flagged as disputed and not relied upon.
6. **A future DESI data release reversing the sign of $w_a$** (favoring $w$ trending toward *more* negative in the future) would remove §4's directional alignment — the check (`C3-desi-preferred-quadrant-trends-toward-less-negative-w`) is explicitly sign-sensitive, demonstrated by the declared `wa_sign_flip` control.

## 8. Honest scope

The strongest claim here is §2's: an elementary, sympy-verified algebraic fact (the vacuum reduction of Padilla's own local field equation) settles that the three legs falsifier 4 names are not in tension with sequestering, closing off — for now — the most direct route to withdrawing CL303. The weakest claims are §3's and §4's numerical/data comparisons, both explicitly and repeatedly flagged as not excluded rather than confirmed, contested rather than settled, and directional rather than quantitative — matching F241's own numerology-caution standard and F367's own epistemic register for its 0.036-dex number. Between those two: this finding adds real, checkable content to the adoption ledger (two named costs neither previously on record) without moving CL303's status, without adopting sequestering, and without touching K10 — a genuine narrowing of the open question, not a closure of it.

## 9. Files

- Module: `src/casim/engine/interactions/cosmology_lambda_sequestering_consistency.py`
- Registry record: `F368-cc-sequestering-consistency` in `tests/registry/interactions.yaml` (tier gate, 3 controls verified red-and-only-there)
- Results: `test-results/F368_cc_sequestering_consistency.json`
- Registered: `src/casim/engine/registry.py` (`interactions.cosmology_lambda_sequestering_consistency`)
- Claim card updated in place: `docs/claims/CL303-sequestering-selectivity-identity-not-adopted.md`

## Reviewed & corrected

**2026-09-05 - 02:45 -- attack pass (inline, 13-point checklist,
`.claude/commands/review-finding.md` protocol -- no cold subagent available against
this device-mounted repo in this session, per review-finding's own inline fallback,
same as F367's precedent):**

1. **Numerical claims re-run independently.** `run()` re-executed with fresh values;
   all 5 checks PASS, matching `test-results/F368_cc_sequestering_consistency.json`
   bit-for-bit. PASS.
2. **All 3 declared controls re-verified red-and-only-there** via
   `casim test --control --id F368-cc-sequestering-consistency`: each control reddens
   exactly its named leg and no other. PASS.
3. **Citation-methodology check on the Padilla §7 quotes.** The passages attributed to
   Padilla's review (the "constrained to be spatially closed" and "incompatible with
   the sequestering proposal" quotes, and the eq.7.10/7.23 structure) were obtained via
   an automated fetch-and-summarize tool reading the arXiv PDF, not by this session
   directly inspecting the primary source page-by-page. **WEAKENS -> flagged, not
   fully fixed**: this is a real methodological weakness distinct from F367's own
   citations (which were of well-known, independently-corroborated literature facts).
   Mitigation applied: two independent fetch queries were run against the same source
   with differently-worded prompts and returned mutually consistent answers on the
   closure/transience-are-base-mechanism-features point (not just the why-now
   extension); falsifier 3 above names this exact risk explicitly rather than leaving
   it implicit. Not fully resolved because this session cannot independently open and
   read the primary PDF page-by-page to triple-check verbatim wording.
4. **Checked the "PPN corrections scale as $\Lambda r^2$, negligible at solar-system
   scale" claim is not overclaimed for THIS model's specific $\langle\tau\rangle$.**
   The finding states this as a generic GR fact (true for a generic small $\Lambda$)
   but does not compute this model's own specific $\langle\tau\rangle$ numerically to
   confirm it is actually small enough. **WEAKENS -> fixed**: added falsifier 2 naming
   this gap explicitly (a model-specific $\langle\tau\rangle$ computation that turned
   out anomalously large would reopen the PPN leg) rather than silently assuming
   genericity carries over.
5. **Checked the closed-recollapse integral's numeric coefficient is not load-bearing.**
   `closed_recollapse_v4_finite`'s reported coefficient ($35\pi/4\,A^4$ at $p=3$) is
   auxiliary output, not asserted against an independently-verified expected value —
   only the boolean `finite` (vs. divergent, as in C2a/C2b) is checked. Confirmed the
   registry record's `expect.exactness` and control reasons never rely on the specific
   coefficient. PASS.
6. **Checked the DESI numeric parameters ($w_0=-0.727$, $w_a=-1.05$) are not presented
   as verified published central values.** The module docstring already calls them
   "illustrative central values ... exact published central values are not
   re-transcribed digit-for-digit here, only the SIGN/quadrant." Confirmed the finding
   prose (§4) also never restates these specific digits, relying only on the
   sign/quadrant claim, which was independently corroborated by two separate fetch
   queries (Nature Astronomy summary + DESI DR2 paper abstract summary) agreeing on
   $w_0>-1,\,w_a<0$. PASS.
7. **Verified the Efstathiou & Gratton citation (arXiv:2002.06892) by direct search**
   rather than from memory alone — confirmed as "The evidence for a spatially flat
   Universe" (2020), matching the counter-argument role cited in §3. PASS.
8. **Checked no existing finding already covers this ground** (searched all files
   under `findings/` for "sequestering", "Kaloper", "Padilla" — only F164, F192, F193,
   F319, F332, F367 appear, none of which attempted falsifier 4). PASS.
9. **Checked for overclaim in the header/status line against §6's honest-scope
   section.** First draft of the module docstring's one-line result read "closes the
   adoption question's PPN leg"; the finding's own Status line was written to match
   §5/§6's actual, narrower conclusion ("falsifier 4 checked and NOT met... CL303 stays
   contingent") from the start of drafting, avoiding the overclaim F367 caught in its
   own review pass 6. PASS (no correction needed at finding-authoring time).
10. **Checked exactness classification.** `exactness: quantitative` on the registry
    record matches F367's own precedent for a mixed-exactness record (C1 is exact by
    algebraic substitution; C2a/C2b/C2c are exact sympy limits/integrals; C3's
    directional check is exact given its inputs, but the inputs themselves are
    illustrative, making the overall record's weakest link quantitative, not exact).
    PASS.
11. **Checked `casim index`, module registry, and test registry all green** after
    every edit: module registry 252/251 covered; `casim test --id` and
    `casim test --control --id` both pass (§ this session's own tool output above).
    PASS.
12. **Checked the claim card update (CL303) matches what was actually found** — status
    stays `contingent` (not promoted, not withdrawn), falsifier 4 marked
    checked-and-not-met, two new costs added — confirmed against §5/§6 before writing
    the card edit. PASS.
13. **Checked the session-claims.yaml topic claim matches what was actually done** (not
    broader or narrower than the falsifier-4 check plus the two surfaced costs). PASS.

**Verdict: CONFIRMED-NARROWER.** Two WEAKENS, one flagged-but-not-fully-fixable within
this session's tool access (item 3, the citation-methodology limitation — mitigated by
cross-checking with a second independent query, and named as falsifier 3), one fixed
(item 4, falsifier 2 added naming the unclosed model-specific $\langle\tau\rangle$
computation). No FAIL. All 3 declared controls re-verified unchanged after review.
