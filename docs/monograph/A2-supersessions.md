# Appendix A2 — Supersessions

*What replaced what, when, why, and which chapter now carries the live version. Reconciled
against all 23 records in `docs/theory/supersessions.yaml` (S1–S23) plus every claims-layer
bookkeeping artifact the chapter-writing pass found and logged in `GAPS.md`. Two different kinds
of "supersession" appear in this project and must not be conflated — this appendix keeps them in
separate tables.*

## A2.1 — Genuine physics supersessions (`supersessions.yaml`, 23 records)

| Record | Date | Kind | Superseded | By | Live chapter | What survives |
|---|---|---|---|---|---|---|
| S1 | 2026-06-01 | superseded | F65, F66, F67, F17, F18 | F69 | Ch.8 | σ-bilinear field construction, retained for W/Z/gluon (Ch.12/13a) |
| S2 | 2026-06-04 | superseded | — (reclassification) | F91 | Ch.8, Ch.13a | Gluon propagator migrated chiral→even in-tree same day |
| S3 | — | superseded | F50, F52, F55, F62 | F64 | Ch.18 | Nothing — all four fully retired by the single dielectric |
| S4 | — | reclassified | F114 | F178 | Ch.18, Ch.19 | The conceptual origin of $G$; $K=e^{2u}$ as PPN-order vacuum representation |
| S5 | — | demoted | — (F83 demoted) | F107, F79 | Ch.17 | F83 demoted from anchor to consistency ceiling |
| S6 | — | superseded | F179 | F253, F255, F256 | Ch.15 | — |
| S7 | — | deprecated | — (documentation move) | F178 | Ch.18 | The physics record (F114/F178/F183); paper-series renumbering only |
| S8 | — | methodology | D2 | D6–D11 | (engineering, not physics) | — |
| S9 | 2026-08-01 | superseded | — (convention, never a finding) | F270 | Ch.9 (energy convention) | — |
| S10 | — | superseded | F270 | F271 | Ch.8 | — |
| S11 | — | superseded | F162 | F272 | Ch.13b | — |
| S12 | — | superseded | F251, F258, F155 | F277 | Ch.23 | Every number in F251/F258/F155 (F277 reproduces them before disagreeing) |
| S13 | 2026-08-02 | superseded | F165 | F279 | Ch.12, Ch.16 | F165's conclusion (hypercharge forced to one normalization) — only the derivation moved (Majorana step, not gravitational anomaly) |
| S14 | — | methodology | — | P5.1 | (engineering) | — |
| S15 | 2026-08-03 | superseded | F230 | F253, F255, F256 | Ch.15 | — |
| S16 | 2026-08-03 | superseded | F16 | F64, F178 | Ch.18 | — |
| S17 | 2026-08-03 | superseded | F19 | F178, F183, F190 | Ch.18, Ch.19, Ch.21 | — |
| S18 | 2026-08-04 | superseded | F21, F23, F25 | F306 | Ch.8 | Every measurement (bit-for-bit reproduced) — only the interpretation moved; F20 `partial`, stays live in Ch.6 |
| S19 | 2026-08-04 | retracted_by_review | — (2 of 3 F22 claims) | F15 | Ch.7 | F22's claim 2 ($\rho(m)$), correct and load-bearing |
| S20 | 2026-08-17 | superseded | F115 | F138, F231 | Ch.12 | — |
| S21 | 2026-08-17 | superseded | F94 | F323, F265 | Ch.13b | — |
| S22 | 2026-08-18 | superseded | F298, F299, F303 | F325 | Ch.13a, Ch.13b | Every number in F298/F299/F303 (F325 reproduces them before disagreeing with the reading) |
| S23 | 2026-09-03 | superseded | F194 (one sub-claim only) | F358 | Ch.22 | F194's conclusion (dark-source requirement) — only the "regardless of clump shape" strict-topological framing dies |

**Two findings routed to appendix A2 in the build plan (`00-plan.md` §2) have no corresponding
`supersessions.yaml` record** — flagged as an uncaptured ledger gap during Phase 0, not fixed
here: **F174b** (folded into the S6 family in substance but never given its own entry) and
**F302** (its claim CL250 reads `withdrawn`; no chapter's research turned up a reason to doubt
this is a genuine, if unrecorded, supersession — unlike the claims-layer artifacts in A2.2 below,
nothing in the finding's own header contradicts the withdrawal).

## A2.2 — Claims-layer bookkeeping artifacts (NOT physics supersessions)

*A second, unrelated phenomenon the chapter-writing pass found and re-found: a claim card
(`docs/claims/CL*.md`) reads `status: withdrawn`, but the finding's own header carries no
supersession banner and no `supersessions.yaml` record names it. In every one of the seven cases
below, an independent chapter read the finding's actual text and found the physics live and
in active use by later chapters — the withdrawal is a mechanical seeding-pass misreading (often
of the finding's own **title**, e.g. "F233...supersedes F119" describing what the finding does to
an *earlier* no-go, misread as a self-referential banner). None of these is fixed in the
monograph (documentation-only); each is logged where found.*

| Claim | Finding | Found by | Gap | Real status |
|---|---|---|---|---|
| CL029 | F15 | Ch.7 | (in §7.2.3, unnumbered) | Live — F15 is S19's own survivor/replacement |
| CL084 | F89 | Ch.8 | G-6 | Live — retains its conclusion; W/Z/gluon table needs the F91 correction |
| CL251 | F306 | Ch.8 | (in G-6's chapter) | Live and unchanged |
| CL082 | F87 | Ch.9 | (in §9, unnumbered) | Live — foundational infrastructure F384–F386 build on |
| CL069 | F72 | Ch.13b | (in §13b.1) | Live |
| CL231 | F265 | Ch.13b | (in §13b.1) | Live |
| CL160 | F181 | Ch.19 | G-9 | Live — F178's own two-function interior kernel, cited approvingly by F184/F185/F356 |
| CL205 | F233 | Ch.17 | G-14 | Live — one of Chapter 17's own central, load-bearing results |
| CL189 | F215 | Ch.25 | (investigated, not logged — repeat pattern) | Live |
| CL193 | F218b | Ch.25 | (investigated, not logged — repeat pattern) | Live |
| CL200 | F226 | Ch.25 | (investigated, not logged — repeat pattern) | Live |

**A related but distinct third phenomenon — genuine content staleness, not a mechanical
misread** — appears twice: **CL022/CL252** (Ch.13b's Gap G-11: both cards predate three findings,
F337/F340/F350, that bear directly on their own stated $\alpha_s$/$d_1$ brackets) and **CL177**
(Ch.22's Gap G-15: F203's falsifiability battery is accurately reported, but three of its six
tests have since been sharpened or superseded in substance by F205/F237/F228, and the card was
never updated to say so). Neither of these is a bookkeeping error — the cards correctly reflect
what was true when written; they are simply out of date against later findings in the same tree.

**Pattern note for whoever next touches the claims layer**: eleven independent chapters, working
cold and without shared context, each independently rediscovered this same artifact. That is
strong evidence the claims-seeding pass (`docs/audits/consolidation-plan-2026-08-04.md`) has a
systematic false-positive mode on findings whose own title or a cited prior finding's name
contains a word like "supersedes," "withdrawn," or "retracted" — worth a dedicated audit pass
rather than seven more individual corrections.
