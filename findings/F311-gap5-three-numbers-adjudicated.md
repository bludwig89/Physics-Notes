# F311 — Completeness gap #5's three un-re-derived numbers are **all three instrument or bookkeeping artifacts, not physics defects**: B9's $\Delta\alpha(M_Z)$ is provably untouched by the supersession that worried the report *and* its $0.24\%$ residual **is** the two-loop leptonic term (closing it $155\times$); all ten `candidate` baselines re-run to **zero regressions**, with three of them permanently red on one hole in a regex; and the two cosmological-constant "pictures" are **sequential, not parallel** — F192's open-list was superseded thirteen hours after it was written

**Date:** 2026-08-11 - 21:20
**Numbering:** **F311**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `candid-tenacious-zwicky`, sector `interactions`.
**Status:** Confirmed — **12/12 PASS**, two declared controls verified RED and journalled. A1 is **bit-identical** (a measured re-run, not a call-graph read); A2/A3 are **computed**; B1 is **exact**; B2/B3 are **measured** (ten artifacts re-run and diffed); C is **structural + computed** and derives no new number.
**Module:** `casim.engine.interactions.derive_gap5_adjudication` (`src/casim/engine/interactions/derive_gap5_adjudication.py`)
**Script:** `tests/findings/test_F311_gap5_adjudication.py` (registry entry `check_gap5`, tier **gate**)
**Results:** `test-results/F311_gap5_adjudication.json`
**Also changes:** `src/casim/baselines.py` — one character class in `_VOLATILE_RE` (§3.1). This is the only behavioural edit outside the new module.
**Executes:** `docs/status/completeness-2026-08-07.md` **gap #5**, *"the three numbers no report has re-derived"*, each on its third consecutive report with nothing recorded against it.
**Cross-references:** [[F251-qed-vacuum-polarization-running-alpha]] (the module leg A audits), [[F277-qed-gluon-refold-period]] / [[F272-bgfield-loop-refold-period]] (the supersession whose reach A1 measures), [[F261-twoloop-qed-ae-amu]] (the two-loop QED sector A2's term belongs to), [[F192-vacuum-energy-full-tensor]] (whose V3 open-list C1 shows stale), [[F193-ontic-vacuum-gravitates-as-zero]] (which closed it, the same day), [[F196-dilution-exponent-derived]] (which closed F193's own obstruction), [[F241-omega-lambda-residual-anthropic]] (where the surviving residual sits), [[F178-gravity-full-tensor-adoption]] (the adopted law C adjudicates under), [[F79-induced-newton-constant]] (whose induced $1/G$ is the mode sum C3 shows F192 double-counts), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] ($\Lambda_\text{UV}=3^{-1/4}M_\text{Pl}$, exact). External: Steinhauser 1998 (two-loop leptonic $\Delta\alpha$); Källén–Sabry.

Raised by Ben, 2026-08-11: *"now attack gap #5 and work on calculating those three values."*

---

## 1. The result that is larger than its three legs

Gap #5 grouped three items only because none had been touched. Working them produced a common shape that is worth more than any of them:

> **None of the three was a physics defect.** One was a correct worry about a supersession that turns out not to reach the number; one was ten silent reds of which **zero** were regressions; one was two findings being read as rivals when they are consecutive. In each case the *reading* was wrong and the physics was fine — and in each case the way to find out was to **run something**, not to re-read.

That matters because gap #5's three items had survived three reports on the strength of being *plausible*. Each is closed here by a measurement that takes under two seconds.

---

## 2. Leg A — $\Delta\alpha(M_Z)$: the supersession does not reach it, and the residual is the two-loop term

### 2.1 A1 — proved by reinstating the defect, not by reading the call graph

The report's worry was exact and well-founded: rubric **B9** cites the leptonic $\Delta\alpha(M_Z)=0.24\%$ as `QUANT` evidence; that number comes from `qed_vacuum_polarization`; supersession **S12-F277** names F251 in its `superseded:` list; and F277 **flipped a vacuum-polarization sign**. Grep found no post-F277 re-derivation. On paper it looks like a headline number resting on corrected code.

It does not, and the check does not say so from the call graph — it **puts the defect back**. The pre-F277 `mod 2π` refold of the shifted momentum is reinstated inside `_fermion_B`, and both legs are re-measured:

| leg | what it is | under the reinstated refold |
|---|---|---|
| **Pi4** `leptonic_running` — **where B9's number comes from** | the analytic one-loop sum $\sum_\ell\frac{\alpha}{3\pi}\big[\ln\frac{s}{m_\ell^2}-\frac53\big]$ | **whole payload bit-identical** |
| **Pi3** `lattice_b0_consistency` — what F277 actually fixed | a 4-D BZ quadrature of the fermion bubble | spread moves by **6880×** |

