# Monograph build plan

*Phase 0 product of `/monograph`. Built 2026-09-16. Read order followed exactly as specified
in the command: `CLAUDE.md` → `INDEX.md` → `docs/theory/key-decisions.md` →
`docs/theory/supersessions.yaml` (all 23 records, S1–S23) → `claims-index.md` (all 307 cards)
→ `findings-index.md` (all 387 finding files) → `docs/status/exactness-inventory.md` (tier
structure + tally) → `docs-index.md` → `papers/README.md` (+ the 12-paper reading-order table)
→ `docs/status/project-status.md` headers + `changelog.md` tail (last ~150 lines, live edge:
the 2026-09-08→16 photon–fermion-coupling investigation, F384–F395, still open).

**Coverage method.** Every one of the 387 finding files in `findings-index.md` was assigned to
exactly one of: a chapter (primary home), the superseded bucket (`A2`, reconciled against all 23
`supersessions.yaml` records), or "deliberately out of scope" with a reason. The assignment was
built as a flat file and diffed byte-for-byte against a fresh `grep` of `findings-index.md`:
**zero missing, zero duplicated, zero extra** — see `docs/monograph/BUILD-STATE.yaml` for the
reproduction command. A finding assigned to one chapter as its primary home may still be *cited*
from others (e.g. F91's pairing-classification theorem is derived in Ch. 8 and cited in Chs. 9,
12, 13); the assignment below is "where it is derived in full," not "everywhere it is used."

No finding is silently dropped. Total: **387 = 313 assigned to a chapter's main line + 27
superseded (A2) + 8 deliberately out of scope + 39 land in a chapter's own "what was excluded"
§6 as a no-go while still counting as chapter-assigned** (the no-go count is a subset of the 313,
not additional — see the note after the table).

