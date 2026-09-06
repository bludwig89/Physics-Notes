# F346 — Ledger E6 first attack: the charged-lepton $E_g/T_{1u}$ "weight-as-phase" shape mechanism (F175/F92) does not transplant to either quark sector — a leaning no-go, not a full closure

**Date:** 2026-09-02 - 02:30
**Status:** Candidate finding — 6/6 checks PASS, all mechanical (exact circulant fit + Monte Carlo uncertainty propagation + a lepton-sector method self-check). **What this establishes:** inverting F175's exact 3-parameter circulant ansatz on the PDG 2024 up-type $(u,c,t)$ and down-type $(d,s,b)$ current-quark mass triplets gives a fitted shape angle $\delta$ that (i) for up-type sits a clean, decisive $>200\sigma$ from every single-irrep $O_h$ weight the same $T_{1u}\otimes T_{1u}$ decomposition offers (including the lepton's own $2/9$), and (ii) for down-type sits a nominal $\sim1.4\sigma$ from the $A_{1g}$ weight $1/9$ (measurement precision) — current data cannot exclude this proximity, and a separately-computed, properly-scaled range-based look-elsewhere estimate puts it at a real but modest coincidence ($p\approx0.57\%$ that at least one of the two quark sectors would land this close to some candidate purely by chance), neither vanishingly rare nor common. (This corrects the finding's first-written text, which conflated the two questions and reported an unrelated, wrongly-scaled $p\approx0.6$ using measurement precision — see the independent review below.) Neither quark sector's fitted amplitude $\eta^2$ approaches the lepton's derived equipartition value $\eta^2=2$ (F92), and the two quark sectors do not even agree with each other. **What this does not establish:** a full closure of ledger row E6 — no alternative quark-sector mechanism has been tried or excluded, only the direct transplant of F175/F92's specific values.
**Reviewed:** 2026-09-02 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F346-review-2026-09-02.md))
**Module:** `src/casim/engine/particles/derive_quark_shape_probe.py`
**Script:** `tests/findings/test_F346_quark_shape_probe.py` (~0.3 s, numpy + stdlib)
**Results:** `test-results/F346_quark_shape_probe.json`
**Test record:** `F346-quark-shape-probe` (tier battery, `tests/registry/particles.yaml`)
**Cross-references:** [[F175-lattice-2-9-eg-weight]] (the exact $\delta^*=2/9$ derivation and the ansatz this reuses verbatim), [[F92-per-constituent-phase-consistency]] (the $\eta^2=1/2$ Koide equipartition amplitude this compares against), [[F80-one-45deg-em-saturation-koide]] (D4's Koide-$Q$ evidence this sharpens from a coarse ratio to an angle-level, uncertainty-propagated statement), [[F121-tau-anchored-canonical-spectrum]] (the "consistency readout, not derivation" statement this row exists to fix), [[F123-p6-si-scale-matter-sector]] (the constituent scale $m_c=309.5$ MeV — a different quantity, not conflated here), [[F75-three-generations-from-bcc-irrep-selection]] (the charge-blind generation-**count** mechanism, discussed in §5 but not re-derived), [[F343-majorana-scale-no-link-found]] (the methodological precedent for a mechanical, multiple-comparisons-aware null result on an open ledger row).

---

## 1. The question (ledger E6)

`docs/status/open-derivations.md` row **E6** grades the six quark (current) masses **ABSENT ×6**: parameters #1–6 have no proposed route at all. F121 §4 is explicit that the numbers currently listed against them are *"the measured values converted to kg — a consistency readout,"* and F123's constituent-quark scale $m_c=309.5$ MeV is a **different quantity** (a dynamically-generated constituent mass, not the current-quark mass this row is about) that the row itself warns must not be quoted as covering it.

E6 names its own smallest useful first question, which this finding answers:

> Does the $E_g/T_{1u}$ machinery that gives the charged-lepton **shape** to $0.007\%$ (F175, using F92) have **any** quark-sector face, or is it structurally lepton-only? F80-D4 already showed the up/down Koide $Q$ values ($0.849,\ 0.731$) sit outside the clean-pair band the lepton argument needs — evidence *for* lepton-only, worth checking properly.

## 2. The exact ansatz, reused verbatim from F175

F175 (D4–D5) writes the charged-lepton masses as a $O_h$-derived circulant:

$$\sqrt{m_a} = \mu\big(1+\eta\cos(\delta+\tfrac{2\pi a}{3})\big),\qquad a=0,1,2,$$

with **two independently-derived** numbers: $\eta=\sqrt2$ (F92, the $45°$ Cooper-pair equipartition) and $\delta^\*=\tfrac29$ rad (F175, the exact $E_g$ representation weight $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$, one of four weights available in $T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g}$, dims $1{+}2{+}3{+}3=9$). F80 §5 supplies the reason only charged leptons reach these specific values: they are the unique sector that is EM-coupled *and* colour-free, so only they couple to the clean abelian rotation whose saturation the equipartition/weight values describe. Quarks carry colour; their mass dynamics are QCD-dominated.