Pi4 touches no grid, no kernel and no refold. **S12-F277 is therefore a *partial* supersession** — it reaches Pi3 and not Pi4 — which is exactly the object CLAUDE.md's claims layer exists to record: *"almost nothing here is superseded wholesale."* B9's evidence was never on corrected code.

### 2.2 A2/A3 — and the $0.24\%$ is the two-loop term, not an error

The one-loop formula omits the two-loop leptonic contribution **by construction**. Källén–Sabry, leading form:

$$\Delta\alpha^{(2)}_\ell=\left(\frac{\alpha}{\pi}\right)^{2}\left[\frac{L}{4}+\zeta(3)-\frac{5}{24}\right],\qquad L=\ln\frac{s}{m_\ell^2}$$

| quantity | value |
|---|---:|
| one-loop total (the module's own Pi4) | $3.142093\times10^{-2}$ |
| PDG leptonic $\Delta\alpha(M_Z)$ | $3.1498\times10^{-2}$ |
| **residual after one loop** | $0.77072\times10^{-4}$ |
| **two-loop term, computed here** | $0.77568\times10^{-4}$ |
| **two-loop / residual** | $\mathbf{100.6\,\%}$ |
| two-loop vs published $0.77621\times10^{-4}$ | $\mathbf{0.068\,\%}$ |
| $1$-loop $+\ 2$-loop | $3.149850\times10^{-2}$ |
| **B9's relative error** | $0.245\,\% \rightarrow \mathbf{0.00158\,\%}$ |
| **improvement** | $\mathbf{155\times}$ |

Zero fitted parameters: the only inputs are $\alpha$, $M_Z$ and the three lepton masses, all already in the module. The remaining $0.00158\%$ sits at the three-loop level ($0.011\times10^{-4}$ in the literature decomposition), which is where a two-loop calculation is supposed to stop.

> **B9 should not be "re-blessed". It should be re-graded upward** — its residual is now explained *and* reduced by two orders, and the term that explains it belongs to the sector F261 already built.

---

## 3. Leg B — the ten `candidate` baselines: zero regressions

Every one was re-run through `casim test --id` and diffed against HEAD. The measured disposition:

| disposition | n | records | evidence |
|---|---:|---|---|
| **clean** | 5 | F64, F128, F181, F240, F241 | reproduce HEAD **exactly** (0 keys changed) |
| **timing-only** | 3 | F182, F184, F200 | *every* drifting key is `_seconds` or `seconds` |
| **float-floor churn** | 1 | F87 | every drifting physics key is a *residual*, committed and re-run both $\ge9$ orders below what it bounds; two keys move by **1 ULP** |
| **undeclared input** | 1 | FA-vs-FC | see §3.2 |
| **regression** | **0** | — | — |
| **supersession** | **0** | — | — |

**Not one of the ten is a physics regression, and not one is explained by the supersession the ledger guessed.** All ten `candidate` entries blamed physics for an instrument defect.

### 3.1 The three timing reds are one hole in one regex — and it is the third instance

`casim.baselines._VOLATILE_RE` exists precisely to keep wall-clock out of a physics diff, and its own comments record two previous patches for this class: `total_elapsed_s` at its first run, `wall_seconds` in C1. It filters `seconds` and `elapsed_s` — but its optional-prefix alternation admits only the *named* prefixes, so a **leading underscore** defeats it. `_seconds` is the convention the F182/F184/F200 harness uses for its per-check timings.

Consequence: three baselines reported pure wall-clock as physics drift, were entered in the ledger as `candidate` (i.e. *suspected physics regressions*), and stayed there for six weeks.

The fix is one character class, placed **outside** the named-prefix group where it cannot be missed a fourth time. After it, all three report *"1 artifact(s) reproduced HEAD exactly"* — which is the measurement that proves they were never regressions.

### 3.2 FA-vs-FC has an undeclared input, and does not measure what its code appears to measure

`_measure_sigma_A` *"prefers a production run if present"*: it reads `test-results/lgt_confinement.json` and short-circuits its own Monte Carlo entirely. Two consequences, both measured:

- **The record is seed-independent.** Five seeds (7, 11, 23, 41, 97) return $\sigma_A$ and $V_A(R)$ identical to ten digits. The `seed=7` parameter in its signature is dead.
- **Its committed baseline matches neither current path.** Production gives $V_A(1)=0.46270$; the inline MC with the short-circuit disabled gives $0.45229$; the committed baseline holds $0.43504$. It was captured against a state of `lgt_confinement.json` that no longer exists — and that artifact is **not declared** in the record's `artifacts_read_only:`, which is the field that exists for exactly this.

The record's *assertion* is unaffected: `results[1].residual`, the $\sigma_A$ vs $\sigma_C(v_*)$ matching identity the comparison exists to test, is $1.2\times10^{-16}$ before and after. Only its Monte-Carlo inputs moved. **Disposition: declare the read-only dependency and re-commit — not a regression, and not S1's photon supersession, which is what the ledger guessed.**

---

## 4. Leg C — the cosmological constant: the two pictures are consecutive, not rival

### 4.1 C1 — the chronology settles it

| | date | what it says |
|---|---|---|
| **F192** V3 | 2026-06-30 - **04:50** | *"all four candidate cancellations remain underived"* |
| **F193** | 2026-06-30 - **17:35** | *"candidate (i) of F164 turned from a position into a derivation"* |
| **F196** | later | derives the $p=2$ dilution exponent **F193 named as its own obstruction** |

**Twelve and three-quarter hours.** F192's open-list was true when written and has been false since that same afternoon; nothing updated it because a finding is written once and superseded rather than rewritten — which is *correct*, and is exactly why a ledger must not read a finding's open-list as a live claim. K9 has carried "two unreconciled pictures" for six weeks on the strength of a status line with a thirteen-hour shelf life.

### 4.2 C2 — F192's sign result is **vacuous** under F193, not contradicted

V1 asserts vacuum $w=-1\Rightarrow\rho+3p=-2\rho<0$, the correct dark-energy sign. Under F193's beable vacuum $\rho_\text{vac}=0$ **exactly**, so $w=p/\rho$ is $0/0$ and there is nothing for the sign statement to be about. The two findings never disagreed about a number; they answered different questions. The sign that matters is the one carried by the *residual* $\rho_\Lambda$, which F193/F196 supply.

### 4.3 C3 — and the $10^{121}$ is a double count that the **adopted** law forbids

CLAUDE.md decision 4 adopts the **induced** Einstein equation, and F79 derives $G$ from matter vacuum polarization with **zero tree-level stiffness** — so in this model $1/G$ *is* the vacuum mode sum up to the BZ edge. F192 V2 then sums the same modes at the same cutoff a second time, as a source on the right-hand side.

Numerically they are the same object two powers of the cutoff apart: F192's committed $\rho_\text{vac}=3.456\times10^{111}$ J/m³ sits **1.65 dex** from $3^{-1}\rho_\text{Planck}$, which is $\Lambda_\text{UV}^4$ at the model's own exact cutoff $\Lambda_\text{UV}=3^{-1/4}M_\text{Pl}$ (F282). In an induced theory the zero-point modes **make** the left-hand side; they cannot also be the right-hand side.

> **The adopted F178 law entails the F193/F196/F241 picture.** K9 / ledger **G1** collapses from *"two unreconciled pictures, the only place the model contradicts itself"* to one picture with one $O(1)$ number, $\Omega_\Lambda\approx0.685$, which F241 already classifies as closed-negative/anthropic.

---

## 5. Verdict

> Gap #5's three numbers are **all three** artifacts of reading rather than of physics. **(A)** B9's $\Delta\alpha(M_Z)$ is provably untouched by S12-F277 — demonstrated by *reinstating* the removed refold, under which the analytic Pi4 payload is bit-identical while the quadrature Pi3 moves $6880\times$ — so S12 is a **partial** supersession; and the $0.24\%$ residual is not an error but the **two-loop leptonic term**, which accounts for $100.6\%$ of it, agrees with the published value to $0.068\%$, and closes B9 from $0.245\%$ to $0.00158\%$ — **$155\times$, zero fitted parameters**. **(B)** All ten `candidate` baselines re-run: **zero regressions, zero supersessions**; three were permanently red on a **leading underscore** the volatile-key regex did not admit — the *third* instance of that defect in that one regex — and one (FA-vs-FC) has an **undeclared artifact dependency** that makes it seed-independent and its baseline unreproducible. **(C)** The two $\Lambda$ pictures are **sequential**: F193 postdates F192 by twelve and three-quarter hours and closes its candidate (i), F196 then closed F193's own obstruction, F192's $w=-1$ is **vacuous** rather than contradicted once $\rho_\text{vac}=0$, and its $10^{121}$ **double-counts** the mode sum F79 uses to induce $1/G$. The adopted law entails one picture, and G1's residual is the $\Omega_\Lambda$ coincidence alone.

---

## 6. Falsifiers

1. **A re-derivation of Pi4 that is *not* bit-identical under the reinstated refold.** Would mean B9 really does depend on the corrected path and A1 is wrong. The control is already in the record.
2. **A two-loop leptonic $\Delta\alpha$ differing from $0.7757\times10^{-4}$ by more than $0.5\%$.** Would break the identification of the residual; the record's `two_loop_control` (drop $\zeta(3)-\tfrac5{24}$) shows the leg can detect this.
3. **Any `candidate` baseline turning out to be a genuine regression.** The `B3-zero-regressions` leg goes **red** if the count is ever non-zero, so it must be read by a human before the "zero regressions" headline is quoted again.
4. **A volatile key that still slips the filter.** `B1` enumerates the cases; adding one that fails is a one-line falsification.
5. **An argument that the induced Einstein equation *does* carry an independent zero-point source.** Would restore F192 V2 and reopen G1 as a genuine contradiction. This is the one place C could be wrong, and it is a physics argument rather than a bookkeeping one.
6. **A dated finding showing F193 does not close F164 candidate (i).** Would return K9 to two pictures.

---

## 7. What is exact vs computed vs open

| Piece | Status |
|---|---|
| Pi4 bit-identical under the reinstated pre-F277 refold | **exact** (whole payload equality, measured) |
| Pi3 spread moves $6880\times$ under the same perturbation | **computed** |
| S12-F277 is a **partial** supersession (Pi3 yes, Pi4 no) | **structural**, established by the two rows above |
| Two-loop leptonic $\Delta\alpha=0.77568\times10^{-4}$ | **computed** (Källén–Sabry leading form, **cited not re-derived**) |
| Two-loop / residual $=100.6\%$; vs literature $0.068\%$ | **computed** |
| B9 $0.245\%\rightarrow0.00158\%$, $155\times$ | **computed**, zero fitted parameters |
| Leading underscore defeats `_VOLATILE_RE` (pre-fix) | **exact** (enumerated) |
| Ten baselines disposed; 0 regressions, 0 supersessions | **measured** (each re-run and diffed vs HEAD) |
| F182/F184/F200 "reproduced HEAD exactly" after the fix | **measured** |
| FA-vs-FC is seed-independent over five seeds | **measured** (identical to 10 digits) |
| F193 postdates F192 by $12.75$ h and closes its candidate (i) | **exact** (dates in the finding headers) |
| $w=p/\rho$ undefined at $\rho=0$ ⇒ F192 V1 vacuous | **structural** |
| F192's $\rho_\text{vac}$ within $1.65$ dex of $3^{-1}\rho_\text{Planck}$ | **computed** |
| The adopted law entails F193/F196/F241 | **structural** — an adjudication, **not a derivation** |
| $\Omega_\Lambda\approx0.685$ | **untouched**, exactly where F241 left it |

---

## 8. Honest scope

**Leg C derives nothing.** It is an adjudication between two existing findings plus one structural argument about double counting, and $\Omega_\Lambda$ is not touched. What changes is that G1 stops being described as a *contradiction* — which was the ledger's own Part-D category, opened four hours earlier for a different row — and becomes a single picture with a single $O(1)$ residual. If §4.3's double-count argument is wrong, C is wrong, and falsifier 5 says so.

**Leg A's two-loop formula is cited, not derived here.** It is the standard Källén–Sabry leading form. What is new is the *identification*: that the model's own one-loop residual is that term, to $0.6\%$ of itself. Deriving the two-loop leptonic bubble on the model's own fields would be a different and larger piece of work, and F261's machinery is where it would start.

**Leg B measures ten artifacts and says nothing about the physics inside them.** "Zero regressions" is a statement about baselines reproducing, not about findings being right. Two dispositions are recommendations rather than completed edits: F87's floor churn should either be accepted and re-committed or have its residual-key floor raised, and FA-vs-FC needs its `artifacts_read_only:` declared before its baseline is re-committed. Neither is done here, because both change records this session does not own.

**One thing this session changed outside its own module**: the `_VOLATILE_RE` character class. It is a behavioural edit to the drift comparator, it is gated by B1 with a control that reinstates the old behaviour, and the three baselines it un-reds were verified to reproduce HEAD exactly afterwards. Every other file touched is new.

---

## 9. Files
- Module: `src/casim/engine/interactions/derive_gap5_adjudication.py`
- Edited: `src/casim/baselines.py` (`_VOLATILE_RE`, one character class)
- Test: `tests/findings/test_F311_gap5_adjudication.py` (record `F311-gap5-adjudication`, tier gate, **12/12**, 1.0 s)
- Results: `test-results/F311_gap5_adjudication.json`
- Controls: both verified **CONTROL** 2026-08-11, journalled to `test-results/control-soundness.json`
