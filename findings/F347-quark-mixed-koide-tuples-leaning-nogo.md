# F347 — Ledger E6, second attack: the literature's mixed-generation-type Koide quark tuples (u,d,s; c,b,t) carry no more of the charged-lepton $E_g/T_{1u}$ shape mechanism than F346's same-generation-type tuples did

**Date:** 2026-09-02 - 03:20
**Status:** Candidate finding — 8/8 checks PASS, all mechanical (exact circulant fit + Monte Carlo uncertainty propagation, both measurement-precision and range-based look-elsewhere calculations built in from the start). **What this establishes:** (i) the historical Harari-Haut-Weyers (1978) Koide-type match on $(u,d,s)$ does **not** hold with current, nonzero-$m_u$ PDG 2024 data — it relied on a since-superseded massless-up-quark assumption; (ii) Rodejohann & Zhang's $(c,b,t)$ Koide $Q\approx2/3$ claim **does** still hold today (to $<1\%$) — a real, still-valid literature coincidence — but Koide's $Q$ depends only on the circulant amplitude $\eta$ ($Q=\tfrac13+\tfrac{\eta^2}{6}$, exactly, independent of the phase $\delta$), and decomposing $(c,b,t)$ shows its fitted $\delta$ is a clean, decisive miss from every single-irrep $O_h$ weight the same $T_{1u}\otimes T_{1u}$ decomposition offers — a miss that is *also* not numerically unusual in absolute terms. Even the $\eta^2$ closeness that drives $Q\approx2/3$ is itself a many-sigma measurement-precision miss from the lepton's derived $\eta^2=2$, despite looking close in percentage terms. **What this does not establish:** a full closure of ledger row E6 — Rivero's signed $(s,c,b)$ variant (a genuinely different ansatz) and other groupings/orderings remain untested.
**Reviewed:** 2026-09-02 — **CONFIRMED** ([independent review](../docs/reviews/F347-review-2026-09-02.md))
**Module:** `src/casim/engine/particles/derive_quark_mixed_koide_probe.py`
**Script:** `tests/findings/test_F347_quark_mixed_koide_probe.py` (~0.2 s, stdlib only)
**Results:** `test-results/F347_quark_mixed_koide_probe.json`
**Test record:** `F347-quark-mixed-koide-probe` (tier battery, `tests/registry/particles.yaml`)
**Cross-references:** [[F346-quark-shape-eg-t1u-leaning-nogo]] (the same-generation-type attempt this directly follows up on, and the pipeline/ansatz reused verbatim), [[F175-lattice-2-9-eg-weight]] (the exact $\delta^*=2/9$ derivation), [[F92-per-constituent-phase-consistency]] ($\eta^2=1/2$), [[F80-one-45deg-em-saturation-koide]] (the EM/colour selection story), [[F121-tau-anchored-canonical-spectrum]], [[F123-p6-si-scale-matter-sector]].

---

## 1. The question

F346 (docs/status/open-derivations.md row E6) tested whether the charged-lepton $E_g/T_{1u}$ circulant shape mechanism (F175's $\delta^*=\tfrac29$ + F92's $\eta^2=\tfrac12$) transplants to **same-generation-type** quark triplets — up-type $(u,c,t)$ and down-type $(d,s,b)$ — and found a leaning no-go. Its independent review (`docs/reviews/F346-review-2026-09-02.md`, Attack 11 — prior-art search) surfaced that the physics literature has, since 1978, instead repeatedly proposed **mixed-generation-type** triplets — crossing up-type and down-type quarks across generations — as Koide-formula candidates:

- **Harari, Haut & Weyers**, "Quark masses and Cabibbo angles," *Phys. Lett. B* **78** (1978) 459–461 — the earliest Koide-type formula in print, for $(u,d,s)$, built on a **massless up quark** ($m_u=0$), an assumption the measured, nonzero up-quark mass has since superseded.
- **Rodejohann & Zhang**, "Extended Empirical Fermion Mass Relation," arXiv:1101.5525, published *Phys. Lett. B* **698** (2011) 152–156 — states the Koide relation "may be valid for the $u,d,s$ quarks, and for the $c,b,t$ quarks."
- **Rivero**, "A new Koide tuple: strange-charm-bottom," arXiv:1111.7232 — a third tuple, $(s,c,b)$, but only with a **negative** sign on $\sqrt{m_s}$ — a genuinely different, signed-square-root ansatz.

This finding re-checks the two real-positive-ansatz tuples, $(u,d,s)$ and $(c,b,t)$, against the same **current** PDG 2024 masses F346 used (not the historical or assumed values the 1978–2011 papers had available), first via the plain Koide $Q$, then via F346's own circulant-fit-vs-single-irrep-weight pipeline. Rivero's signed $(s,c,b)$ tuple is noted but **not** fit here — F175's ansatz is a real, all-positive circulant; admitting a sign flip is a genuine generalization of the ansatz, not a rerun of this one, and is left for a future session.

## 2. Method: identical ansatz and candidate set to F346

