# Findings supersession triage — header pass over all 282 active findings

**Date:** 2026-08-04 - 09:00
**Session:** `exciting-trusting-lovelace` (claim board: `docs/design/session-claims.yaml`)
**Scope:** Stage 0 (reconcile `docs/theory/supersessions.yaml` against the finding files) + Stage 1 (header-only triage of every active finding). **No finding file was moved. No physics was changed. No banner was applied** — see §5 for why the intended banner fix turned out to be the wrong action.
**Disposal bar in force:** *nothing live survives* — the enforced `deprecated/README.md` rule. A finding whose headline claim is dead but which retains live algebra stays active with a banner.

---

## 1. Headline

**Zero findings qualify for retirement on the header evidence.** The candidate queue this pass was meant to produce is empty, and that is a substantive result rather than a failure of the pass.

Three things came out of it that matter more than the empty queue:

1. **Header status lines carry no supersession signal at all.** Every one of the 16 findings the ledger explicitly names as superseded still reads `**Status:** Confirmed — N/N tests PASS`. Nothing in a header distinguishes a live finding from a superseded one.
2. **`findings/` has no banner enforcement whatsoever.** Both `tools/apply_supersession_banners.py` and its gate test iterate `record["tests"]` only, and walk `tests/` and `src/` only. Every banner in a finding file is hand-written, unverified, and can go missing or drift silently. This is the real Stage 0 gap, and it is larger than "some banners are missing."
3. **The premise that motivated this pass does not hold.** Dielectric-gravity findings are *not* wholesale superseded by the full-tensor adoption — the ledger retains the dielectric as the canonical vacuum/weak-field representation, which `CLAUDE.md` Decision 4 also states. Details in §4.

---

## 2. What was measured

| Quantity | Count |
|---|---|
| Active finding files in `findings/` | 282 |
| Distinct labels (11 are letter-suffixed `b`-variants) | 282 |
| Ledger records in `supersessions.yaml` | 17 |
| Findings named in a `superseded:` / `reclassified:` list | 23 |
| …of those, already retired to `deprecated/findings/` | 4 (F16–F19) |
| …of those, active **and** carrying a banner | 4 (F106, F114, F173, F174) |
| …of those, active with **no banner** | 16 |
| Findings carrying a banner with no ledger entry | 4 (F20, F22, F64, F176b) |
| Findings with zero citations from other findings **and** zero code/test references | **1** (F32, `Confirmed — 4/4 tests PASS`) |

Reference counts come from a sweep of `src/`, `tests/` and `scenarios/` for `F<N>` tokens, and of every finding body for `[[F<N>-…]]` wiki-links.

---

## 3. Why header-only triage cannot dispose

### 3.1 The status line is silent

The 16 ledger-named unbannered findings, with what their own header claims:

| Finding | Ledger record | Header `Status:` says | Findings citing it | Code/test refs |
|---|---|---|---|---|
| F50 | S3 | Confirmed — 8/8 PASS | 0 | 42 |
| F52 | S3 | Confirmed — 5/5 PASS | 3 | 78 |
| F55 | S3 | Confirmed — 5/5 PASS | 1 | 31 |
| F62 | S3 | Confirmed — 6/6 PASS | 3 | 140 |
| F65 | S1 | Confirmed — 4/4 PASS | 6 | 17 |
| F66 | S1 | Confirmed | 6 | 23 |
| F67 | S1 | Confirmed — 3/3 PASS | 8 | 48 |
| F155 | S12 | Partial — 5/5 PASS | 7 | 97 |
| F162 | S11 | Partial — 3/3 PASS | 11 | 64 |
| F165 | S13 | Confirmed — 4/4 PASS | 2 | 20 |
| F174b | S4 | Confirmed — 5/5 PASS | 5 | 41 |
| F179 | S6 | Resolved-as-relabel — 5/5 PASS | 6 | 25 |
| F230 | S15 | Confirmed (negative) — 6/6 PASS | 3 | 17 |
| F251 | S12 | Confirmed — 5/5 PASS | 9 | 102 |
| F258 | S12 | Confirmed — 6/6 PASS | 4 | 49 |
| F270 | S10 | *(no Status line)* | 4 | 3 |

