# F362 — Fluctuation corrections to F130's confinement eigenvalue do **not** move it off $b^1$ under F130's own bond-moving convention ($g^2\to bg^2$, $\lambda$ held fixed): every order of that expansion carries an exact integer eigenvalue, the composite "effective" exponent this route can define is scheme-dependent (not universal), and the model's own calibrated coupling sits two decades past the expansion's validity radius — a genuine Migdal–Kadanoff treatment that lets $\lambda$ flow under decimation is a different, untested route (see Prior art, §4a)

**Date:** 2026-09-04 - 02:45
**Numbering:** **F362**, taken as `NEXT FREE NUMBER` (max+1, no gaps). Session `cowork-k3-blockspin-fluctuation`, sector `interactions`.
**Status:** Confirmed — **4/4 checks PASS**, two declared controls each verified to redden exactly the leg they target and no other.
**Checked:** 2026-09-04 — 6 PASS / 5 WEAKENS / 2 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**
**Module:** `casim.engine.interactions.cosmology_blockspin_fluctuation` (`src/casim/engine/interactions/cosmology_blockspin_fluctuation.py`)
**Test:** registry record `F362-blockspin-fluctuation-eigenvalue` (`tests/registry/interactions.yaml`, `entry: run_all`, tier **gate**)
**Results:** `test-results/F362_blockspin_fluctuation.json`
**Executes:** `docs/status/open-derivations.md` row **G2**'s own suggested attack, verbatim: *"compute the block-spin relevant eigenvalue WITH FLUCTUATION CORRECTIONS on F130's existing machinery, and see whether it moves off $b^1$ by 1.6%."* Also `docs/status/completeness-2026-08-20-prompts.md`'s K3 prompt (shared with **K12**, same operator).
**Answers (negatively):** [[F310-gamma-is-a-blockspin-eigenvalue]] falsifier 1 / `docs/claims/CL267-tilt-is-a-blockspin-eigenvalue.md` falsifier 2 — *"a block-spin computation with fluctuation corrections that still returns exactly $\lambda_\sigma=b^1$."* **This is that computation, and that is what it returns** — with a mechanism, not a null.
**Cross-references:** [[F130-blockspin-rg-gauge-gravity]] (C1, the $\lambda=0$ leading-order eigenvalue $\lambda_\sigma=b$ this extends, and `magnetic_deformation_ratio`'s own $b^{-2}$ measurement, reproduced here as a limiting case), [[F310-gamma-is-a-blockspin-eigenvalue]] (the identity $\gamma\equiv y-1$ this residual belongs to), [[F295-tilt-is-an-anomalous-dimension-not-a-second-scale]], [[F296-holographic-cosmology-names-the-operator-and-validates-T1]], [[F285-initial-condition-measure-cannot-tilt]] (untouched), [[F101-strong-coupling-sigma-compact-rotor]] (the $\lambda=\chi\Omega^2$, $\chi=1$ mapping and the model's own $\Omega$ values used in §5), [[F110-realtime-link-hamiltonian-confinement]] / `casim.engine.gauge.link_hamiltonian` (`sigma_strong_pt2`, the exact strong-coupling PT machinery this reuses read-only), F115/F325 (the locked $g_s^2=\tfrac14$ used in §5).

Raised by Ben, 2026-09-04, via the prompt handed to this session (open-derivations G2 / rubric K3, shared with K12).

---

## 1. The question

F130 C1 computed the confinement (string-tension) block-spin eigenvalue at $\lambda=0$ — the **frozen** flux tube, no plaquette fluctuations at all: $\hat\sigma=g^2/2$ exactly, and bond-moving ($g^2\to b\,g^2$) gives the exact integer $\lambda_\sigma=b$. F310 identified this as *why* every earlier route to G2/K3's non-integer $\gamma$ failed: an anomalous dimension is a non-integer RG exponent, and $\lambda_n=b^{-n}$-type results from a **linear** (Gaussian) block average cannot produce one. The ledger's own next step, and F310's own falsifier 1, is direct: turn $\lambda$ back on — add the fluctuation correction the frozen limit deliberately dropped — and see whether the eigenvalue moves.

The repo already owns the machinery to do this exactly, not approximately: `link_hamiltonian.sigma_strong_pt2` computes the second-order strong-coupling perturbation-theory correction to $\hat\sigma$ with **exact integer arithmetic in its energy denominators** (Z₃ Kogut–Susskind Hamiltonian, dense diagonalisation). This finding composes that machinery with F130's own bond-moving rule and asks the ledger's question directly.

