# Structural test: the Alcubierre warp metric in the lattice model

**Date:** 2026-06-30 - 20:06
**Type:** structural-consistency test prompt (not a Tier A/B/C falsification brief — there is no measured datum to confront; the question is whether a *known GR solution* can be realized by the model's own beable/lattice constraints). Hand this whole file to a sub-agent or a future session as a self-contained brief: it carries the hypothesis, the model commitments it is tested against, a first-pass verdict, and the CASIM/symbolic work needed to promote that verdict to a finding.
**Cross-references:** [[F178-gravity-full-tensor-adoption]], [[F181-covariant-interior-kernel-battery]], [[F193-ontic-vacuum-gravitates-as-zero]], [[F64-em-connection-gravity]], [[F79-structural-newton-constant]], [[F107-canonical-a-adoption-L4-grb-gate]], [[F69-paired-spinor-photon]]; brief `FA01` (LIV bound on lattice signal speed).

---

## 1. Hypothesis under test

Can the Alcubierre warp-drive metric — or any member of its family (Natário zero-expansion, Bobrick–Martire subluminal solitons, Lentz solitons, Fuchs et al. 2024 constant-velocity drive) — be realized as an actual field configuration on this model's BCC lattice, given what the model has already derived about how its gravity sector is sourced?

This is **not** asking "does GR admit the Alcubierre metric" (it does, trivially — any metric solves $G_{\mu\nu}=8\pi T_{\mu\nu}$ for *some* $T_{\mu\nu}$). It is asking whether the **required** $T_{\mu\nu}$ is the kind of object this model's lattice can actually produce, given that here gravity is not free-standing geometry but an **induced** field sourced by **beable** (actual, per-cell, non-negative) matter content (F178, F193).

## 2. The standard-physics baseline (for calibration)

The Alcubierre metric,
$$ds^2 = -c^2dt^2 + \big(dx - v_s(t)\,f(r_s)\,dt\big)^2 + dy^2 + dz^2,$$
with $f$ a smooth bump function (1 inside the bubble, 0 outside) and $v_s$ the bubble's coordinate velocity, was shown by Alcubierre (1994) to permit $v_s>c$ for an Eulerian observer outside the bubble while every local worldline inside it remains timelike. The known costs, established in the literature this model should be checked against:

- **Energy condition violation.** The required $T^{00}$ is negative in a thin wall around the bubble — first shown by Alcubierre and sharpened by Pfenning & Ford (1997), "[The unphysical nature of 'warp drive'](https://arxiv.org/abs/gr-qc/9702026)."
- **Quantum-inequality bound.** Ford & Pfenning's QI analysis restricts the negative-energy region to a sampling time of order the bubble-wall light-crossing time; for the original Alcubierre wall this is $\sim10^{-33}\,\text{s}$, and the integrated negative energy needed exceeds the mass-energy of the visible universe by roughly $10^{11}\times$. The Natário (zero-expansion) variant relaxes the sampling-time bound to $\sim10^{-10}\,\text{s}$ but does not remove the sign problem ([Ford–Pfenning QI on the Natário drive](https://hal.science/hal-00734603v2/document)).
- **2021–2025 "positive-energy" program.** Bobrick & Martire (2021, "[Introducing Physical Warp Drives](https://arxiv.org/abs/2102.06824)") reclassified warp drives generally and showed the *subluminal* members of the family can in principle be sourced by ordinary positive-energy matter — at the cost of giving up faster-than-light transport. Lentz (2021) proposed superluminal positive-energy solitons; this is contested, and a 2025 re-analysis ("[Violations of the Weak Energy Condition for Lentz Warp Drives](https://www.researchgate.net/publication/397934716_Violations_of_the_Weak_Energy_Condition_for_Lentz_Warp_Drives)") finds WEC violation persists once the full stress tensor is checked. Fuchs et al. (2024, Applied Physics/UAH, using the open "Warp Factory" toolkit) constructed a **constant-velocity, subluminal, all-energy-conditions-satisfied** warp metric — but it is explicitly capped below $c$ and carries no FTL utility.

**Net standard-physics state:** every metric in this family that is genuinely *superluminal* still requires negative energy density somewhere in its source tensor; every metric that satisfies all energy conditions with ordinary matter is *subluminal*. This trade-off is the literature's current floor, independent of this model.

## 3. Model elements the test is run against

| # | Commitment | Source | What it constrains |
|---|---|---|---|
| M1 | Gravity = induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, full tensor, canonical | F178 | The metric is not freely specifiable; it is solved *forward* from an actual matter/field configuration, never posited and then back-solved for whatever $T_{\mu\nu}$ is needed. |
| M2 | $T^{00}$ is a **beable**: diagonal, real, $|\psi(\mathbf x)|^2\times(\text{rotation weight}) \ge 0$ at every cell, with no additive $c$-number / zero-point term | F193 (A2) | **Local energy density on the lattice cannot be negative.** The $+\tfrac12\hbar\omega$ zero-point piece exists only in the template (Fock) description and is explicitly a *superimposable*, not a beable — it does not source $K$ or $G_{\mu\nu}$ at all, positively or negatively. |
| M3 | The two-function interior kernel ($A,B$ independent, $AB\neq1$) is the canonical strong-field/interior solver; it reproduces GR-TOV and isotropic perfect fluids exactly | F181 | The model *can* represent generic (including anisotropic) stress-energy geometrically — the obstruction is not "the kernel can't carry exotic $T_{\mu\nu}$," it's "the lattice can't *produce* the sign such a $T_{\mu\nu}$ needs (M2). |
| M4 | $c_\text{lat}=1/\sqrt3$ is the hard angular-rotation-rate bound of the substrate (Finding 25/26, `CLAUDE.md` §Core Design Decisions #2); no lattice update propagates information faster | F26/F79/F107, LIV bound `FA01` ($E_\text{QG,2}=1.36\times10^{19}$ GeV, subluminal $n=2$) | Any construction requiring superluminal *local* signal propagation (as opposed to superluminal *coordinate* separation via metric engineering) is excluded outright — this is a harder, structural version of the usual SR objection, because here $c_\text{lat}$ is a literal per-tick update rule, not just a Lorentz-invariance postulate. |
| M5 | Vacuum is ontologically the single state $\psi\equiv0$; $H\,0=0$ exactly | F193 (A1) | There is no fluctuating "quantum vacuum" reservoir of beable energy to draw on — ruling out Casimir-style sourcing (see §5). |

## 4. Structural analysis

**4.1 — The metric-engineering direction is inverted relative to the model.** Alcubierre's method, and every variant in §2, is to *posit* the metric (the bump function $f$, the velocity $v_s$) and *solve for* the $T_{\mu\nu}$ Einstein's equations demand. M1 forbids this order of operations as a *fundamental* procedure here: the model's $G_{\mu\nu}$ is induced from an actually-existing field configuration (F64's enclosed-mass $K$, F178's full-tensor source). This doesn't make the Alcubierre metric meaningless in the model — it can still be evaluated as a *target* geometry — but it reframes the question correctly: not "is this metric consistent with $G_{\mu\nu}=8\pi T_{\mu\nu}$" (it always is, for the $T_{\mu\nu}$ GR computes), but "does any beable field configuration on the BCC lattice produce that $T_{\mu\nu}$." That is a much harder, model-specific bar.

**4.2 — The required $T^{00}<0$ region is structurally unreachable.** This is the sharp result. Pfenning–Ford and every subsequent superluminal variant (Alcubierre, Natário, the contested Lentz solitons per the 2025 re-analysis) require a region of negative $T^{00}$ in the bubble wall. M2 (F193, derived — not posited) states the model's beable energy density is a sum of non-negative quadratic terms with no sign-flipping term available at the ontological level. This is a **strictly stronger** prohibition than the standard QFT one: ordinary QFT *does* permit local negative energy density (Casimir effect, squeezed vacuum states), bounded only by the Ford–Roman quantum inequalities. This model's own F193 result removes that channel entirely at the level of what *gravitates* — the zero-point/fluctuation piece is explicitly not a beable, hence cannot source $K$ or $G_{\mu\nu}$ even when present in the template description (M5). **Conclusion: the superluminal members of the warp-drive family (Alcubierre, Natário, contested-Lentz) are excluded in this model on stronger grounds than in mainstream GR+QFT — not merely "energetically prohibitive" but "the sourcing mechanism does not exist."**

**4.3 — The subluminal, positive-energy members (Bobrick–Martire general class; Fuchs et al. 2024 constant-velocity drive) are the only candidates not immediately excluded by M2.** These use only $T^{00}\ge0$, so they don't trip the beable non-negativity bound. They would instead need to be checked against M1/M3/M4: can a beable configuration that produces the required (positive but still anisotropic/superluminal-adjacent flow) stress tensor actually be constructed and does its forward-solved metric under F181's two-function kernel reproduce the target bubble geometry? This is open — it has not been attempted — and is the one branch worth real CASIM time (§6). Note the obvious caveat: subluminal warp drives have no FTL payoff, so a positive result here is a statement about the model's flexibility for *exotic-but-physical* metric engineering (relevant to, e.g., inertial-shielding or acceleration-cancelling geometries), not about faster-than-light travel.

**4.4 — Even a hypothetical superluminal *coordinate* solution collides with M4.** Independent of the energy-condition problem, the warp-bubble mechanism relies on the metric itself (not local matter) carrying the ship FTL relative to Eulerian observers far away — a move that exists in continuum GR because the metric is dynamical independent of any propagation speed limit on matter fields. On this lattice, the metric is **not** an independently dynamical object; it is read off the induced $K$ / two-function kernel sourced by $T_{\mu\nu}$, which is itself built from fields obeying the $c_\text{lat}$ update rule (M4). It is not yet established whether an induced-gravity construction of this kind can support a non-trivial *shift vector* (the $-v_s f(r_s)$ term) at all in the regime $v_s>c_\text{lat}$ without the source/kernel combination breaking down (e.g., kernel non-hyperbolicity, loss of a well-posed initial-value formulation) — this is a second, independent obstruction worth checking explicitly rather than assuming.

## 5. Problems identified (ranked by severity)

1. **No negative-beable-energy channel (fatal for all superluminal variants).** F193's derived non-negativity of $T^{00}$ removes the one ingredient every confirmed-still-WEC-violating superluminal warp solution needs, and removes it more completely than standard QFT does (no Casimir/zero-point loophole — M5).
2. **Metric-engineering is methodologically backwards relative to the model's causal chain** (matter beables → induced $G_{\mu\nu}$, never the reverse). Any "test" of Alcubierre's metric has to be re-posed as a forward search over beable configurations, which is a much harder and not-yet-attempted computation.
3. **Unverified well-posedness of a superluminal shift vector under the induced-gravity construction** (M4/F181 kernel) — independent of the energy-condition problem, and currently an open question rather than a settled no.
4. **The literature's own floor** (Ford–Pfenning QI, the 2025 Lentz re-analysis) already excludes the superluminal branch on conventional GR+QFT grounds; the model doesn't need to do new work to inherit that conclusion for the same metrics.

## 6. Optional solutions / mitigation paths worth testing

| Path | What it would require in this model | Verdict risk |
|---|---|---|
| **A — Subluminal positive-energy class** (Bobrick–Martire / Fuchs et al. constant-velocity drive) | Forward-construct a beable field configuration whose induced $T^{00}\ge0$, run it through the F181 two-function kernel, check if the resulting metric reproduces the target bump geometry at $v_s<c_\text{lat}$. No M2 violation; M1/M4 need explicit checking. | Most likely to yield a real (if FTL-less) result — recommend running this first. |
| **B — Natário zero-expansion reformulation** | Same M2 problem as Alcubierre (still needs $T^{00}<0$ somewhere per Ford-Pfenning's own QI analysis of the Natário case) — does not avoid the fatal problem, only relaxes the QI sampling-time bound. Not worth separate model-specific work beyond noting it inherits problem 1. | Excluded for the same reason as Alcubierre. |
| **C — Treat $f$ as a *target* and search whether any allowed (positive-$T^{00}$) lattice configuration approximates a bump-like $K$ profile at $v_s\to c_\text{lat}^-$** (i.e. push the subluminal class as close to the lattice speed limit as M4 allows) | Pure CASIM parameter scan on the F181 kernel; well-posed, no new physics needed. | Bounded, answerable; gives a quantitative "how close can this model's warp-like geometry get to $c_\text{lat}$" number. |
| **D — Revisit M5 (no fluctuation reservoir)** | Would require deriving a beable analogue of vacuum fluctuations that *does* gravitate — directly contradicts the load-bearing F193 derivation and would have to reopen F164's cosmological-constant resolution. Not recommended; flagged only because it's the one assumption an FTL-permissive result would need to overturn. | High cost, low payoff — touches a closed, cross-validated finding chain (F164→F193→F196). |

**Recommended path: A, then C.** Both are forward (matter → metric) computations consistent with M1, use the existing F181 kernel without modification, and produce a definite, checkable number either way.

## 7. CASIM build & run (for the sub-agent that picks this up)

1. **Symbolic gate (sympy, no lattice run):** confirm that the standard Alcubierre/Natário $T_{\mu\nu}$ (computable directly from $G_{\mu\nu}$ of the bump metric) has $T^{00}<0$ somewhere in the wall for any $f$ with the required boundary conditions ($f\to1$ inside, $f\to0$ outside, smooth). This reproduces Pfenning–Ford symbolically inside the repo rather than citing it secondhand — cheap, and pins down exactly where M2 bites.
2. **Forward search (Path A):** using `ca_interior_metric.py` (F181), parametrize a positive-$T^{00}$, momentum-carrying beable configuration (e.g. a moving shell of positive energy density with a tuned momentum-flux $T^{0i}$) and solve forward for the resulting two-function metric; compare to the Bobrick–Martire / Fuchs target geometry.
3. **Speed-limit scan (Path C):** sweep the shell's coordinate velocity toward $c_\text{lat}=1/\sqrt3$ and record where the F181 kernel's well-posedness or the EP/redshift/deflection battery (F62/F64, already regression-tested) breaks down.
4. **Write-up:** if 1–3 converge to a determinate result, file it as a new finding (`findings/F19{7+}-alcubierre-...md`, next number after F196 at time of writing — re-check `findings-index.md` for collisions per `CLAUDE.md` convention) and add a one-paragraph `docs/status/changelog.md` entry. If inconclusive, leave this file as the open brief and note what specifically blocked it.

## 8. Verdict gate (first pass, literature + findings synthesis only — no new CASIM run yet)

- **Superluminal Alcubierre/Natário/contested-Lentz family: STRUCTURALLY EXCLUDED** in this model, on grounds *stronger* than mainstream GR+QFT (no beable negative-energy or zero-point-fluctuation channel exists at all — F193 M2/M5), independent of and in addition to the standard Ford–Pfenning quantum-inequality exclusion.
- **Subluminal positive-energy family (Bobrick–Martire / Fuchs 2024): NOT EXCLUDED, NOT YET TESTED.** No model commitment forbids it; §7 steps 2–3 are the concrete next work.
- This is a **first-pass synthesis**, not a finding — promote to `F19{7+}` only after the symbolic + CASIM steps in §7 are actually run.

## 9. RESOLVED → F204 (2026-06-30 - 20:55)

The §7 symbolic + forward steps were run; the first-pass verdict is **confirmed by computation** and promoted to **[[F204-alcubierre-warp-structural-exclusion]]** (5/5 PASS, `tests/findings/test_F200_alcubierre_structural.py`, results `test-results/F200_alcubierre_structural.json`). Numbers:

- **§7.1 symbolic gate (exact, residual 0):** the Alcubierre Eulerian energy density is $\rho=-\tfrac{1}{8\pi}\tfrac{v_s^2}{4}\tfrac{(y^2+z^2)}{r_s^2}f'(r_s)^2$, derived from the full Einstein tensor and matching Pfenning–Ford with zero residual. $\rho<0$ in the wall for any smooth $f$ → WEC violated for the Eulerian observer → **M2 (F193) fatal** for the superluminal branch.
- **§7 forward / Path A:** integrated wall energy $E(v_s)=-C v_s^2<0$ for **every** $v_s$ (incl. subluminal); F181 kernel carries a positive source fine (M3 — kernel is not the obstruction, the source *sign* is); momentum density and negative wall are both $\propto f'^2$ (co-supported, $98.5\%$).
- **§7 Path C / speed limit:** induced isotropic field well-posed, $c_\text{eff}\le c_\text{lat}=1/\sqrt3$; warp ceiling is $c_\text{lat}$, and $\rho_\text{wall}\propto-v_s^2$ never opens a positive-source bubble (M4).

Still open (recorded in F204 §Open): a *dynamically evolved* superluminal shift vector (gravitomagnetic $T^{0i}$ kernel, live two-grid) and a genuine forward Bobrick–Martire construction of the subluminal class. This brief is now closed as a structural test; constructive subluminal work, if ever wanted, lives under those open items.

## Sources

- [Alcubierre drive — Wikipedia](https://en.wikipedia.org/wiki/Alcubierre_drive)
- [Pfenning & Ford, "The unphysical nature of 'warp drive'" (gr-qc/9702026)](https://arxiv.org/abs/gr-qc/9702026)
- [Ford–Pfenning quantum inequalities applied to the Natário warp drive](https://hal.science/hal-00734603v2/document)
- [Ford & Roman, "Quantum Inequality Restrictions on Negative Energy Densities in Curved Spacetimes" (gr-qc/9805037)](https://arxiv.org/abs/gr-qc/9805037)
- [Bobrick & Martire, "Introducing Physical Warp Drives" (2102.06824)](https://arxiv.org/abs/2102.06824)
- [Fuchs et al., "Analyzing Warp Drive Spacetimes with Warp Factory" (2404.03095)](https://arxiv.org/pdf/2404.03095)
- [Violations of the Weak Energy Condition for Lentz Warp Drives (2025 re-analysis)](https://www.researchgate.net/publication/397934716_Violations_of_the_Weak_Energy_Condition_for_Lentz_Warp_Drives)
- ["Is a Warp Drive Possible? The Physics, 30 Years On"](https://sciencereader.com/the-elusive-physics-of-warp-drives-and-faster-than-light-travel/)