Not one header says superseded. A reader — or a batch pass — working from headers alone would classify all 16 as KEEP, and would be wrong about the *status* of every one of them while being accidentally right about the *disposal*.

### 3.2 Keyword triage is worse than silence

A scan for supersession-adjacent language (`superseded|retired|obsolete|excluded|no-go|negative|circular|wrong|error|withdrawn`) in title + status flags **67 of 271** findings. Nearly all are **false positives of a specific and important kind: they are negative results.** F127 ("a four-avenue no-go"), F282 ("the model admits **no** slow-roll inflaton"), F108 ("an exact no-go theorem"), F145 ("a bare-coupling no-go"), F292 ("$d=6$ and $d=9$ excluded").

These are the falsification record. They are the load-bearing evidence for why the model looks the way it does, and they are the *last* files that should leave `findings/`. Any keyword-driven sweep will surface them first and most confidently, because they use the vocabulary of obsolescence to describe their own results.

### 3.3 What the ledger actually says is dead

Read the `retained:` clauses and the supposed candidates dissolve:

- **S13 → F165** — `RETAINED: EVERYTHING F165 CONCLUDES.` The record supersedes two *sub-claims inside* the finding (a redundant anomaly row), not its conclusion. A file-level banner here would misinform.
- **S15 → F230** — `RETAINED: The whole file, as the standing negative result behind founding decision 7.` What is superseded is the *attack script*, not the finding.
- **S11 / S12 → F162, F155, F251, F258** — what was superseded is a **code defect**: a `mod 2π` refold of shifted momentum against a kernel whose period lattice is $\sqrt3\cdot$fcc. The physics findings stand; a module they used had a bug.
- **S1 → F65, F66, F67** — the σ-bilinear *photon attribution* died. The bilinear field construction survives for W/Z/gluon, and F65–F67 are the birefringence exclusion chain that **forced** the paired-spinor photon of F69. Deleting them deletes the reason F69 exists.
- **S3 → F50, F52, F55, F62** — see §4.
- **S4 → F174b** — reclassified, not superseded; the vacuum/weak-field results are explicitly retained.

None of the 16 clears "nothing live survives." Several are named in the ledger for reasons that have nothing to do with the finding's own validity.

---

## 4. The dielectric-gravity premise, checked

The motivating example for this pass was that findings related to dielectric gravity are superseded by the adoption of the full-tensor equations and should all go. The ledger says otherwise, on both sides:

- **The dielectric is still canonical** for its regime. S4's `retained:` keeps the vacuum and $p \ll \rho c^2$ results — factor-2 bending, $\beta=\gamma=1$, Mercury, Shapiro, redshift — plus the structural $G = a^2c^3/(8\pi\sqrt3\,\hbar)$. `CLAUDE.md` Decision 4 states the same: $K=\exp(2GM/rc^2)$ is the **vacuum/weak-field representation** of the induced Einstein equation. It is not going away.
- **The rest-mass-sourced route (F50/F52/F55/F62) was superseded by F64 in May, not by F178** — and even then only partially. S3 records that F62's lapse-mix sign convention is *still production code* in `interactions/gravity.py`, and that F50's G2/G3 and F52's H3/H3b remain the standing regressions. F62 carries 140 code/test references.
- **F114 is the one genuinely superseded object** — and it is already bannered, and its paper is already in `deprecated/`.

So the cluster expected to sweep out wholesale is the cluster that mostly stays, and the one file that should go was disposed of ten months ago.

---

## 5. The Stage 0 fix, and why it was not applied

The intent was to apply the 16 missing banners. Inspection of the mechanism changed the recommendation.

`tools/apply_supersession_banners.py` builds its worklist from `record["tests"]` and stamps into a **Python module docstring** via `ast`. It never reads `record["findings"]`, and returns `no-docstring` for markdown. Its gate test `test_no_orphan_banners` walks `tests/` and `src/` only. `test_every_finding_referenced_has_a_finding_file` checks only that the file *exists*.

