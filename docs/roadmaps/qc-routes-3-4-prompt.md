# Session prompt — QC empirical thread, Routes 3 & 4 (Bell/Tsirelson + intrinsic-decoherence floor)

*Hand this whole file to a fresh session working in the `Physics Notes` project. It is self-contained. Read `CLAUDE.md` first, then this.*

---

## Background you need

The quantum-computing cross-test thread is now complete as an **internal consistency** demonstration: the SU(2) cellular-automaton model *permits* QC (F212 perfect entangler), the entangler coupling is *derived* from `ca_dirac` hopping (F214: super-exchange $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, $U=2\arcsin m$), it *emerges* from genuine second quantization (F217), the substrate *runs* universal algorithms at scale (F218/F222), *on genuine matter* (F220), and it hosts noise + error correction (F221). Everything so far reproduces **textbook** QM/QI — necessary, but not yet a discriminating test against data.

Four routes were identified to make the thread empirically testable. Routes 1 (SI-anchor the super-exchange vs cold-atom data) and 2 (doublon leakage vs quantum-dot error budgets) are being executed in the originating session. **Your job is Routes 3 and 4** — the two routes that ask whether the discrete substrate leaves a fingerprint that continuum QM would not.

Key structural facts (verify against the repo, don't trust this blindly):
- Fundamental cell (F107/F123): $a=6.598\,\ell_P=1.06638\times10^{-34}$ m, $\tau=a/(c\sqrt3)=2.05366\times10^{-43}$ s, so the fundamental lattice is **Planckian**; the emergent low-energy world is many block-spin steps coarser.
- $c_\text{lat}=1/\sqrt3$ (F26); Lorentz-violating operators are RG-**irrelevant** under block-spin ($\lambda_n=b^{-n}$, F130).
- The interpretation is in the ’t Hooft cellular-automaton family (deterministic substrate); there is an existing CHSH test at `tests/**/test_02_QM1_CHSH.py` and the FC05 quantum-battery brief in `tests/falsification/`.

---

## Route 3 — Bell / Tsirelson: exactly QM, or a lattice correction?

**Question.** A deterministic CA substrate that reproduces QM must either (a) saturate Tsirelson’s bound $S_\text{CHSH}=2\sqrt2$ **exactly** — in which case loophole-free Bell experiments cannot discriminate it from QM and you must *say so plainly* — or (b) predict a small deviation $\delta S(a,E)$ from the discreteness, which is then testable against the existing loophole-free Bell data (Hensen 2015, Giustina 2015, Shalm 2015, and later BIG Bell / cosmic-Bell tests) that agree with QM to high precision.

**What to deliver.**
1. Compute the model’s CHSH value for the F212/F214 lattice singlet (the genuine $2^n$ register, *not* the hand-inserted product "singlet" flagged in the QM-1 test). Use the native measurement/rotor operators. Establish whether $S=2\sqrt2$ to machine precision or carries a correction.
2. If a correction exists, derive its scaling in the lattice spacing / measurement-angle discretisation (leading order in $a\cdot p$ or in the rotor-angle granularity), and turn it into a number or an upper bound.
3. Confront the result with published loophole-free Bell $S$-values and their error bars. State clearly whether the model is **Bell-indistinguishable** from QM (a defensible, honest outcome) or makes a falsifiable deviation.
4. Address the measurement-independence / superdeterminism question head-on: does the CA substrate rely on correlated settings, or does it reproduce the correlations with free settings? This determines whether Bell tests are even the right arena.

**Caution.** Do not overclaim a "violation" or a "beyond-QM" signal without an algebraically clean derivation. The most likely honest result is exact $2\sqrt2$ (⇒ not discriminating), which is itself a valuable, publishable statement.

---

## Route 4 — Intrinsic-decoherence / unitarity floor from discreteness

**Question.** If the lattice is physical, does a long quantum computation show any intrinsic departure from perfect unitarity — a minimum decoherence rate, a maximum entangling velocity (a Lieb–Robinson bound $=c_\text{lat}$), or a gate-error floor — set by $a$ and $c_\text{lat}$? F222 shows the register’s norm drift is pure floating-point ($10^{-13}$), i.e. the model currently asserts **no** intrinsic floor. Make that assertion quantitative and bound it against experiment.

**What to deliver.**
1. Derive the predicted intrinsic-decoherence / unitarity-violation rate as a function of $a$, $c_\text{lat}$, and the system energy/size. The expected answer is zero or Planck-suppressed — show which, and with what exponent.
2. Derive the model’s Lieb–Robinson / maximum-entangling-rate bound and confirm it equals $c_\text{lat}=1/\sqrt3$ in lattice units (this is the QC-sector analogue of the F180 GW-speed / signalling-speed results; reuse that machinery).
3. Confront the predicted floor with (i) collapse-model bounds — CSL, Diósi–Penrose — from the current literature, (ii) the observed coherence of real quantum processors and atomic clocks, (iii) neutron/atom interferometry decoherence limits. Show the predicted floor sits *below* current bounds (consistency) or, if not, flag the tension.
4. Tie in the F220 **doublon leakage** as the one *non-Planck-suppressed* native decoherence channel, and distinguish it (an emergent, material-scale effect) from any fundamental discreteness floor.

**Caution.** Keep "fundamental Planckian floor" and "emergent doublon leakage" strictly separate — they differ by ~30 orders of magnitude. Use the F107/F123 SI bridge for all dimensionful statements. Reuse F130 (LIV irrelevance) and F180 (signal speed) rather than re-deriving.

---

## Working rules (from CLAUDE.md — follow exactly)

- **Re-check finding numbers before writing.** Concurrent sessions are active; F215–F222 are taken. Grep `findings-index.md`, pick the next free `F{N}`, and note the collision-check in the finding header. These two routes likely become two findings.
- Algebraic exactness first, then machine precision. Prefer deriving over positing.
- **Search before asserting present-day facts** (collapse-model bounds, latest Bell results, current QC coherence numbers change — use web search).
- One markdown file per finding in `findings/F{N}-name.md`; a `test_F{N}_*.py` in `tests/findings/` writing JSON to `test-results/`; date-stamp `yyyy-mm-dd - hh:mm`.
- Beware numpy/scipy on chiral transforms (CLAUDE.md note); the entanglement/CHSH sector is plain complex linear algebra, so it’s safe, but assert unitarity/Hermiticity explicitly.
- Update `docs/status/changelog.md` and `docs/status/exactness-inventory.md`; run `python3 tools/regen_indexes.py` at the end.
- Escape literal `|` as `\|` in any table/finding title (Markdown-table gotcha).

## Definition of done

Two findings (Route 3, Route 4), each with a passing test and a JSON result, that answer the yes/no discriminating question honestly — including the fully-acceptable answer "indistinguishable from QM / Planck-suppressed below all current bounds, therefore this route does **not** yield a near-term test, and here is why." A clear verdict is the deliverable, not a manufactured signal.
