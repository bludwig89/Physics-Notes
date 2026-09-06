# F373 — G6 nuclear binding: the OBE quark-size regulator b=0.55 fm is not independently tuned — it matches the model's own gauge-derived confinement radius R_conf=1.11/√σ=0.52 fm to 5.5%, and the deuteron is insensitive to the swap

**Date:** 2026-09-05 - 15:10
**Status:** Confirmed (Tier-B, quantitative) — 11/11 checks PASS (revised after review-finding attack pass, see `**Checked:**` below; original script passed 8/8 but had a latent root-finding bug fixed in the same pass, see §9). This is a consistency/insensitivity check, not an algebraic elimination of a parameter: b remains a length that must be supplied to the OBE solver, but it is no longer independently tuned to nuclear data alone — a completely different sector of the model (pure SU(3) gauge dynamics, zero nuclear-force input) predicts a value 5.5% away, and the deuteron's physical observables (r_d, the still-bracketed ω coupling) barely move when b is set from that prediction instead of from the nuclear fit.
**Module:** `src/casim/engine/particles/nuclear.py` (unchanged — read-only reuse of `solve_deuteron`), `src/casim/engine/particles/baryon_dynamics.py` (unchanged — read-only reuse of `spectrum_and_ground_vector`/`PAIR_W`/`_overlap`)
**Tests:** `tests/findings/test_F373_quark_size_from_confinement_radius.py`
**Results:** `test-results/F373_quark_size_from_confinement_radius.json`
**Test record:** record `F373-quark-size-from-confinement-radius` (tier battery, kind `result_dump`) — the script above, baseline `test-results/F373_quark_size_from_confinement_radius.json`. Declared 2026-09-05.
**Checked:** 2026-09-05 — 11 PASS / 0 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER** (attack pass found and fixed a real root-finding defect in the test script itself, not in the underlying physics; the fix strengthened rather than weakened the result — see §9).
**Claim:** none — refinement (this narrows an existing Tier-B parameter count, G6; it does not assert a new algebraic/physics-tested result against QM/SM/GR/SR/QFT in the D12 sense, so no `docs/claims/` card is written).
**Cross-references:** [[F113-nn-short-range-repulsive-core]] / [[F126-nn-intermediate-range-sigma-attraction]] / [[F128-nn-short-range-omega-repulsion]] / [[F240-omega-coupling-from-vector-sector]] (the four findings that fixed b=0.55 fm to the deuteron — the parameter this finding checks), [[F104-p4-deuteron-tensor-bound-nucleus]] (the coupled-channel deuteron solver reused unmodified), [[F146-emergent-su3-string-tension-into-bag]] (the source of R_conf — the entire result of this finding rests on F146 §4a/4b), [[F122-p2-dynamical-baryon-three-body]] (the P2 three-body ECG solver reused for the companion candidate), [[F372-npsplit-theory-uncertainty]] (the most recent finding to reuse the same √σ=0.42 GeV anchor for a different purpose), [[F123-p6-si-scale-matter-sector]] (names the σ↔f_π unification as open strong-sector debt — the reason this finding stays Tier-B rather than promoting to Tier-1)

---

## 1. The question (session brief, rubric row G6)

G6 (nuclear binding) is QUANT: the deuteron binds at $E_b=2.224$ MeV (0.026% from the measured 2.22457 MeV) and $r_d$ to 0.4%, on a fully derived one-boson-exchange (OBE) potential — pion tensor (F104), quark-Pauli short-range core (F113), scalar-isoscalar σ attraction (F126), isoscalar-vector ω repulsion (F128/F240) — with **no tuned hard core**. The one number still independently fixed to reproduce the deuteron is the constituent quark size $b=0.55$ fm. The brief asks: what does $b$ physically represent, and does an already-derived model scale supply it?

## 2. What $b$ physically represents

$b$ is the width of the single-quark Gaussian density used throughout the OBE construction — the standard "quark-cluster model" size parameter (Oka–Yazaki / RGM literature range 0.5–0.6 fm, quoted verbatim in F113). It enters in three places, all sharing the *same* $b$ (F126: "one physical length throughout"):