$$\sqrt{m_a} = \mu\big(1+\eta\cos(\delta+\tfrac{2\pi a}{3})\big),\qquad a=0,1,2,$$

fit exactly (any 3 positive numbers admit this fit — 3 real degrees of freedom in, 3 out) and compared against the three single-irrep $O_h$ weights available in $T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g}$: $A_{1g}=\tfrac19$, $E_g=\tfrac29$, $T_{1g}$ or $T_{2g}=\tfrac13$ (the same restricted candidate set F346 used, avoiding subset-sum fishing). Tuples are ordered by ascending mass — $(u,d,s)$ and $(c,b,t)$ — matching both the literature's own naming convention and F346's ordering convention for this ansatz (a genuine, disclosed choice among the $3!=6$ orderings a 3-element unordered tuple admits; see the review below).

**The key structural point this finding turns on:** Koide's $Q = \sum m_a/(\sum\sqrt{m_a})^2$ depends **only** on $\eta$ — algebraically, $Q=\tfrac13+\tfrac{\eta^2}{6}$, independent of $\delta$ (checked exactly below, to $10^{-9}$). F175/F92's stronger claim requires **both** $\eta^2=2$ **and** $\delta=\tfrac29$; a literature-flagged $Q\approx\tfrac23$ coincidence is only ever evidence for the first, weaker half.

## 3. Method validation: lepton self-check (C6)

The identical code, run on F121's charged-lepton masses:

| quantity | recovered | F175/F92 target | agreement |
|---|---|---|---|
| $\delta\bmod\tfrac{2\pi}{3}$ | $0.222230$ rad | $\tfrac29=0.222222$ rad | $0.0033\%$ |
| $\eta$ | $1.414201$ | $\sqrt2=1.414214$ | $1.3\times10^{-5}$ abs. |

Confirms the fitting method before it is applied to the two new tuples.

## 4. The result

Inputs: PDG 2024 current-quark masses (S. Navas et al., *Phys. Rev. D* **110**, 030001 (2024)) — identical values to F346 — $u=2.16\pm0.07$, $d=4.70\pm0.07$, $s=93.5\pm0.8$, $c=1273.0\pm4.6$, $b=4183\pm7$, $t=172570\pm290$ MeV.

**$(u,d,s)$ — the historical Harari-Haut-Weyers claim does not survive current data.** Koide $Q=0.5667$, a $15.0\%$ relative miss from $\tfrac23=0.6667$ — not close. The 1978 near-hit used $m_u=0$; with the measured $m_u=2.16$ MeV, the match is gone. The fitted phase ($\delta\bmod\tfrac{2\pi}3=0.0769$ rad) also misses every $O_h$ candidate at $10.8\sigma$ (measurement precision, nearest $A_{1g}=\tfrac19$) and is not numerically unusual in absolute terms either (range-based look-elsewhere $p=9.8\%$). $\eta^2=1.400$ is nowhere near the lepton's $2$. A clean negative on every axis.

**$(c,b,t)$ — Rodejohann-Zhang's $Q\approx2/3$ claim is real and still holds, but is $\eta$-only.** Koide $Q=0.66922$, a $0.38\%$ relative match to $\tfrac23$ — a genuine, still-valid coincidence with current data. Decomposing it:

| quantity | value | comparison | verdict |
|---|---|---|---|
| $\eta^2$ | $2.01533$ | lepton target $2$; relative diff $0.77\%$; MC $\sigma=0.0016$ | **$9.6\sigma$ from $2$ — excluded at measurement precision despite the small percentage gap** |
| $\delta\bmod\tfrac{2\pi}3$ | $0.06865$ rad | nearest candidate $A_{1g}=\tfrac19=0.11111$ rad; MC $\sigma=2.08\times10^{-4}$ | **$204\sigma$ from $A_{1g}$ — a clean, decisive miss** |
| range-based look-elsewhere ($\delta$) | central distance $0.0425$ rad | domain $[0,\tfrac{2\pi}3)=2.094$ rad, 3 candidates | $p=12.2\%$ — **not numerically unusual either** |

The pattern is the mirror image of "looks close but isn't": $Q$'s percentage-level closeness to $\tfrac23$ survives only because $Q$ is blind to $\delta$ entirely, and even the $\eta^2$ number driving that closeness is, at PDG's actual precision on $c,b,t$, a decisively excluded value rather than a confirmed one. **The literature's $(c,b,t)$ coincidence carries no accompanying phase/shape coincidence at all.**