## 2. C1 — the closed form, verified against the repo's own exact solver

$$\hat\sigma(g^2,\lambda) = \frac{g^2}{2} - c_2(g^2)\,\lambda^2 + O(\lambda^4),\qquad c_2(g^2)=\frac{1}{6g^2}\ \text{exactly}$$

The $1/(6g^2)$ closed form is not assumed — it is read off `sigma_strong_pt2` at five values of $g^2\in\{0.25,0.5,1,2,4\}$ on a genuine `PlaquetteGrid` diagonalisation, and $c_2(g^2)\cdot g^2 = 1/6$ agrees at every point to the floating-point floor ($<4\times10^{-16}$). This one relation is the finding's entire empirical input; everything after this section is exact algebra on it.

## 3. C2 — every order of the expansion is an exact integer eigenvalue (generalises F130 C3/C4)

Bond-moving with $\lambda$ held fixed (F130's own convention — the same one `magnetic_deformation_ratio` uses to establish that $\lambda$ is irrelevant) sends $g^2\to b g^2$. Strong-coupling PT builds $\hat\sigma$ as a series in **plaquette-flip order** $n$; each term is fixed by dimensional analysis of its energy denominators to scale as

$$\text{term}_n(g^2,\lambda) = a_n\,\lambda^{2n}\,(g^2)^{1-2n}\qquad\Longrightarrow\qquad \text{term}_n(bg^2,\lambda)/\text{term}_n(g^2,\lambda) = \boxed{b^{\,1-2n}}$$

sympy-exact for every $n$. $n=0$ is F130's leading term, eigenvalue $b^{+1}$ (relevant). Every $n\ge1$ term is **irrelevant**, at an **integer** eigenvalue $b^{-1},b^{-3},b^{-5},\dots$ — never anything in between. This is checked against the repo's own independent measurement: the $n=1$ term's eigenvalue **relative to the leading term** is $b^{1-2}/b^{1}=b^{-2}$, which is exactly the ratio `blockspin.magnetic_deformation_ratio` already reports ($r_\text{coarse}/r_\text{fine}\to b^{-2}$) — reproduced here to $<2\%$ at $b=2,3,4$ in the small-$\lambda$ limit (module `check_c2_power_counting`).

**Under F130's own bond-moving convention — $g^2\to bg^2$ with $\lambda$ held exactly fixed — no finite order, and no convergent sum of them, can contribute a non-integer piece to the leading term.** This is the precise generalisation of F130 C3/C4's *"a linear block average is a Gaussian calculation and cannot produce a non-integer exponent"* to that same convention — it was never special to the linear (zeroth) order; it is a property of the **entire** strong-coupling expansion around $\lambda=0$ evaluated **this way**, because every term in that expansion is, by the same dimensional analysis that fixes the leading one, an integer power of $b$. This is a statement about the convention F130 C1 established (rescale $g^2$ alone, freeze $\lambda$), not a scheme-independent fact about all possible block-spin transformations of this Hamiltonian — see §4a.

### 3a. The small-$\lambda$ cross-check's residual is $O(\lambda)$, not $O(\lambda^2)$ — investigated, does not change the conclusion

The review pass on this finding flagged that `check_c2_power_counting`'s docstring mischaracterised
its own residual as "finite-lambda $O(\lambda^2)$ corrections" (i.e. attributed to the *next* term of
the truncated series). Re-running the cross-check at a third, smaller $\lambda$ (0.0025, 0.00125, in
addition to the finding's own 0.005, 0.01) settles this: at every $b\in\{2,3,4\}$ the ratio of
successive relative errors converges cleanly to $2.00$ as $\lambda\to0$ (e.g. $b{=}2$:
$2.015\to2.008\to2.004\to2.002$), not to $4.00$. A residual that halves when $\lambda$ halves is
$O(\lambda^1)$, not $O(\lambda^2)$.

That is real physics, not an artifact: `magnetic_deformation_ratio` measures the actual (non-
perturbative) ground state, and the standard strong-coupling argument that kills the linear-in-$\lambda$
term for the *vacuum* energy (the plaquette operator $\cos\hat\varphi_p$ changes flux sector, so its
diagonal matrix element vanishes in the vacuum) does not obviously apply to the *flux-tube* ground
state used to define $\hat\sigma$: a plaquette flip adjacent to the string can locally deform it
without changing its winding class, so a genuine first-order matrix element can survive there. This
module's `sigma_hat_2nd_order` never claimed to include that term — it is exactly what
`sigma_strong_pt2`'s own docstring scopes as the *second-order* coefficient — so its absence is not a
defect in the closed form checked in §2 (C1 compares like for like, to the float floor). It **is** a
defect in how §3's cross-check explained its own $2\%$ tolerance margin, now corrected here.

Does an $O(\lambda)$ term change §3's central claim? Under the *same* power-counting convention used
there (a term $\propto\lambda^{k}(g^2)^{1-k}$ carries eigenvalue $b^{1-k}$ under $g^2\to bg^2$,
$\lambda$ fixed), $k=1$ gives eigenvalue $b^{0}=1$ — **marginal, and still an integer power of $b$.**
So a real linear-order term, under this specific convention, does not supply a non-integer piece
either; it strengthens the pattern (odd order too) rather than breaking it. It is not, however,
computed or controlled anywhere in this module — `check_c2_power_counting`'s $2\%$ tolerance is
honestly attributable to it now, not to a higher even order, and no claim in §2–§4 rests on the
$O(\lambda^2)$ mischaracterisation that has been removed.

## 4. C3 — the composite "effective" exponent this route *can* define is not universal

Compose the truncated formula with bond-moving into a ratio and a log-exponent anyway, at one finite blocking factor $b$:

$$\text{ratio}(g^2,\lambda,b)=\frac{\hat\sigma(bg^2,\lambda)}{\hat\sigma(g^2,\lambda)},\qquad y_\text{eff}=\log_b(\text{ratio}),\qquad \gamma_\text{eff}=y_\text{eff}-1.$$

In the dimensionless variable $\varepsilon\equiv\lambda^2/(3g^4)$ (the ratio $\Delta\hat\sigma/\hat\sigma(0)$ at $b=1$; sympy-verified $g^2$ cancels identically), the exact closed form is

$$\text{ratio}(\varepsilon,b) = \frac{b^2-\varepsilon}{b(1-\varepsilon)}.$$

Two things follow, both checked numerically (module `check_c3_universality`, `universality_scan`):

1. **As $b\to\infty$ at any fixed $\varepsilon$, $\gamma_\text{eff}\to0$.** $\gamma_\text{eff}\sim\varepsilon(1-b^{-2})/\ln b\to0$ — the asymptotic (true RG fixed-point) eigenvalue is exactly $b^1$, consistent with C2: an irrelevant correction, by construction, cannot survive to the scaling limit.
2. **At any *finite* $b$, $\gamma_\text{eff}$ is not $b$-independent — and a real critical exponent must be.** Tuning $\varepsilon$ so that $\gamma_\text{eff}(b{=}2)=0.015$ (the G2/K3 target's midpoint) gives $\gamma_\text{eff}=0.0112$ at $b=3$, $0.0094$ at $b=4$, $0.0083$ at $b=5$ — a fractional spread of $30$–$82\%$ across $b\in\{2,\dots,5\}$ at *every* tuning tried (table below). A genuine anomalous dimension is a **scheme-independent** number; this quantity depends explicitly on which $b$ you used to define one coarse-graining step, which is definitionally not that.

| tuned at $b$ | $\gamma_\text{eff}(2)$ | $\gamma_\text{eff}(3)$ | $\gamma_\text{eff}(4)$ | $\gamma_\text{eff}(5)$ | fractional spread |
|---|---:|---:|---:|---:|---:|
| 2 | 0.0150 | 0.0112 | 0.0094 | 0.0083 | 45% |
| 3 | 0.0201 | 0.0150 | 0.0125 | 0.0111 | 60% |
| 4 | 0.0240 | 0.0180 | 0.0150 | 0.0132 | 72% |
| 5 | 0.0273 | 0.0204 | 0.0170 | 0.0150 | 82% |

**This is the decisive structural point, independent of any coupling value.** Even setting aside whether the model's own $(g^2,\lambda)$ is in a trustworthy regime (§5), the object this route computes cannot be identified with $\gamma$, because $\gamma$ is one number and this is a family of numbers indexed by an arbitrary choice of $b$.

### 4a. Prior art and scope — this is Migdal–Kadanoff bond-moving with $\lambda$ frozen, not full Migdal–Kadanoff RG

F130 C1's convention — parallel-compose $b$ fine links into one coarse link ($g^2\to bg^2$) while
leaving every other coupling in the Hamiltonian untouched — is a genuine, standard building block of
real-space RG for lattice gauge theories (the "bond-moving" half of the classic
Migdal–Kadanoff scheme), but it is only half of it. The full Migdal–Kadanoff prescription pairs
bond-moving with **decimation** (integrating out the moved links via the character expansion), and
the character-expansion coefficients this generates are new functions of *all* the couplings present
— for a theory with both an electric ($g^2$) and a magnetic/plaquette ($\lambda$) term, standard
treatments of this construction — *Renormalization group equations in lattice gauge theories*, Nucl.
Phys. B (1978), https://www.sciencedirect.com/science/article/abs/pii/0550321378902821 , and *Migdal–
Kadanoff recursion relations in SU(2) and SU(3) gauge theories*, Nucl. Phys. B (1981),
https://www.sciencedirect.com/science/article/abs/pii/0550321381904910 — let **both** couplings flow, and can mix in couplings to
higher group representations that were not present in the starting Hamiltonian at all. This finding's
route never performs that decimation step: it holds $\lambda$ exactly fixed and only asks how the
*truncated series in that fixed $\lambda$* transforms when $g^2$ alone is bond-moved — which is
F130 C1's own convention, reused unmodified, not a re-derivation of a full RG step.

**What this means for §3/§6's claim.** "Every finite-order term carries an integer eigenvalue" is
established here for *this* convention — freeze $\lambda$, bond-move $g^2$ — and that is what
`term_eigenvalue`/C2 compute and what `check_c2_power_counting` verifies against real dynamics
(§3a). It is not shown, and this finding does not attempt to show, what happens to the eigenvalue
spectrum under a decimation step that lets $\lambda$ flow and mix into new representations — that is
a structurally different (and substantially harder) calculation, and remains an open route, not one
this finding has closed. §9's "what would falsify this" is written narrowly for exactly this reason.

## 5. C5 — and the model's own coupling is nowhere near where any of this could be trusted

The model's calibrated confinement point is $g_s^2=\tfrac14$ (locked at the BZ edge, F115/F325) with $\lambda=\chi\Omega^2=\Omega^2$ ($\chi=1$, F101). F101 §5 quotes $\Omega\approx1.3$ (a representative mid-zone value) and separately notes *"the data wants $\Omega=0.997829$"*. At **either** value:

| $\Omega$ | $\lambda=\Omega^2$ | $\varepsilon=\lambda^2/(3g^4)$ | perturbative ($\varepsilon\ll1$)? |
|---|---:|---:|---|
| $1.3$ | $1.690$ | $15.23$ | **no** — 76$\times$ over |
| $0.997829$ | $0.996$ | $5.29$ | **no** — 26$\times$ over |

$\varepsilon\sim5$–$15$ is one to two decades past the truncation's radius of validity ($\varepsilon\ll1$ required for an $O(\lambda^2)$ series to mean anything). Concretely, $\hat\sigma(g_s^2,\Omega^2)$ evaluated from the truncated formula is **negative** ($-1.78$ at $\Omega=1.3$) — an unphysical string tension — and the coarse/fine ratio goes negative (undefined $\log$) for $b\ge4$ at $\Omega=1.3$ and $b\ge3$ at $\Omega=0.997829$. The model's own physical point is not merely "not exactly matching the target" — the calculation this route performs breaks down entirely there.

## 6. Verdict

> **Adding the fluctuation correction F130's $\lambda=0$ leading order dropped does not move the confinement eigenvalue off $b^1$ under F130's own bond-moving convention ($g^2\to bg^2$, $\lambda$ held fixed) — and within that convention it structurally cannot.** Every order of the strong-coupling expansion around $\lambda=0$, evaluated this way, carries an exact integer eigenvalue $b^{1-k}$ (C2, extended to odd $k$ in §3a) — the *whole* series, not just its leading (Gaussian) term, extending F130 C3/C4's own explanation for why every earlier route failed. The one composite quantity this expansion *can* define at a finite blocking step is not $b$-independent (C3) — it fails the basic definition of a universal critical exponent regardless of coupling — and the model's own calibrated coupling sits two decades past this whole expansion's validity radius, where the truncated string tension is outright unphysical (C5). This is F310's own falsifier 1 firing, exactly as named: *"kills the whole route ... and is worth as much"* as a positive result. It closes the SPECIFIC route open-derivations G2 pointed at — bond-moving with $\lambda$ frozen — and narrows what a successful one would need: either a genuinely **non-perturbative** RG treatment of the confinement sector at fixed $\lambda$ (a real fixed point away from $\lambda=0,\infty$ with its own non-integer eigenvalue, or a resummation rather than a truncation), or a full Migdal–Kadanoff decimation step that lets $\lambda$ itself flow and mix into new couplings (§4a) — not a higher term of the same fixed-$\lambda$, $\lambda=0$ expansion.

## 7. What this does *not* touch

**F310's C1–C8 stand untouched.** The operator identification $\gamma\equiv y-1$, the all-integer F130 spectrum this finding's C2 reinforces (not merely repeats — it now covers the whole strong-coupling series, not only the reported eigenvalues), the $n_t=2$ tensor prediction, and the critical-measure hypothesis are unaffected; this finding closes one specific candidate *mechanism* for supplying $\gamma$, not the identification itself. **F285/F286/F296 are untouched** (not re-attacked, per the prompt's explicit instruction). **The $1/N$ route (F310 C8) is untouched and still not re-entered** — it remains a labelled, un-adopted coincidence check, unrelated to this finding's route.

**What is now open.** G2/K3/K12's residual reverts to: no in-repo mechanism currently supplies $\gamma$. A future attempt needs either (a) a genuine non-perturbative fixed point of the confinement RG distinct from $\lambda=0,\infty$ (this finding says nothing about whether one exists — only that a perturbative expansion around $\lambda=0$ cannot reach it), or (b) a route outside the confinement sector entirely (F130's other four measured eigenvalues — $c_\text{lat}$, the two LIV classes, gravity discretisation — are *also* all-integer per F130 §3/§7, and this finding's C2 argument applies to any of them built the same way, i.e. as a finite-order expansion around an exactly-solvable linear point; none is flagged as a live candidate here, only noted as sharing the same structural obstruction).

## 8. What is exact vs. computed vs. open

| Piece | Status |
|---|---|
| $c_2(g^2)=1/(6g^2)$ | **exact** (closed form, matched to `sigma_strong_pt2` at 5 points to the float floor) |
| $\text{term}_n$ eigenvalue $=b^{1-2n}$ | **exact** (dimensional/power-counting identity) |
| $n=1$ relative eigenvalue $=b^{-2}$, matches `magnetic_deformation_ratio` | **exact** (identity) + **quantitative** (cross-check, $<2\%$ at small $\lambda$) |
| Cross-check residual is $O(\lambda)$, not $O(\lambda^2)$ (verified to $\lambda=0.00125$); consistent with a marginal ($b^0$) term under the same convention | **quantitative** (investigated, §3a) |
| $\gamma_\text{eff}\to0$ as $b\to\infty$ at fixed $\varepsilon$ | **exact** (closed-form limit) |
| $\gamma_\text{eff}$ is $b$-dependent (non-universal) | **quantitative** (30–82% spread, tabulated) |
| Model's $\varepsilon\sim5$–$15$, non-perturbative | **computed**, on cited $g_s^2$/$\Omega$ values (F115/F325/F101) |
| **Whether a non-perturbative confinement fixed point exists with a non-integer eigenvalue** | **open — not attempted here** |

## 9. Honest scope

**This is a negative result about one specific route, not a no-go for G2.** It shows a perturbative expansion around F130's $\lambda=0$ point cannot produce $\gamma$; it does not show no mechanism in the model can. The ledger's framing (F310 falsifier 1) explicitly anticipated and priced this outcome as valuable.

**The universality argument (§4) is the load-bearing one**, not the numerology of §5. Even a model recalibration that moved $g_s^2$ or $\Omega$ into the perturbative regime would not rescue this route, because the $b$-dependence of $\gamma_\text{eff}$ is a property of the truncated series' functional form, not of where it is evaluated.

**Higher orders ($\lambda^4$, $\lambda^6$, …) are not computed here** — C2's argument is that they don't need to be: the power-counting is general (every $n$), and no order changes the leading term's eigenvalue. A resummation to all orders is a different, harder object than "the next term," and this finding does not attempt one.

**What would falsify this finding specifically (narrower than F310's falsifier 1).** F310's falsifier 1 is stated at the level of "a block-spin computation with fluctuation corrections that still returns exactly $\lambda_\sigma=b^1$" — this finding is one such computation, restricted to F130's fixed-$\lambda$ bond-moving convention, and it is the one that fired. It would be over-narrow to read F310's falsifier as requiring, from here on, a single fully non-perturbative computation that is simultaneously non-integer *and* $b$-independent: an intermediate result — a genuine Migdal–Kadanoff decimation step (§4a) that lets $\lambda$ flow, even carried out only perturbatively in the new mixed couplings — would already fall outside what this finding rules out, and would be a legitimate next attempt at the same target, not a repeat of this one.

**A minor, inherited note, not a claim of this finding.** F310's target range ($\gamma=0.0136$–$0.0176$) is quoted unchanged here. A newer DESI+CMB "SPA" combination reported after F310 was written gestures toward a slightly lower central value ($\gamma\approx0.0132$, below F310's own floor) — whether that changes the target range is F310's/K3's bookkeeping, not something this finding's negative result depends on either way.

## 10. Files
- Module: `src/casim/engine/interactions/cosmology_blockspin_fluctuation.py`
- Test: registry record `F362-blockspin-fluctuation-eigenvalue` (`tests/registry/interactions.yaml`, tier gate, `entry: run_all`, 4/4 checks PASS)
- Results: `test-results/F362_blockspin_fluctuation.json`
- Controls: both verified **CONTROL** 2026-09-04 (`wrong_c2_sign` reddens exactly C1; `wrong_power` reddens exactly C2; neither disturbs the other legs)

## Reviewed & corrected

**2026-09-04 - 14:10** — attack pass: **CONFIRMED-NARROWER** (cold `general-purpose` subagent,
13-attack review-finding protocol; independently re-derived C1's closed form and C3's ratio formula
in its own sympy session, confirming both exactly). Found: the central claim overclaimed scope —
"structurally cannot" and "property of the entire strong-coupling expansion" read as scheme-
independent RG facts, but the result is specific to F130's own bond-moving convention (g2 -> b*g2,
lambda held fixed), not a statement about all possible RG treatments of this Hamiltonian; a real
Migdal-Kadanoff decimation step lets couplings mix and was never tested (attack 10 + the requested
"central logical move" stress test). Separately, a genuine numerical anomaly: `check_c2_power_counting`'s
small-lambda residual scales as O(lambda), not the O(lambda^2) its docstring claimed (attack 12).
Fixed: narrowed the title, Sec 3, Sec 6 verdict, module docstrings and CL300's statement/falsifier
to the F130 fixed-lambda convention explicitly; added Sec 4a (prior art: Migdal-Kadanoff recursion
relations for lattice gauge theories, with citations, and what this route does not test); added
Sec 3a, independently reproducing the O(lambda) residual myself (re-ran `check_c2_power_counting`
at lambda=0.0025 and 0.00125 in addition to the finding's own two points; the ratio of successive
relative errors converges to 2.00, not 4.00, at every b in {2,3,4}) and explaining it physically —
real, not an artifact, and (under the same fixed-lambda convention) an integer (b^0, marginal)
eigenvalue itself, so it does not change Sec 3/Sec 6's conclusion but does correct the check's own
docstring, which was wrong about why its 2% tolerance holds; softened Sec 9's falsifiability
language and CL300's falsifier so an intermediate Migdal-Kadanoff-with-flowing-lambda result would
count, rather than requiring one computation to be simultaneously non-integer and b-independent from
a fully non-perturbative treatment (attack 13); added a one-line inherited-target note on the newer
DESI+CMB-SPA n_s combination (attack 6, F310's bookkeeping, not this finding's claim). Rejected: none
outright — attacks 3 and 8 (exactness inflation on "every order n" language; the perturbativity
threshold's slack at the physical point) were judged already adequately scoped/documented (the n>=2
power-counting is a dimensional-analysis identity, not an extrapolation needing its own control; the
threshold's margin at the physical point is 26-76x, not marginal) and are recorded here rather than
silently dropped. Deferred: none — no fix required touching CLAUDE.md Core Design Decisions or
`supersessions.yaml`, so no hard-verdict escalation was triggered.