1. **F113's core profile.** The quark-overlap suppression $s=e^{-R^2/8b^2}$ that interpolates the colour-magnetic core from $+341.8$ MeV at $R=0$ to zero at large separation, and the closed-form `derived_core_potential(r,b)` used by `solve_deuteron(core="derived")`.
2. **F104/F113's vertex form factor.** $[1-e^{-(r/b)^2}]^2$, which smears the OPEP $1/x$ and $1/x^3$ short-range singularities so the grid needs no hard wall.
3. **F126/F128's folded Yukawa.** The σ and ω vertices are each convolved with two Gaussian quark densities of width $b$ (`folded_yukawa`), giving a scalar/vector Yukawa finite at $r=0$.

So $b$ is, physically, **the RMS spatial size of a single confined constituent quark inside a colour-singlet baryon** — not a nuclear-force-specific number at all. That framing is the whole of this finding: a quantity with that description should be computable from the model's *confinement* sector, independent of the nuclear-force fit that currently supplies it.

## 3. The candidate: F146's gauge-derived confinement radius

F146 measured the model's own 3D SU(3) gauge dynamics (Metropolis on the model's `su3_exp` link representation — **zero nuclear-force input, zero σ/ω/core content**) and carried the measured string tension through the F131 block-spin binding solver to get a **scale-invariant, parameter-free** single-constituent confinement radius:

$$R_\text{conf}\sqrt\sigma = 1.11 \quad\text{(F146 §4a, converged to \(\approx\)3\% across a 1.67× resolution change)}.$$

This is explicitly framed in F146 as "a single-constituent confinement radius" and compared to the proton charge radius as "the right order" — i.e. F146 already asked and answered exactly the question this finding needs: how big is one confined quark, in this model? Converting with the same $\sqrt\sigma=0.42$ GeV anchor the nuclear sector's own P6 debt already shares (F123 §5; reused verbatim by F372 for a different purpose):

$$R_\text{conf} = \frac{1.11}{\sqrt\sigma} = \frac{1.11\times197.32698\ \text{MeV·fm}}{420\ \text{MeV}} = 0.5215\ \text{fm}.$$

**Check A1:** $|0.55-0.5215|/0.5215 = 5.46\%$ — R_conf lands within 10% of the independently-tuned $b$, using **no nuclear-force input whatsoever**.

## 4. A weaker companion candidate, checked and ruled inferior

Before concluding that R_conf is the right answer, a second model-native candidate was checked so the agreement above is not "any model number is close": the P2 three-body ECG solver (F122/`baryon_dynamics.py`) already computes the ground-state quark–quark pair separation $\langle r_p\rangle$ at its own roadmap-literal baseline point ($m_q=0.785$, $\sigma=1$, $\alpha_s=0.5$ — the same point F372 reuses). For three equal masses in a totally symmetric spatial state (verified S₃-exact here, check B0, residual $4\times10^{-11}$), the standard identity $\sum_{i<j}r_{ij}^2=3\sum_i\rho_i^2$ gives the single-quark RMS spread about the baryon centre of mass, $\langle\rho^2\rangle=\langle r_p^2\rangle/3$. Converting with the same anchor:

$$b_\text{P2-ECG} = \sqrt{\langle r_p^2\rangle/3}\times\frac{\hbar c}{\sqrt\sigma} = 0.4111\ \text{fm}.$$

**Check B1 (informational):** $|0.55-0.4111|/0.4111=33.8\%$ — markedly worse than R_conf's 5.5% (check B2 confirms R_conf is the closer candidate). Two things are worth recording honestly about this number rather than discarding it silently: (i) it is close to F113's *own, pre-σ/ω* fine-tuned value $b\approx0.408$ fm (the core-only fit, before σ and ω were added) — an internal cross-check that the P2 solver's baseline point is at least self-consistent with the *earlier* stage of this same construction, even though it undershoots the *final* physical value; (ii) F122 §5 already flags this exact baseline point as NR/$V_0$-free and known to overshoot the constituent mass scale (its own $m_p/\sqrt\sigma$ comparison), so a 34% miss on a *length* derived from the same uncorrected solve is not a surprise. R_conf, by contrast, comes from a fully independent construction (gauge dynamics, not a quark-model Hamiltonian ansatz) and does not carry that particular caveat — though it carries its own, §6 below.