**Any 3 positive numbers admit an exact $(\mu,\eta,\delta)$ fit** of this form — it is a coordinate change (3 real degrees of freedom in, 3 out), the same fact that underlies Koide's own original parametrization. So inverting the ansatz on quark masses is not by itself informative; what is informative is **where the fitted $\delta$ lands** relative to the three single-irrep weights the *same* 9-dimensional decomposition offers — $A_{1g}=\tfrac19$, $E_g=\tfrac29$, $T_{1g}$ or $T_{2g}=\tfrac13$ — since a hit there would be evidence of the same lattice structure, and a clean miss is exactly the "structurally lepton-only" no-go the row anticipates. Multi-irrep *combinations* are deliberately excluded from the candidate set: every integer $0$–$9$ is some subset sum of $\{1,2,3,3\}$, so comparing against subset sums would be pure post-hoc fishing; comparing against a single named channel's weight mirrors what F175 actually derived.

A phase shift $\delta\to\delta+\tfrac{2\pi}{3}$ is exactly a cyclic relabelling of which triplet index is "first," so $\delta\bmod\tfrac{2\pi}{3}$ is the labelling-independent, physical quantity compared throughout.

## 3. Method validation: the same code recovers F175/F92 on leptons (C5)

Before trusting the method on quarks, the identical fitting code is run on the PDG charged-lepton masses (F121's own values):

| quantity | recovered | F175/F92 target | agreement |
|---|---|---|---|
| $\delta \bmod \tfrac{2\pi}{3}$ | $0.222230$ rad | $\tfrac29=0.222222$ rad | $0.0033\%$ |
| $\eta$ | $1.414201$ | $\sqrt2=1.414214$ | $1.3\times10^{-5}$ abs. |

This confirms the inversion is a faithful inverse of F175's forward construction (the labelling ambiguity resolves correctly under the $\bmod\ \tfrac{2\pi}{3}$ reduction) before it is applied to quarks.

## 4. The quark-sector result

Inputs: PDG 2024 current-quark masses (S. Navas et al. (Particle Data Group), *Phys. Rev. D* **110**, 030001 (2024)) — $u,d,s$ at $\overline{\text{MS}}$, $\mu=2$ GeV; $c,b$ at $\overline{\text{MS}}(m_q)$; $t$ from direct kinematic measurement (**not** a current $\overline{\text{MS}}$ mass — an inherited scheme inconsistency, flagged exactly as F80-D4 already flags it: "scheme-rough; the conclusion is robust").

| | $u,c,t$ (MeV) | $\sigma$ (MeV) | $d,s,b$ (MeV) | $\sigma$ (MeV) |
|---|---|---|---|---|
| central | $2.16,\ 1273.0,\ 172570$ | $0.07,\ 4.6,\ 290$ | $4.70,\ 93.5,\ 4183$ | $0.07,\ 0.8,\ 7$ |

Fitted circulant parameters, and their distance from the nearest single-irrep $O_h$ weight (Monte Carlo, $2\times10^4$ draws propagating the PDG uncertainties above):

| sector | $Q$ (Koide) | $\eta^2$ | $\delta\bmod\tfrac{2\pi}{3}$ | nearest weight | distance |
|---|---|---|---|---|---|
| lepton (check) | $0.66666$ | $2.000$ | $0.22223$ rad | $E_g=2/9$ | $0.003\sigma$-level, $0.003\%$ |
| up-type $(u,c,t)$ | $0.8488$ | $3.093$ | $0.07452$ rad | $A_{1g}=1/9$ | $\mathbf{219\sigma}$ |
| down-type $(d,s,b)$ | $0.7313$ | $2.388$ | $0.11012$ rad | $A_{1g}=1/9$ | $1.45\sigma$ |

(The Koide $Q$ values reproduce F80-D4's recorded $0.849$ and $0.731$, confirming this computation shares the same, previously-checked mass inputs and is a genuine angle-level extension of that result, not an independent re-measurement.)

**Up-type is a clean, decisive miss.** At $219\sigma$ from the nearest candidate ($A_{1g}=1/9$) — and further still from $E_g=2/9$ ($882\sigma$) and $T_{1g}/T_{2g}=1/3$ ($1546\sigma$) — the up-type angle is nowhere near any weight this decomposition offers, at a significance current PDG precision resolves completely unambiguously.

**Down-type's proximity to $1/9$ is not excluded by data, and is a modest, not-dismissible coincidence.** $1.45\sigma$ (measurement precision, PDG-uncertainty Monte Carlo) means current data cannot rule out $A_{1g}=1/9$ for down-type — a weaker statement than confirmation, and this is the only role measurement-precision $\sigma$ can play here. The separate question — *is a central-value proximity this close numerologically unusual for an otherwise generic angle* — needs its own, differently-scaled calculation: a range-based look-elsewhere estimate over the natural domain $[0,2\pi/3)$ that a fitted phase can occupy. That calculation (not measurement precision) gives $p\approx0.28\%$ for down-type alone, and $p\approx0.57\%$ for "at least one of the 2 sectors this close to some candidate," using the observed central distances $9.92\times10^{-4}$ rad (down-type) and $0.0366$ rad (up-type) against the $2\pi/3\approx2.094$ rad domain — a real but modest coincidence, not the earlier (and wrong) claim that it is *more likely than not* to be pure chance. (An earlier draft of this finding instead fed the measurement-precision $\sigma$ into that look-elsewhere formula, which inverts the wrong way: an increasingly precise future measurement landing exactly on $1/9$ would have been reported by that formula as *less* significant, not more — caught by a perturbation-sweep review attack and fixed; see `docs/reviews/F346-review-2026-09-02.md`.) The "flagged, not adopted" verdict does not rest on this probability being small — it rests on two things the probability estimate cannot supply: there is no independent theoretical reason down-type quarks specifically would carry the $A_{1g}$ (not $E_g$) weight, the way F80 supplies one for the lepton's $E_g$; and the near-miss does **not** recur in the up-type sector — no consistent cross-sector pattern emerges. **Flagged, not adopted.**

**Neither sector reaches the lepton's amplitude.** $\eta^2_\text{up}=3.09$ and $\eta^2_\text{down}=2.39$ both sit well away from the lepton's derived $\eta^2=2$ (F92), and from each other — no universal quark equipartition point emerges either, consistent with F80's story that only the EM-coupled, colour-free sector reaches that saturation point.

## 5. The generation-count question is separate, and not attacked here

E6's question bundles two different things the ledger keeps distinct elsewhere: whether quarks share the lepton's $T_{1u}$ generation-**triplet** structure (the *count*, 3), and whether they share its specific $E_g$-weight **shape** (the *angle* $2/9$ and amplitude $\eta^2=2$). This finding attacks only the shape question, and gets a leaning no-go on it (§4).

The count question has a relevant existing fact worth noting explicitly, though it is **not** newly derived here: F75's derivation that the fermion generation multiplet is exactly the $T_{1u}$ irrep of $O_h$ rests only on (i) the point-group content of the BCC nearest-neighbour shell and (ii) the F27 scalar-mass parity rule selecting the unique odd triplet from it (F75 §3, Steps 2–3). Neither step references electric charge, colour, or any gauge quantum number — the argument is about the lattice geometry seen by *any* Dirac fermion's mass term. So nothing in F75 itself would forbid the quark generations from being the same $T_{1u}$ triplet (matching the observed fact of exactly 3 quark generations); F75's own §7 caveat that "generation index = orbital irrep" is "a hypothesis, not a theorem" applies here exactly as it does to leptons, no more and no less. This is offered as a pointer for a future session, not a result of this one.

## 6. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | pipeline sanity: recomputed $Q_\text{up},Q_\text{down}$ match F80-D4's recorded $0.849,0.731$ | matched to $10^{-3}$ | exact |
| C2 | up-type angle decisively excluded (measurement precision) from every single-irrep $O_h$ weight | $219\sigma$ (nearest) | quantitative |
| C3 | down-type angle NOT excluded (measurement precision) from $A_{1g}=1/9$ | $1.45\sigma$ | quantitative |
| C4 | range-based look-elsewhere probability is modest, not overwhelming and not dismissible | $p\approx0.57\%$ (either sector), $p\approx0.28\%$ (down-type alone) | quantitative |
| C5 | neither quark sector's $\eta^2$ matches the lepton's derived $2$ | up $3.09$, down $2.39$ | quantitative |
| C6 | method self-check: recovers F175's $2/9$ and F92's $\sqrt2$ on leptons | $0.003\%$, $1.3\times10^{-5}$ | machine |

**Overall 6/6 PASS.** (Renumbered and C3/C4 re-scoped during review — see `docs/reviews/F346-review-2026-09-02.md`, Attack 7 — from an earlier 5-check version whose C3/C4 conflated measurement precision with a look-elsewhere estimate.)

## 7. Verdict, and what would reopen this

**Leaning no-go for the shape-level question, not a full closure.** (Verdict unchanged by the review's correction; only the down-type statistical justification moved — see the boxed note in §4 and the independent review.) The direct transplant of F175/F92's specific $(\delta,\eta)$ values onto either quark-mass triplet fails: up-type decisively (excluded by data at $>200\sigma$), down-type not excluded by data but only a modest, not-dismissible numerical coincidence once a properly-scaled look-elsewhere estimate is applied (§4). This sharpens F80-D4's coarse Koide-$Q$ observation into a quantitative, uncertainty-propagated statement at the angle level, using the *same* group-theoretic candidate set ($A_{1g},E_g,T_{1g}/T_{2g}$) the lepton derivation itself produced — closing off the most literal version of "maybe it's just a different weight from the same decomposition" for up-type, and showing the one apparent down-type near-hit does not survive scrutiny.

What is **not** closed: (i) a quark-sector mechanism built on different physics (e.g. one anchored to the constituent/dynamical mass of F123 rather than the current mass, or one that incorporates the QCD condensate rather than ignoring it) has not been tried; (ii) the generation-**count** question (§5) is untouched and may have a positive answer via F75 independent of this shape-level result; (iii) down-type's $1/9$ proximity is not proven meaningless — a future session with an independently-motivated reason to expect $A_{1g}$ specifically for down-type (not yet proposed anywhere) could revisit it; (iv) the independent review (`docs/reviews/F346-review-2026-09-02.md`, Attack 11) surfaced a different, untested avenue in the literature: Harari, Haut & Weyers, *Phys. Lett. B* **78** (1978) 459, report a Koide-type $Q\approx2/3$ for a **mixed-generation-type** quark triplet (mixing up- and down-type, e.g. $u,d,s$ together) — a different grouping from the same-generation-type $(u,c,t)$/$(d,s,b)$ triplets tested here (which match F80-D4's convention). This finding does not test that grouping and neither confirms nor excludes it.

**Grade:** E6 promotes **ABSENT → OPEN** per the ledger's own stated criterion — a first named attack and a first computation, even one with a leaning-negative outcome, is exactly what promotes the grade; a clean structural no-go is stated to be "a legitimate, valuable outcome" there, and this is a partial version of one (decisive for up-type, inconclusive-leaning-negative for down-type).

**Claim:** none — this finding neither derives, extends, nor contradicts anything the standing claims rule (`docs/claims/README.md`) is built to track — it establishes that one specific extension attempt of an *existing* mechanism (F175/F92) does not work, without asserting a new, defensible, present-tense claim about quark masses. Per the finding-claim-test-guide's own contract, "a pure no-go might not need one," and this result is honestly short of even a pure no-go (down-type is inconclusive, not excluded) — so no card is filed. A card would become appropriate if a future session either (a) fully excludes any quark-sector shape mechanism in this family, which would be a `no_go` card, or (b) finds a working one, which would be a `derivation`/`prediction` card.

## 8. Provenance

- **New:** the circulant-fit inversion applied to quark mass triplets; the restriction of the candidate-weight set to single-irrep weights (avoiding subset-sum fishing); the Monte Carlo PDG-uncertainty propagation into the fitted angle; a range-based look-elsewhere estimate for the down-type near-hit (corrected during review from an earlier, wrongly-scaled measurement-precision version — `docs/reviews/F346-review-2026-09-02.md`); the lepton-sector self-check tying the method to F175/F92; the explicit separation of the count question (§5, not attacked) from the shape question (§4, attacked).
- **Reused:** F175's exact ansatz and $E_g$-weight derivation; F92's $\eta^2=1/2$ derivation; F80's EM/colour selection story and its D4 quark masses (reused verbatim for direct comparability, cross-checked against PDG 2024's near-identical current values); F121's charged-lepton masses; F75's charge-blind generation-count mechanism (cited, not re-derived); F343's methodology (mechanical null result with an explicit, quantified multiple-comparisons caveat) as the structural template for this finding.
- **External:** PDG 2024 quark masses (S. Navas et al., *Phys. Rev. D* **110**, 030001 (2024), "Quark Masses" summary table).
- **Verification:** `tests/findings/test_F346_quark_shape_probe.py` (2026-09-02, 10/10 pytest functions PASS, 6/6 named checks PASS via the registry entry point), results `test-results/F346_quark_shape_probe.json`, registry record `F346-quark-shape-probe` (`tests/registry/particles.yaml`, tier battery) — `casim test --id F346-quark-shape-probe` PASS. Independent review: `docs/reviews/F346-review-2026-09-02.md` (CONFIRMED-NARROWER; blind cold-subagent re-derivation matched to 5-6 sig figs by a different numerical method; one perturbation-sweep attack found and fixed a real statistical-framing bug, documented above).
