# Finding-number collisions — decision sheet

> **Note added 2026-08-05 - 09:30.** This sheet is the record of the 2026-07-31 *duplicate* pass and
> is still accurate for that. Its **gap** counts are a snapshot, not a standing figure: numbers are
> now taken one at a time at write time, lowest free first (CLAUDE.md "Concurrency"), so the gap
> list is a work queue that shrinks as findings land rather than an archive that grows. Twenty-two
> of the gaps are declared `status: free` in `docs/design/finding-numbers.yaml` and will be spent by
> ordinary work. The duplicate half of this sheet is unaffected — a `b` suffix is still how a
> genuine collision is resolved.


*Created 2026-07-31 - 10:15, **executed 11:05**. Companion to `docs/design/finding-numbers.yaml`, which is the machine-readable record `casim index` enforces. See also `docs/status/baseline-provenance.md` for the other decision queue this session produced.*

## Result: 10 collisions → 1, and both numbering gaps closed

| | before | after |
|---|---:|---:|
| Duplicated finding numbers | 10 | **1** (F200) |
| Numbering gaps | 18 | **16** (F111, F127 closed) |
| Finding files | 258 | 261 |

**The rule applied:** the less-load-bearing side of each pair takes a **`b` suffix** — `F101b`, `F26b`, and so on. That was your instruction ("change the older of the two to b") with one adjustment I had to make and want to flag.

### The "older" rule could not be applied as stated

For 9 of the 11 pairs there is **no recorded age difference at all**: both files entered the repo in the same bulk commit (`git log --diff-filter=A` gives an identical timestamp) *and* carry the same internal date. Git and the documents agree that nothing distinguishes them by age.

So the tie-break used was the asymmetry your instruction was pointing at — **which side the rest of the repo actually cites** — measured before this session's own documents existed:

| # | Kept the bare number | Took `b` | Why |
|---|---|---|---|
| **26** | speed-of-light-as-rotation-rate | `F26b`-bcc-spin-axis | 5 cites vs 2, **and** it is CLAUDE.md core decision 2. Half its citations read "Finding 26" rather than "F26" — ungreppable, so renaming it had unbounded cost |
| **101** | strong-coupling-sigma-compact-rotor | `F101b`-one-heavy-branch-fit-W | 2 vs 0 |
| **102** | coupled-rotors-crossover-survives | `F102b`-particle-layer-em-su3-backaction | 2 vs 0 (also the older by git-add date, the one pair where that differed) |
| **134** | unified-real-space-integration | `F134b`-phase4-chiral-blockspin | 2 vs 0; head of the F134–F137 arc |
| **174** | stellar-structure-overlay | `F174b`-shape-angle-2-9 | 1 vs 0 |
| **176** | saturation-self-duality-principle | `F176b`-covariant-dielectric-tov | cites tied 1–1, so **the internal date decided**: 2026-06-29 is older than 06-30 |
| **199** | angular-self-duality-derivation | `F199b`-amplitude-mode-stability | 3 vs 2. The collision most worth fixing — both files argue adjacent points in one derivation |
| **218** | algorithm-through-the-engine | `F218b`-alpha2F-firstprinciples | 3 vs 0 |

**Why `b` is better than a fresh number**, and why the F174 caution I raised earlier no longer applies: the suffix *keeps the number*. Every existing "F174" citation in the lepton-shape discussion still resolves, and `W_star`'s constants-registry provenance still names F101. Nothing had to be propagated.

Each renamed file carries a note under its heading saying it was renumbered at C8.2, so a reader who arrives by an old link is not left guessing.

### F136 — one rename, two collisions cleared

`F136-realspace-scalar-confinement.md` opened with `# F135 — Real-space confinement (U1)`: its *content* was F135 while its *filename* said F136. It is now **`F135b-realspace-scalar-confinement.md`**. No coin-flip was needed — the file's own content named its number, and the other F135 (`F135-blockspin-wavepacket-realtime.md`) was unambiguous. Result: `F136-colour-triplet-dirac-quark-confinement.md` is the sole F136, and the hidden F135 duplication is gone too.

### F200 — the one genuine tie, still yours

| File | Date | Cites |
|---|---|---:|
| `F200-eg-sextic-coupling-computed.md` | 2026-06-30 | 3 |
| `F266-sterile-neutrino-dark-matter.md` | 2026-06-30 | 3 |

Same commit, same internal date, equal citations. Neither rule picks a side, so I left it `unreviewed` rather than coin-flipping a physics number — `casim index` prints it on every run. They are cross-sector (lepton/strong E_g sextic coupling vs the F47 sterile-neutrino dark-matter relic), so context disambiguates in practice and the cost of leaving it is low. **One sentence from you closes it: which of the two becomes `F200b`.**

## F111 and F127 — the write-ups existed all along

You were right that there were tests and no findings. Searching for the three names found no finding file — but the write-ups were **inside the test docstrings**, complete with check tables and verdicts. Three finding files now record them, quoting the tests and adding no physics; each says plainly that the test remains the primary record.

| New file | Recovered from |
|---|---|
| `F111-second-order-light-deflection.md` | `test_F111_second_order_deflection.py` — $\alpha_2(\sigma) = \pi(2+\sigma)$; lattice $4\pi$ vs GR $15\pi/4$, excess $\tfrac{\pi}{4}\varepsilon^2$ |
| `F111b-tree-gauge-su3-ladder.md` | `test_F111_tree_gauge_su3_ladder.py` — 3D tree-gauge KS Hamiltonian + SU(3) Casimir ladder / character rotor |
| `F127-alpha-em-derivation-four-avenue-nogo.md` | `test_F127_alpha_em_derivation.py` — four routes to $\alpha$, all sharp negatives; the obstruction is the U(1) Ward identity $\Pi(0)=0$ |

`F111` keeps the bare number because S4's ledger record depends on its D3 check (it is why retiring `test_F114_dielectric_black_hole.py` at C7.6 lost no coverage). F127 is worth having visible: a no-go on the model's **last free dimensionless input** was absent from `findings-index.md`.

Two notes on what the recovery exposed. `F111b`'s baseline is one of the C7 close-out's **regression candidates** — a real run drifts with no supersession link — so the numbers in that file need a re-check before being quoted as current. And F127's avenue E (the $1/\alpha(\Lambda) = 64$ coincidence, 1.14% from experiment) is recorded as an *observation, not a derivation*, exactly as the test labels it.

## One check had to be refined

The nine resolutions immediately tripped the C8.2 stale-declaration check: it failed on "declares duplicate(s) that no longer exist", which is right for an abandoned exception and wrong for a **resolved** one — the entry *is* the record of the renumbering and should outlive the collision. `casim index` now exempts `status: resolved`. Finding that within a minute of resolving is the check working.

## Recorded as settled (no action)

- **F2–F15** — `accepted`: findings 1–15 predate the one-file-per-finding layout and live in `findings/F01-F15-findings.md`. Also why the inventory cites "Finding 1" rather than "F1".
- **F219, F229** — `resolved`: abandoned after collisions the changelog records; deliberately unused.
- **`F34b-wmu-mass-stueckelberg.md`** — accepted convention, and now the precedent for the eight new `b` files: `casim index` treats `34b` as its own key rather than folding it into 34.