## 5. Physics-tested check: does R_conf actually work in the deuteron?

Comparing two numbers is not enough. This finding re-solves the **full** derived-OBE deuteron (`solve_deuteron(core="derived", ...)`, F104 π tensor + F113 core + F126 σ + F128/F240 ω) with $b=R_\text{conf}=0.5215$ fm substituted for the tuned $0.55$ fm, holding every *other* model-derived quantity fixed exactly as F240 does ($g_\text{cm}=18.31$ MeV, bare $g_{\sigma NN}^2/4\pi=8.18$, $m_\sigma=622$ MeV, $m_\omega=782.7$ MeV) and re-bisecting **only** the still-bracketed ω coupling to the physical $E_b=2.224$ MeV — the one number F240 itself left as a Tier-B bracket $[5.4,11.1]$, not this finding's target.

| quantity | $b=0.55$ fm (tuned, F240) | $b=R_\text{conf}=0.5215$ fm (this finding) | shift |
|---|---|---|---|
| **Route A** (F113 core + bare σ + ω) | | | |
| $g_{\omega NN}^2/4\pi$ | 5.39 | 6.38 | +18.4% |
| $r_d$ | 1.978 fm | 1.966 fm | **0.62%** |
| $P_D$ | 6.3% | 6.5% | — |
| **Route B** (pure σ+ω OBE, no core) | | | |
| $g_{\omega NN}^2/4\pi$ | 11.15 | 11.33 | +1.6% |
| $r_d$ | 1.881 fm | 1.875 fm | **0.32%** |
| $P_D$ | 7.1% | 7.3% | — |

(Both routes bind $E_b=2.224$ MeV exactly by construction of the ω-coupling bisection, as in F240 — that is not a new result here.)

**Checks C1–C4:** at $b=R_\text{conf}$, route A's $r_d$ is still within 5% of the physical 1.97 fm (residual 0.22%, check C1), the required $g_{\omega NN}^2/4\pi=6.38$ stays comfortably inside the empirical OBE/SU(6) window (check C2), route B's $r_d$ stays within 8% of physical (residual 4.8%, check C3), and — the headline number — **$r_d$ moves by under 1% between the independently-tuned $b$ and the gauge-derived $R_\text{conf}$** (max shift across both routes 0.62%, check C4). The ω coupling shifts more (up to 18% in route A) but stays inside the bracket F240 already declared open; nothing here pins that bracket further. **Check C0** confirms the root search behind C1–C4 actually bracketed a genuine sign change at both $b$ values compared (not a stale/garbage bisection — see §9 for why this check exists at all).

**Check D (stress test, not gated).** The weaker P2-ECG candidate ($b=0.411$ fm) is tested under **both** routes. Route B still binds a physically reasonable deuteron ($r_d=1.86$ fm, $P_D=7.9\%$, 5.3% off physical $r_d$). Route A — re-solved here with a bracket-validated root finder after the review-finding pass caught the original script silently mis-solving this exact point (§9) — also binds well: $g_{\omega NN}^2/4\pi=9.56$, $r_d=1.929$ fm, only **2.1% off** the physical 1.97 fm (check D1). So the model is not simply insensitive to *any* $b$ (R_conf is still the specifically better match, per B2), but it is also **not fragile** at the P2-ECG candidate value the way the unfixed script's silent bug made it briefly appear to be. Check D3 additionally locates route A's genuine physical edge — the $b$ beyond which no positive $g_{\omega NN}^2/4\pi$ solves the deuteron at all — at $b\approx0.6755$ fm, and confirms every $b$ this finding actually compares ($0.41$, $0.52$, $0.55$ fm) sits comfortably ($\ge$15% margin) below it; see §9 for what this boundary is and why it was invisible before the review pass.

## 6. Honest scope — why this stays Tier-B, not a closed derivation