Consequences:

- The `findings:` blocks added during the F16–F19 retirement (on S1, S16, S17) are **read by nothing**. The markdown banners on those four files were hand-written.
- All 8 banners on active findings are hand-written and unverified. Four of them (F20, F22, F64, F176b) have no ledger entry at all — the exact "tombstone the ledger does not know about" that `test_no_orphan_banners` exists to catch, sitting in the one directory that test does not walk.
- Hand-writing 16 more banners would add 16 more unverified strings and make the drift problem worse.

**Recommended fix, in order:**

1. Extend `apply_supersession_banners.py` with a markdown path (blockquote banner, same `SENTINEL`, keyed off `record["findings"]`), and widen `test_no_orphan_banners` to walk `findings/` and `deprecated/findings/`. This makes the finding-level banner a checked artifact rather than a convention.
2. Populate `findings:` blocks on S3, S4, S6, S10, S11, S12, S13, S15 with per-file `status` + `dead` + `live` text, taken from the `retained:` clauses already written. For S13 and S15 the correct `status` is arguably neither `fully_` nor `partially_superseded` — the ledger retains everything — so the vocabulary may need a fourth term (`sub_claim_superseded`) rather than a banner that overstates.
3. Reconcile the four orphan banners (F20, F22, F64, F176b) into ledger records, or remove them.

**Not executed here because of concurrency.** The claim `gracious-jolly-meitner` is open on F20–F25 and has already escalated one `supersessions.yaml` edit (adding F20 to S1) rather than executing it. Steps 1–3 touch that same file and one of those same findings. They belong to a single session that owns the ledger.

---

## 6. Disposition

| Class | Count | Action |
|---|---|---|
| KEEP — live, no ledger entry | 262 | none |
| KEEP — ledger names them, but `retained:` keeps the conclusion | 16 | banner once §5.1 lands; **do not move** |
| KEEP — already bannered, correctly | 4 | none |
| KEEP — bannered but orphaned from the ledger | 4 | reconcile per §5.3 |
| RETIRE | **0** | — |
| Review individually | 1 | F32 (§7) |

## 7. The one item worth a look

**F32** — *"W_μ Phase 2: Free W Propagation — F26 Rotation Law per Isospin Component"*, `Confirmed — 4/4 tests PASS`. The only finding in the corpus with **zero** citations from other findings and **zero** references from `src/`, `tests/` or `scenarios/`.

That is an orphan signal, not an obsolescence signal, and the distinction matters: F32 may be perfectly correct and simply superseded in practice by the later W/Z work without anyone recording it, or it may be live physics that nothing currently exercises. Either way it is the single file where a `/review-finding` pass would tell us something a header cannot. It does **not** meet the retirement bar on this evidence.

---

## 8. Answer to the question that prompted this

*Can obsolescence be determined from the header, or does `/review-finding` have to run on every finding?*

**Neither.** Headers cannot dispose — §3 shows the status line is silent and the keyword signal is actively misleading, because the project's most valuable findings are negative results that describe themselves in the vocabulary of obsolescence. But 282 reviews are not the alternative either, because the ledger already holds the disposal reasoning for every finding that has one, and it says *retain* in almost every case.

The binding constraint is not knowledge, it is **enforcement**: the reasoning exists in `supersessions.yaml` and is not connected to the finding files. Fix the connection (§5) and the question answers itself continuously, for free, at every `make gate` — instead of being re-derived by a triage pass each time. That is the same lesson `deprecated/README.md` records from P0.4, one directory over.

For the residual — findings with no ledger record whose status is genuinely unknown — `/review-finding` remains the only instrument, and F32 is the only file this pass can justify pointing it at.

---

*Baseline note: gate record `supersession-ledger` was already red before this session (`S14-P5.1-live-display-retired`: malformed decision id `P5.1`, a concurrent claim's record absent from HEAD). Captured pre-edit; not caused by this pass.*
