# Session prompt — derive the angular self-duality (C/|B| = 0.636)

**Created:** 2026-06-30 - (this session)
**Type:** Roadmap / session-starter prompt
**Predecessors:** F177 (honest terminus), F176, F175, F172, F150, F118, F96, F95, F92

---

## Paste-as-prompt

> You are the research assistant on the SU(2) cellular-automaton physics program (see `CLAUDE.md`). Your task this session is to attempt the **first-principles derivation of the angular self-duality** that F177 left as the honest terminus of the F174→F177 arc.
>
> **The one number to derive.** Produce, without fitting it and without *positing* the self-duality, the ratio of the two E_g Landau invariants of the second-shell condensate:
>
> $$\frac{C}{|B|}=\frac{1}{2\cos\tfrac23}=0.63622\quad\Longleftrightarrow\quad \cos3\delta^*=-\frac{B}{2C},\quad 3\delta^*=Q=\tfrac23\ \text{rad}.$$
>
> Equivalently: derive the sextic E_g clock self-coupling λ₆ (currently fitted at 0.243, F118) from the saturated condensate. B is already derived; the open object is C (= λ₆·e⁶), i.e. the angular half of the saturation self-duality.
>
> **Read first (targeted, not whole files):** F177 (the terminus and what BPS does/doesn't give), F176 (the 3δ=Q principle), F92 (the radial derivation whose *structure* you must imitate), F96 (the exact π/4 massless anchor and the two-value theorem), F95 (derived B, the C no-go), F118 (the self-consistent Mexican-hat (κ_E,c,W) solve and λ₆≈0.243), F145 (the induced-coupling/Fierz mechanism, c=2/9), F172 (the algebraic-vs-computed fork). Use `findings-index.md` to locate, then read only those files.
>
> **Constraint (project philosophy).** Algebraic exactness preferred, then machine precision. Do **not** introduce new physics to "close" the angle — if the solve forces a posit, that negative result is the deliverable. Beware numpy/scipy on chiral transforms (CLAUDE.md); use real arithmetic where possible.

---

## The derivation program (what to actually do)

### Step 0 — Reframe, don't start from scratch
The angular problem is **not** "find δ." It is "find the displacement of 3δ off the **exact π/4 anchor** (F96: Q=2/3 ⟺ 3δ=π/4 at mₑ=0) that mₑ>0 induces, and show it lands at 3δ = Q = 2/3 rad." Start every line of the solve from the F96 boundary condition.

### Step 1 — Build the second exact relation (the F92 analogue)
F92 derived the *radial* invariant because two independently-derived mass laws (pair-sum m=sin2t, bilinear m=y²) intersect at a unique angle (45°). The angular derivation needs the **same shape**: a second exact expression for 3δ, independent of "minimise the brake," that when set equal to the minimiser cos3δ*=−B/(2C) forces 3δ=Q. **Identify or rule out this second relation.** Without it the angle stays a one-equation/two-unknown fit. This is the conceptual core — spend the most effort here.

### Step 2 — The saturated-condensate induced-coupling solve (the deferred computation)
Compute C = λ₆·e⁶ from first principles, not by fit:
1. Take the saturated VEV e\* and the y_τ=1 wall from F118's self-consistent (κ_E, c, W) solution.
2. Integrate out the heavy binding exchange (dielectric / dual-Meissner gluon) and Fierz-project onto the E_g **sextic** invariant cos²3δ, reading λ₆ as (exact rational) × α_eff\* — the F145 machinery, carried two orders up from the validated quartic (c=2/9).
3. **The decisive algebraic question:** does α_eff\* (the IR coupling) **cancel in the ratio C/|B|** (since B also carries it)? 
   - If yes → 3δ=Q is an algebraic theorem, no nonperturbative number needed.
   - If no → C/|B| is a *computed* QCD-like value (F172's scale-residual fate). Report that as the terminus.

### Step 3 — Hunt for the mechanism (self-duality out, not in)
Standard Bogomolny fixes wall tension, not the vacuum angle (F177-B2). The angle is fixed only if the **BPS wall profile** δ′=±√(2W) and the **bulk minimiser** cos3δ*=−B/(2C) **coincide** — a marginal/degenerate condition that holds at exactly one C/|B|. Test whether the saturated condensate sits at that degeneracy, and whether it forces C/|B|=0.636. If so, the self-duality is *derived* as "angular budget saturates with the radial budget (y=1)" — F92's unitarity-filling reading, ported to the angle.

## Success / falsification criteria (both required)
- **Anchor recovery (necessary):** as mₑ→0 the solve must return 3δ→π/4 **exactly** (F96). Any mechanism that misses this is wrong regardless of its physical-point value.
- **Value discrimination (sufficient):** the self-dual 0.63622 and the transcendental competitor 2/π=0.63662 differ by 4×10⁻⁴; lepton ratios are reproduced to 0.007%. The solve must land to **≤10⁻⁴** and **predict which value**:
  - converges on 0.63622 → angular=radial self-duality confirmed;
  - converges on 0.63662 → a different (quadrant-averaging) mechanism;
  - converges off both → C/|B| is a genuinely computed nonperturbative number; self-duality must be posited, not derived (honest terminus).

## Hardest open step
The **sextic induced-coupling projection at saturation** (Step 2.2–2.3). F92/F95/F118/F150 all set up to it but never executed it. Everything else is existing scaffolding.

## Deliverables
- A new finding file `findings/F{next}-*.md` (check max F-number first — concurrent sessions; F177 is current). State outcome honestly: derived theorem, computed number, or forced posit.
- A test `tests/findings/test_F{next}_*.py` with the anchor-recovery and value-discrimination checks; results JSON in `test-results/`.
- `docs/status/changelog.md` one-paragraph entry; update `docs/status/exactness-inventory.md`.
- Run `python3 tools/regen_indexes.py` at the end.

## One-line framing
*Derive λ₆ (= C/|B|) from the saturated E_g condensate by carrying F145's induced-coupling Fierz projection up to the sextic; the whole result turns on whether α_eff\* cancels in the ratio and whether the wall/bulk degeneracy lands at 0.63622 — with the F96 π/4 anchor as the boundary condition and the 0.63622-vs-2/π split as the falsifiable discriminator.*