- **R_conf's own measurement carries a known caveat.** F146's σ measurement runs on a 3D simple-cubic SU(3) action that F265 (2026-07-30, extended in the S21 supersession record) showed is blind to $\approx1/3$ of the curvature-carrying link content relative to the model's genuine BCC lattice. `docs/theory/supersessions.yaml`'s own running commentary lists "F94 4D cubic, **F146 3D cubic**... to be rebuilt on the BCC lattice" among the re-scoped (not invalidated, not yet re-derived) results. So $R_\text{conf}=0.52$ fm is a real, zero-nuclear-input model prediction, but one that could itself shift by an $O(1/3)$-curvature-sized amount once measured on the true BCC action — which would move the 5.5% agreement with $b$ in either direction. This finding does not attempt that re-measurement (out of scope; it is F146's own open item, not G6's).
- **The ω coupling is still a bracket, not a pin.** Nothing here derives $g_{\omega NN}$ itself (F240's own open item); this finding only shows that its *value*, whatever it needs to be, stays inside the same physical window when $b$ is set from R_conf instead of tuned.
- **No claim of exact identity.** $b$ and $R_\text{conf}$ are constructed from genuinely different pictures — a phenomenological Gaussian quark-cluster ansatz (F113/F126) versus a single relativistic Dirac constituent in an idealised confining well sourced by measured gauge-sector σ (F146) — so a residual 5–6% gap is exactly what a "same physical quantity, two different model routes" comparison should honestly show, not evidence of an exact algebraic tie. Per CLAUDE.md's practice of attempting algebraic derivation before accepting a number: no closed-form route from $R_\text{conf}$ to $b$ was found or attempted here beyond direct substitution, because the two constructions are not related by an identity — they are independent calculations of the same physical scale.
- **Numerology / look-elsewhere (added by the review-finding pass, §9).** $R_\text{conf}$'s building block $\hbar c/\sqrt\sigma=0.470$ fm is itself a generic hadronic length in this model — the same $\sqrt\sigma=0.42$ GeV anchor that sets confinement scales everywhere else in the tree — so this is not "any O(1) coefficient times a QCD scale matches": landing within 10% of the tuned $b=0.55$ fm requires F146's dimensionless coefficient to sit in $[1.054,1.288]$, a $\approx23\%$-wide window out of an $O(1)$ range. F146's coefficient $1.11$ was fixed by the SU(3) lattice Monte Carlo *before* this comparison was ever run (F146 predates this finding by several sessions), so it was not tuned to land there. Separately, the independent literature value for this same quark-cluster-model regulator (Oka–Yazaki / RGM quark models, already quoted in F113 as 0.5–0.6 fm) brackets both $b$ and $R_\text{conf}$ — consistent with, not proof against, "this is a generic scale that several approaches to the same physics converge on."
- **Route A has a genuine physical edge, found by the review pass (§9).** Route A (core+σ+ω) only has a solution at *positive* $g_{\omega NN}^2/4\pi$ for $b\lesssim0.6755$ fm (check D3); beyond that the coupling required to bind the deuteron goes negative, i.e. unphysical, and route A cannot bind at all via a real ω coupling. Every $b$ actually compared here ($b_\text{P2}=0.41$, $R_\text{conf}=0.52$, $b_\text{tuned}=0.55$ fm) sits $\ge$15% below that edge, so none of this finding's own comparisons are near it — but a future correction to $R_\text{conf}$ (e.g. from the BCC re-derivation the point above already flags as owed) that pushed it substantially higher could approach this boundary, and the boundary itself was invisible before the review pass because of the defect described in §9.
- **What is and is not claimed.** Claimed: $b$ is no longer *only* a number independently fit to reproduce the deuteron — a completely different sector of the model predicts a compatible value with zero nuclear-force content, and the deuteron's physical observables barely move under the swap. Not claimed: $b$ is eliminated as a parameter, or derived to algebraic/machine exactness. G6 should be read as "1 parameter, cross-checked to 5.5% by an independent sector of the model — not a free nuclear-only fit," not as "0 parameters."

## 7. Checks

| # | Check | Tier | Residual |
|---|---|---|---|
| A1 | R_conf (F146) within 10% of tuned $b=0.55$ fm | quantitative | 5.46% |
| B0 | P2 ground state S₃-symmetric (companion candidate sanity) | machine | $4.1\times10^{-11}$ |
| B1 | P2-ECG candidate vs tuned $b$ (informational, not gated) | quantitative | 33.8% |
| B2 | R_conf is the closer of the two candidates | quantitative | — (confirmed) |
| C0 | Route-A/B root search actually bracketed a real root at both $b$=tuned, $b=R_\text{conf}$ (integrity, added §9) | integrity | 0 (confirmed) |
| C1 | Route A $r_d$ within 5% of 1.97 fm at $b=R_\text{conf}$ | Tier-B | 0.22% |
| C2 | Route A required $g_{\omega NN}^2/4\pi$ in OBE/SU(6) window [3,12] | Tier-B | — (6.38, confirmed) |
| C3 | Route B $r_d$ within 8% of 1.97 fm at $b=R_\text{conf}$ | Tier-B | 4.8% |
| C4 | $r_d$ shifts $<10\%$ between tuned $b$ and $R_\text{conf}$ (insensitivity) | Tier-B | 0.62% |
| D1 | Route A finds a real, bracket-valid root at $b_\text{P2}$ (added §9 — the exact point the unfixed script silently broke on) | integrity | 0 (confirmed) |
| D3 | Every compared $b$ sits $\ge$15% below route A's physical crossover $b\approx0.6755$ fm (added §9) | integrity | 18.6% margin |

11/11 PASS. All arithmetic real (real-space Schrödinger + real Yukawa folds + real ECG matrix elements); no chiral/complex transforms, so the CLAUDE.md numpy caveat does not bite.

## 8. What this adds to the model

1. **G6's one tuned parameter is now cross-checked, not free.** $b=0.55$ fm is consistent, to 5.5% and with no new free parameter, with F146's independently-derived single-constituent confinement radius — a genuine cross-sector prediction (pure SU(3) gauge dynamics) landing in the right window for a completely different construction (the OBE quark-cluster folding).
2. **The deuteron's physical observables are demonstrably insensitive to the residual 5.5% gap.** $r_d$ moves by under 1% when $b$ is swapped for the gauge-derived value; only the still-bracketed $\omega$ coupling absorbs the difference, and it stays inside its already-declared physical window.
3. **A documented, ruled-out alternative.** The P2 three-body solver's own single-quark spread is a natural second candidate and was checked; it is a worse match (34%) and is recorded rather than silently discarded, together with the honest note that it reproduces F113's *original* pre-σ/ω fit almost exactly — a separate, smaller internal consistency this finding surfaces as a byproduct.
4. **What remains genuinely open.** A closed-form algebraic tie between $b$ and $R_\text{conf}$ was not found (and is not obviously expected, given the different constructions); $R_\text{conf}$'s own gauge measurement needs the BCC re-derivation F265/S21 already called for; the $\omega$ coupling stays a Tier-B bracket; and route A's own physical range (positive $g_{\omega NN}^2/4\pi$ only for $b\lesssim0.6755$ fm, §6/§9) is now documented but not derived from anything — it is simply where the current OBE construction's arithmetic happens to stop admitting a physical solution. None of these is attacked here — they are separate, already-named debts (F146's own open item; F240's own open item; the route-A boundary is new debt this finding's own review pass surfaced).