## 5. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| C1a | $(u,d,s)$'s $Q$ not close to $2/3$ with current data | $15.0\%$ off | quantitative |
| C1b | $(c,b,t)$'s $Q$ close to $2/3$ with current data | $0.38\%$ | quantitative |
| C1c | $Q=\tfrac13+\tfrac{\eta^2}{6}$ identity holds exactly, both tuples | $<10^{-9}$ | exact |
| C2 | $(c,b,t)$ phase decisively excluded (measurement precision) from every $O_h$ weight | $204\sigma$ | quantitative |
| C3 | $(c,b,t)$ phase proximity not numerically unusual (range-based) | $p=12.2\%$ | quantitative |
| C4 | $(c,b,t)$ $\eta^2$ close in percent ($<2\%$) but excluded at measurement precision ($>5\sigma$) | $0.77\%$, $9.6\sigma$ | quantitative |
| C5 | $(u,d,s)$ fails both phase and amplitude independently of its $Q$ miss | $10.8\sigma$, $\eta^2$ diff $0.60$ | quantitative |
| C6 | lepton self-check recovers F175's $2/9$ and F92's $\sqrt2$ | $0.003\%$, $1.3\times10^{-5}$ | machine |

**Overall 8/8 PASS.**

## 6. Verdict, and what would reopen this

**Leaning no-go, sharper than F346's.** Neither of the two literature-favoured mixed-generation-type tuples carries F175/F92's specific shape mechanism. $(u,d,s)$ fails even the weaker $Q$-only test once the historical massless-up-quark assumption is replaced with measured data. $(c,b,t)$ passes the $Q$-only test but that test is provably blind to the phase information the lepton mechanism actually needs — decomposing it into $(\eta,\delta)$ shows a decisive miss on both counts (phase: decisively excluded and numerically unremarkable; amplitude: decisively excluded despite a small percentage gap). Combined with F346, this closes off the two most literature-prominent 3-quark Koide groupings — one same-generation-type family, two mixed-generation-type tuples — as carriers of the lepton's shape mechanism, strengthening the "structurally lepton-only" reading without proving it exhaustively.

What is **not** closed: (i) Rivero's signed $(s,c,b)$ tuple uses a genuinely different ansatz (a diagonal $\pm1$ sign matrix on $\sqrt{m_a}$ before the DFT) that has not been generalized into this pipeline or tested; (ii) other quark triplet groupings and orderings exist combinatorially and have not been exhaustively searched (nor should they be — an unrestricted search over all $\binom{6}{3}=20$ triplets and $3$ inequivalent orderings each would itself become the multiple-comparisons fishing this finding's candidate-weight restriction is designed to avoid); (iii) the generation-**count** question (F346 §5, via F75) remains untouched by either quark-mass finding.

**Grade:** this is a second, independent attack on the already-OPEN ledger row E6 (F346 promoted ABSENT×6→OPEN); it does not change E6's grade further but sharpens its "current status" text with a second, literature-driven no-go.

**Claim:** none — this finding neither derives, extends, nor contradicts anything the standing claims rule (`docs/claims/README.md`) is built to track. It shows that two already-published Koide-tuple candidates do not carry a different, existing mechanism's (F175/F92's) specific values — a negative result about an extension attempt, not a new present-tense assertion about quark masses. Per the finding-claim-test-guide's "a pure no-go might not need one," no card is filed.

## 7. Provenance

- **New:** applying F346's circulant-fit-vs-candidate-weight pipeline to the literature's mixed-generation-type tuples; the explicit $Q=\tfrac13+\tfrac{\eta^2}{6}$ identity check separating Koide's amplitude-only criterion from F175's stronger phase-and-amplitude criterion; the "close in percent, excluded in sigma" duality for $(c,b,t)$'s $\eta^2$, built in from the start (not retrofitted after a review, unlike F346); the correction of the historical Harari-Haut-Weyers $(u,d,s)$ claim against current, nonzero-$m_u$ data.
- **Reused verbatim:** F346's `fit_circulant`, candidate-weight set, Monte Carlo methodology, and the measurement-precision/range-based-look-elsewhere separation (built in here from line one, having learned from F346's Attack-7 bug rather than repeating it); F175's ansatz and $E_g$-weight derivation; F92's $\eta^2=\tfrac12$; F121's PDG lepton masses.
- **External:** PDG 2024 quark masses (S. Navas et al., *Phys. Rev. D* **110**, 030001 (2024)); Harari, Haut & Weyers, *Phys. Lett. B* **78** (1978) 459–461; Rodejohann & Zhang, arXiv:1101.5525 / *Phys. Lett. B* **698** (2011) 152–156; Rivero, arXiv:1111.7232 (cited for scope, not fit). The independent review (`docs/reviews/F347-review-2026-09-02.md`) additionally surfaced F. G. Cao (2012) and A. Kartavtsev, arXiv:1111.0480, "A remark on the Koide relation for quarks" — both further prior art on the plain-$Q$ question for quark triplets, neither performing the $\eta/\delta$ phase decomposition this finding is built on (confirmed independently novel by the review's blind subagent).
- **Verification:** `tests/findings/test_F347_quark_mixed_koide_probe.py` (2026-09-02, 12/12 pytest functions PASS including a forced-hit regression guard, 8/8 named checks PASS via the registry entry point), results `test-results/F347_quark_mixed_koide_probe.json`, registry record `F347-quark-mixed-koide-probe` (`tests/registry/particles.yaml`, tier battery) — `casim test --id F347-quark-mixed-koide-probe` PASS.