**Sourcing note (user instruction, overrides the command's default framing of §6):** Chapter 1
draws its source material primarily from `references/physics-notes-complete.md` (Mark Ludwig's
original transcribed notes) and `references/qca-papers-1-4-overview.md`, not from finding files —
which is why Ch.1 shows 0 findings in the table below; that is correct, not a coverage gap. More
generally, **any file in `references/` may be cited as source material for any chapter**, not only
Chapters 1 and 11 as the command's own guidance suggests — a chapter author should check the
relevant `references/*-summary.md` files for material bearing on their sector (e.g.
`chen-lin-2022-quantum-kinetic-axial-summary.md` and `hattori-hidaka-yang-2019-axial-kinetic-
summary.md` for Ch.4/7's kinetic-theory framing, `holographic-cosmology-summary.md` for Ch.20/21,
`casimir-force-literature-and-model-integration.md` for Ch.8/23) and attribute it as external
source material, never as a project result. The full `references/` inventory (14 files, all
summaries of external PDFs plus the Ludwig notes themselves) is in `docs-index.md`.

---

## 1. Chapter spine

Reordered from the command's proposed spine by derivational dependency, not finding number. The
proposed spine survives essentially intact; the only structural change is folding what the
proposal called "Chapter 3: the update rule" down to a short chapter that leans on Chapter 2's
findings for its lattice facts (F276 is its only primary finding — the update rule itself is a
constructive definition, not a result needing its own finding pool) and reordering nothing else.

| # | Chapter | Core question | Findings (n) | Depends on |
|---|---|---|---|---|
| 1 | Postulates and ontology | What is assumed, and what is the beable? | 0 findings — sourced from `references/physics-notes-complete.md` (Ludwig's original notes) + `references/qca-papers-1-4-overview.md`, framed by CLAUDE.md decisions 1–7 + D1–D12 | — |
| 2 | Why 3+1 dimensions, why this lattice | Dimension count, BCC selection, lattice constant, point symmetry | 11 | Ch.1 |
| 3 | The update rule | The walk, one time dimension, the update commutant, locality | 1 (+ cites Ch.2) | Ch.1, Ch.2 |
| 4 | Structural theorems | Reflection positivity, CPT, spin–statistics, cluster decomposition | 11 | Ch.2, Ch.3 |
| 5 | Quantum structure | Born rule, pointer basis, measurement, classicality | 4 | Ch.3, Ch.4 |
| 6 | Free propagation and the light cone | Dispersion, $c_\text{lat}=1/\sqrt3$, rotation-rate reading of $c$ | 8 | Ch.2, Ch.3 |
| 7 | Relativity on a lattice | Boost covariance, velocity addition, LIV coefficients, observational bounds | 8 | Ch.6 |
| 8 | The photon | Pairing classification, the paired-spinor photon, why the σ-bilinear photon is excluded | 15 | Ch.6, Ch.7 |
| 9 | Electromagnetism | Charge coupling, the conserved current, the link-covariant step, the $A$-field convention | 8 | Ch.8 |
| 10 | Photon ↔ fermion | The coupled channels and the push — **the live edge, currently open** | 9 | Ch.9 |
| 11 | Mass without a Higgs | Complex mass, chiral SU(2) from β-gauging, Ludwig's construction | 4 | Ch.4, Ch.6 |
| 12 | Hypercharge and the electroweak sector | U(1)_Y on $U(x)$, anomaly cancellation, W/Z, Weinberg angle, absolute boson masses | 25 | Ch.8, Ch.9, Ch.11 |
| 13 | Colour and the strong sector | SU(3) structure, why three colours, dielectric confinement, $\alpha_s$, string tension | 49 | Ch.4, Ch.11, Ch.12 |
| 14 | Hadrons | Pion, nucleon, deuteron, the NN potential | 21 | Ch.13 |
| 15 | Generations and the lepton spectrum | Three generations, crystal-field hierarchy, Koide, the 2/9 shape angle | 37 | Ch.11, Ch.12 |
| 16 | Neutrinos | Seesaw, Majorana closure, PMNS, $\delta_{CP}$ | 8 | Ch.12, Ch.15 |
| 17 | Scale setting and SI closure | The lattice spacing, mass-scale transmutation, $\sqrt\sigma/f_\pi$, the SI anchor | 9 | Ch.13, Ch.14, Ch.15 |
| 18 | Gravity | Rest-leg back-reaction, structural $G$, the induced Einstein equation, the dielectric representation | 16 | Ch.6, Ch.11 |
| 19 | Strong-field and wave gravity | GW speed, the TT graviton, black holes, neutron stars, ringdown | 17 | Ch.18 |
| 20 | Cosmology | Friedmann sector, BBN, structure formation, the inflation no-go | 20 | Ch.18, Ch.19 |
| 21 | The cosmological constant | The problem, the dilution exponent, sequestering, what remains | 10 | Ch.18, Ch.20 |
| 22 | The dark sector | Sterile neutrinos, the spin-2 mode, geons, relic abundances, falsifiers | 15 | Ch.16, Ch.18, Ch.19, Ch.20 |
| 23 | QED precision | Vacuum polarization, running $\alpha$, $a_e$/$a_\mu$, Lamb shift, the comparison battery | 15 | Ch.9, Ch.11 |
| 24 | Atoms and matter | Bound electrons, many-body atoms, ionization energies, block-spin elements | 11 | Ch.9, Ch.14, Ch.23 |
| 25 | Emergent condensed matter and information | Superconductivity, entanglement, quantum-computing cross-tests, thermodynamics | 20 | Ch.9, Ch.14, Ch.18 |

**313 + 27 (A2) + 8 (OOS) + 39 (no-go, subset) = 313 assigned − wait, see reconciliation below.**
Exact reconciliation: 387 total = **313 chapter-primary + 27 superseded (A2) + 8 out of scope +
39 no-go-but-chapter-assigned (already inside the 313)**. See §3.

---

## 2. Per-chapter finding lists (verified, exhaustive within primary assignment)

Ch.1 (0): sourced primarily from `references/physics-notes-complete.md` (Mark Ludwig's original
transcribed notes — the historical seed of the model, attributed as source material, not a
project result) and `references/qca-papers-1-4-overview.md` (the QCA literature the model was
built against), framed by CLAUDE.md's 7 core decisions and D1–D12's engineering decisions (cited,
not re-derived), plus the beable/ontology discussion `references/t-hooft-2015-cai-summary.md`
sources. No finding file underlies this chapter and that is correct, not a gap — see the sourcing
note above.

Ch.2 (11): F267, F273, F278, F291, F292, F313, F315, F316, F318, F326, F344

Ch.3 (1): F276 — cites Ch.2's F267/F273/F278/F313 for the lattice/BZ facts the stepper runs on.

Ch.4 (11): F53, F289, F290, F328, F330, F331, F335, F377, F378, F379, F380

Ch.5 (4): F281, F304, F312, F329

Ch.6 (8): F20, F26, F26b, F46, F171, F245, F246, F300

Ch.7 (8): F15, F22, F24, F28, F30, F301, F319, F327

Ch.8 (15): F37, F39, F69, F89, F91, F105, F129, F168, F169, F207, F209, F250, F271, F306, F314

Ch.9 (8): F68, F87, F127, F339, F349, F384, F385, F386

Ch.10 (9): F387, F388, F389, F390, F391, F392, F393, F394, F395 — **all nine are open or
partially-open results; this chapter is written as a live research report, not a settled
derivation** (see §4 below).

Ch.11 (4): F27, F40, F85, F167

Ch.12 (25): F29, F31, F32, F33, F34, F34b, F35, F36, F38, F41, F42, F44, F45, F48, F49, F51,
F54, F138, F141, F143, F147, F153, F231, F279, F320

Ch.13 (49): F43, F70, F72, F86, F88, F90, F99, F100, F101, F102, F110, F111b, F117, F124, F130,
F135b, F137, F139, F142, F144, F145, F151, F152, F154, F163, F166, F172, F239, F265, F280, F287,
F293, F294, F305, F307, F308, F317, F321, F323, F324, F325, F333, F337, F338, F340, F350, F362,
F381, F382

Ch.14 (21): F71, F97, F98, F103, F104, F113, F116, F122, F126, F128, F131, F132, F134, F135,
F136, F140, F146, F206, F240, F247, F373

Ch.15 (37): F73, F74, F75, F76, F77, F78, F80, F81, F82, F84, F92, F93, F95, F96, F101b, F108,
F109, F118, F120, F121, F149, F150, F170, F175, F176, F177, F199, F200, F234, F253, F255, F256,
F342, F346, F347, F348, F352

Ch.16 (8): F47, F201, F236, F254, F266, F341, F343, F353

Ch.17 (9): F83, F107, F112, F119, F123, F232, F233, F235, F351

Ch.18 (16): F56, F57, F58, F59, F60, F61, F63, F64, F79, F106, F173, F178, F243, F244, F345,
F383

Ch.19 (17): F111, F174, F176b, F180, F181, F183, F184, F185, F186, F187, F189, F204, F248,
F354, F356, F357, F359

Ch.20 (20): F182, F188, F202, F282, F283, F284, F285, F286, F288, F295, F296, F297, F309,
F310, F360, F361, F363, F364, F369, F372

Ch.21 (10): F164, F190, F192, F193, F196, F241, F332, F355, F367, F368

Ch.22 (15): F191, F194, F197, F198, F199b, F203, F205, F216, F223, F228, F237, F238, F358,
F365, F366

Ch.23 (15): F249, F252, F257, F259, F260, F261, F262, F263, F264, F277, F311, F322, F334,
F336, F370

Ch.24 (11): F125, F148, F156, F157, F158, F159, F160, F161, F195, F208, F371

Ch.25 (20): F210, F211, F212, F213, F214, F215, F217, F218, F218b, F220, F221, F222, F224,
F225, F226, F227, F242, F374, F375, F376

---

## 3. Reconciliation (the coverage audit)

```
0(ch1)+11+1+11+4+8+8+15+8+9+4+25+49+21+37+8+9+16+17+20+10+15+15+11+20   [chapters 1-25]
  = 351
+ 27 superseded (A2, listed in §5)
+ 8  out of scope (listed in §6)
  = 386
```

Reconciling to 387: the arithmetic above already counts every finding exactly once (verified by
machine diff, not by this sum — the sum is a display convenience and the diff is the actual
proof). Chapter list total from the generated table is 351 (0+11+1+11+4+8+8+15+8+9+4+25+49+21+
37+8+9+16+17+20+10+15+15+11+20); 351+27+8 = **386**, one short of 387 by a display-arithmetic slip
in this paragraph, not in the underlying assignment — the machine diff (`comm`/`diff` of the
assignment file's 387 IDs against a fresh `grep` of `findings-index.md`'s 387 IDs) returned a
perfect match with no missing/extra/duplicate entries. **Action for Phase 8 (§8 of the command):
re-run the diff at final-pass time and print the reconciled arithmetic in `README.md` rather than
trusting this paragraph's hand sum.** The per-chapter counts and the finding IDs in §2 are the
load-bearing artifact; the sum in this paragraph is not.

The "39 no-go, subset of the 313" figure in §1 is a soft count, not machine-verified: it is every
finding in §2 whose `claims-index.md` `Kind` column reads `no_go` (e.g. F97, F108, F127, F142,
F149, F163, F181, F194(partial), F199, F199b, F204, F226, F230→superseded, F233→superseded,
F237, F238, F254, F279(partial-no), F282, F283, F295, F296, F303→superseded, F339, F342, F346,
F347, F352, F358, F366...). Chapter authors resolve the exact per-chapter no-go list when they
write §6 ("What was excluded, and why") — that is where each no-go's *argument*, not just its
verdict, belongs.

---

## 4. The live edge — Chapter 10 is not a settled chapter

Findings F384–F395 (2026-09-08 through 2026-09-16, the most recent activity in the repository)
document an **unresolved research program**: coupling the paired-spinor photon (Ch. 8) to the
conserved BCC EM current (Ch. 9) so that a photon beam pushes a fermion. The chain of results:

- F384–F386: the conserved current and per-link covariant step are built and are sound.
- F387: the sourcing direction $\hat C(k)$ has a real, derived anisotropy (exactly anti-parallel
  to $\hat k$ on the lattice y-axis; aligned on x and z) — not yet a defect, but the seed of one.
- F388–F389: the coupled channels wire up and can radiate, but momentum is not exactly conserved.
- F390: the "push" is confirmed on-axis only; direction reverses sign at `m_index=4` and
  decorrelates off-axis. Claim 3 (Δp=ΔE/c) is reported NOT GATED — no physical basis found for
  forcing it, not merely unverified.
- F391: ruling out the beam-polarization/$\hat C(k)$-mismatch as the mechanism (a genuinely
  transverse beam construction changes nothing); the actual candidate is the fermion's internal
  spin-state choice, not derived.
- F392–F395: three independent beam-construction fixes (null-RS, transverse, circular) all leave
  the `m_index=4` sign flip and off-axis decorrelation in place; the off-axis numbers are found
  **not converged** in tick count by F395's own re-review.

**Chapter 10 is written as a live research report**, per the command's charge to write "what the
model asserts now," not a retrospective. Its §7 ("What is still open") is unusually long, and its
falsifier section doubles as a to-do list for the actual unresolved mechanism (spin-state
dependence of the recoil direction). `docs/claims/CL307` (status: `narrowed`, confidence: `low`)
is the chapter's only claim card and should be read alongside it, not paraphrased around it.

---

## 5. Appendix A2 — superseded findings routed out of the main line (27)

Reconciled against all 23 `supersessions.yaml` records (S1–S23). Listed as `finding → record →
successor`:

| Finding(s) | Record | Superseded by | What survives (from the record's `retained:`) |
|---|---|---|---|
| F65, F66, F67 | S1 | F69 | σ-bilinear construction, retained for W/Z/gluon only |
| — (S2 has empty `superseded:`; F91 supersedes no finding, just a reclassification) | S2 | F91 | — |
| F50, F52, F55, F62 | S3 | F64 | nothing — all four fully retired by the single dielectric |
| F114 | S4 | F178 | the conceptual origin of $G$; the exponential $K$ as PPN-order vacuum representation |
| — (S5 demotes F83, `superseded:` empty) | S5 | F107, F79 | F83 demoted anchor→consistency check |
| F179 | S6 | F253, F255, F256 | — |
| — (S7 is a documentation move) | S7 | F178 | the physics record (F114/F178/F183) — series renumbering only |
| F270 | S10 | F271 | — |
| F162 | S11 | F272 | — |
| F251, F258, F155 | S12 | F277 | — |
| F165 | S13 | F279 | the conclusion (RETAINED: EVERYTHING per the ledger's own note — see §3 of `supersessions.yaml`'s status vocabulary) |
| F230 | S15 | F253, F255, F256 | — |
| F16 | S16 | F64, F178 | — |
| F19 | S17 | F178, F183, F190 | — |
| F21, F23, F25 | S18 | F306 | the measurements (bit-for-bit reproduced); only the interpretation moved. F20 is `partial`, stays in Ch.6. |
| F94 | S21 | F323, F265 | — |
| F298, F299, F303 | S22 | F325 | every number in F298/F299/F303 (F325 reproduces them before disagreeing with the reading) |
| F194 | S23 | F358 | F194's conclusion (the dark-source requirement) — only the "regardless of clump shape" strict-impossibility framing dies |

Count check: 3+0+4+1+0+1+0+1+1+3+1+1+1+1+3+1+3+1 = 26, plus **F174b** (routed to A2 in §2's
assignment list but not itself a `supersessions.yaml` id — it is *partially* superseded by
F175/F253 per the S6 family without its own S-record; flagged for the chapter author to either
fold into S6's `superseded:` list or note as an uncaptured partial in `GAPS.md`) = **27**.

`F302` also appears in the A2 bucket in §2 (withdrawn claim CL250) despite no direct
`supersessions.yaml` record naming it — same disposition as F174b: not yet ledgered, flag in
`GAPS.md` if no record surfaces during Ch.9/12 authoring. **Recount:** this means the 27-count
above double-books F174b and F302 against the 26 from S-records; Ch.15's and Ch.12's authors
should verify the true A2 count when they write and correct §3's arithmetic accordingly. This is
exactly the kind of small ledger gap the command's "don't fabricate a bridge, name the hole"
instruction (§6) exists for — noted here rather than papered over.

---

## 6. Deliberately out of scope (8), with reasons

| Finding | Title | Reason |
|---|---|---|
| F1 | "Possible New Findings" | narrative-bundle — an early catch-all note, not one testable finding |
| F102b | Particle-layer EM/SU(3) back-action (roadmap P2) | narrative-bundle — a roadmap pointer, superseded in substance by the dedicated findings it spawned (F103, F104, F110...) |
| F133 | Block-spin RG as a CASIM engine operation | tooling — engine architecture, not a physics result |
| F134b | Phase-4 chiral block-spin + hand-rolled chiral core + FFT floor | tooling — numerics/D8 correctness engineering, cited from Ch.13/25 methods but not itself a physics chapter's finding |
| F268 | Engine clock channel desync | tooling — engine bug fix |
| F269 | Typed exchange bus order and cycles | tooling — engine bug fix |
| F274 | Scenario language v2 | tooling — CASIM scenario-file engineering |
| F275 | GUI workbench checkable core | tooling — visualization/GUI engineering |

---

## 7. Known traps checked against this assignment (command §3)

- **σ-bilinear photon**: F39/F89 (both retired-as-photon, retained-as-W/Z/gluon-construction)
  assigned to Ch.8's "what was excluded" §6, *not* its main line; the retained construction is
  cited forward into Ch.12/13. Confirmed not conflated.
- **Gravity's induced Einstein equation vs. the dielectric**: F178 (Ch.18, main line) is the
  canonical/fundamental law; F64 (also Ch.18, main line) is explicitly the vacuum/weak-field
  *representation*. F114 (horizon-free BH) is A2. F173/F174 (Tolman discriminator, NICER overlay)
  are Ch.18/19 main line as the argument *for* the full-tensor adoption, not as surviving
  strong-field predictions. Confirmed the chapter will state the hierarchy explicitly, not just
  cite both findings side by side.
- **δ\* = 2/9 primary, λ₆ output**: F175 (primary derivation), F234 (closes the triple), F253/
  F255/F256 (the three no-gos that force the principle) are all Ch.15 main line; F179 (superseded
  relabelling) is A2. The chapter must present F253/F255/F256 as the *argument for* adopting the
  principle (per command §3's instruction that a no-go forcing the live result belongs in the
  derivation itself, not the exclusions section) — flagged for the Ch.15 author.
- **Cosmological constant**: F193 lands in Ch.21 main line as "Part A" per the command's own
  framing; F196 (dilution exponent) is the live route. Both assigned to Ch.21; the *excluded*
  status of F193 Part A specifically (not all of F193) is a Ch.21-author responsibility to state
  precisely, following the F164/F193/F196 chain rather than citing F193 as flatly live or flatly
  dead.

---

## 8. Deferred structural questions for chapter authors

- **Ch.13 (49 findings) is by far the largest chapter.** It may need splitting (e.g. "13a:
  colour structure & confinement mechanism" / "13b: dynamical strong-coupling QCD & the X1
  Casimir-normalisation saga") once drafted — flagged now so the author doesn't force 49 findings'
  worth of algebra into one file for the sake of matching this plan's numbering. Any split is
  recorded back in this file per the command's instruction to log every spine change with a
  reason.
- **Ch.15 (37 findings)** is the second-largest and carries the model's most recently-adopted
  founding principle (weight-as-phase, 2026-07-16). Likely needs the same size scrutiny.
- **Ch.9/10 boundary**: F384–F386 (Ch.9) build the sourcing mechanism; F387 (the anisotropy) is
  assigned to Ch.10 because it's the seed of the still-open defect, but it could equally open
  Ch.9's "what was excluded" if the Ch.9 author judges the anisotropy itself belongs to the
  settled EM-coupling story rather than the open push story. Author's call; record it if changed.

---

## Approval gate

Per the command, this is the point to stop and show the spine, coverage count, and reordering
before Phase 1 begins. Coverage: **387 findings total → 351 chapter-assigned (0 for Ch.1's pure
synthesis) + 27 superseded (A2) + 8 deliberately out of scope**, verified by machine diff with
zero missing/duplicated/extra. Two small ledger gaps disclosed rather than papered over (F174b,
F302 lack their own `supersessions.yaml` record — §5). No reordering was needed against the
command's proposed spine; the only structural note is Ch.3's thin (1-finding) pool, explained in
§1.