## 9. Review-finding pass (2026-09-05) — a real defect, found and fixed

The mandatory attack-and-fix pass (13-attack adversarial review, cold subagent + independent verification) found one genuine defect, in the **test script**, not in the underlying physics or in F146/F240's results:

**The defect.** The original `bisect_bind()` helper bisected a hard-coded bracket (route A: $g_{\omega NN}^2/4\pi\in[2,9]$) without ever checking that the endpoints actually bracketed a sign change. Outside that bracket's true root window it silently returned a garbage midpoint with no error or warning. Verified independently (two scratch scripts, not just re-stating the subagent's claim): at $b=b_\text{P2}=0.4111$ fm — the finding's own companion-candidate value from §4 — route A's true root sits at $g_{\omega NN}^2/4\pi\approx9.56$, just outside the old $[2,9]$ bracket, so the old script returned $E_b=14.03$ MeV, $r_d=0.94$ fm: nonsense, reported as if it were a real result. Because §5's original "Check D" only ever ran route B at $b_\text{P2}$, this failure was never surfaced or reported as a defect — it was invisible by omission, not by design.

**Independent verification (attack 7, perturbation).** Before touching anything, the claim was reproduced directly: a coarse sign-change scan across $b\in[0.30,0.80]$ fm at the old $[2,9]$ route-A bracket confirmed `bracket_ok=False` and the exact garbage numbers above outside a narrow working window $b\in[0.43,0.62]$ fm; a wider unconstrained scan ($g_{\omega NN}^2/4\pi\in[-5,30]$) then located the true roots the narrow bracket was missing, at every tested $b$.

**The fix.** `find_root_gomega()` replaces `bisect_bind()`: it scans coarsely for an actual sign change first and returns `(None, False)` — not a number — when none exists in the scanned range, so a caller cannot mistake "no physical solution found" for a real root. Every route call in the script now goes through this function and every downstream check (C1–C4, the new D1) is gated on a new integrity check (C0) that the root search actually found a real bracket. Two integer/dead-code items the subagent also flagged (`M_RHO` mislabelled as the ρ mass while numerically equal to `M_OMEGA_DEFAULT`, and an unused universal-coupling calculation built from it) were removed — they were computed but never fed into any check or the JSON output, so their removal changes nothing about the results, only the script's honesty about what it uses.

**What the fix changed about the finding's substance — nothing for the worse.** Re-running with the fix does **not** weaken the headline result: A1–C4 are numerically identical to the original run (the old bracket happened to be valid at both $b$ values the headline comparison uses, $b_\text{tuned}=0.55$ and $R_\text{conf}=0.5215$ fm — check C0 now confirms this explicitly instead of assuming it). What the fix adds is new information that was previously hidden: route A also binds well at $b_\text{P2}=0.4111$ fm (check D1, $r_d$ only 2.1% off physical — the model is more robust there than the buggy script's silent failure made it briefly look), and route A has a genuine physical edge near $b\approx0.6755$ fm beyond which no positive ω coupling can bind the deuteron at all (check D3) — a real, if distant, boundary of the current OBE construction that is now documented (§6) rather than invisible.

**Other attacks.** Attack 5 (numerology/look-elsewhere) produced the quantified caveat now in §6 (the $[1.054,1.288]$ coefficient window and the independent Oka–Yazaki literature range). Attacks 1–4, 6, 8–13 found nothing requiring a change: the test record already existed with a real `kind`/`expect.exactness` (attack 8), no superseded finding is cited without its supersession (attack 9, F265/S21 was already carried), and the finding already stated the narrowest supported claim (attack 10) before this pass.

## Exactness-inventory additions

Tier-B (quantitative): A1 (R_conf vs tuned $b$, 5.5%), C1–C4 (full derived-OBE deuteron re-solved at $b=R_\text{conf}$, insensitivity of $r_d$ to $<1\%$) — 5 entries. Machine: B0 (S₃ symmetry of the companion candidate's ground state) — 1 entry. Integrity (added by the review-finding pass, 2026-09-05): C0, D1, D3 (root-search bracket validity and route A's documented physical range) — 3 entries.

## Reviewed & corrected

**2026-09-05 - 15:45** — attack pass: **CONFIRMED-NARROWER**. Found: the test script's `bisect_bind()` silently returned a garbage root outside its hard-coded bracket (never surfaced because §5's original stress test only ran route B at the one $b$ value, $b_\text{P2}=0.4111$ fm, where route A's old bracket happened to fail). Fixed: replaced with an adaptive, bracket-validated root finder (`find_root_gomega`); added 3 new integrity checks (C0, D1, D3); removed unused/mislabelled dead code (`M_RHO`, two derived-but-unused couplings); added a quantified numerology caveat (§6) and documented route A's genuine physical edge at $b\approx0.6755$ fm (§6, §9). Rejected: none. Deferred: route A's physical-edge boundary itself is new, undissolved debt — noted in §8 point 4, no finding number claimed for it (it is a boundary of the current construction, not a new physics result).
