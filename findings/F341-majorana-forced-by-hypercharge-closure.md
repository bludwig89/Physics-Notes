# F341 — No protecting symmetry forbids the F47 Majorana term, and removing it reopens the F165/F279 hypercharge closure: Majorana is the structurally required completion for the model's own hypercharge derivation, not merely a permitted option (rubric C4)

**Date:** 2026-08-31 - 16:35
**Checked:** 2026-08-31 - 16:19 -- cold subagent review (independent re-derivation of S1/S2 from scratch, plus adversarial search for an undercutting route), 5/5 legs CONFIRMED, 0 FAIL -- **CONFIRMED-NARROWER** (mechanical content exact; the headline "forced" wording tightened to make its conditionality explicit). See `docs/reviews/F341-review-2026-08-31.md`.
**Test record:** record `F341-majorana-forced-by-hypercharge-closure` (tier battery, sector particles) — `tests/registry/particles.yaml`
**Claim:** CL290
**Builds on:** [[F47-majorana-seesaw-higgs-free]] (the Higgs-free Majorana step, and the Y=0 forcing), [[F165-hypercharge-quantisation-from-anomaly-and-mass]] / [[F279-hypercharge-constraint-attribution]] (the hypercharge closure the Majorana row supplies), [[F202-leptogenesis-from-intrinsic-L-violation]] (the model's own use of L-violation as a load-bearing feature), [[F266-sterile-neutrino-dark-matter]] (the sterile relic built on the same Majorana step).

---

## The question (rubric row C4)

Row C4 of the completeness rubric — "Neutrino nature (Dirac vs Majorana)" — has read **PARTIAL** for five or more completeness reports:

> The Higgs-free Majorana step is constructed and $\nu_R$ is a structurally-forced total singlet ($Y=0$, and F279 A2 makes that row the one that closes the hypercharge system). Nothing **forces** Majorana over Dirac.

F47 builds a Higgs-free, gauge-invariant, R-unitary Majorana mass step for $\nu_R$ and shows the see-saw scaling comes out correctly. But F47 never claimed to *exclude* a Dirac-only alternative — a $\nu_R$ with only the ordinary F27/F41-style Dirac mass step and no Majorana bilinear is, on its own, an equally gauge-invariant construction. The residual has sat unmoved: **permitted, not forced.**

This finding closes the row with two convergent structural arguments, both mechanically re-verified rather than merely argued in prose (`tests/findings/test_F341_majorana_forced_by_hypercharge_closure.py`), plus an honest statement of exactly what is *not* claimed.

## Argument S1 — no protecting symmetry exists in the model

A Majorana mass term for a fermion is forbidden only by a symmetry under which the bilinear is charged. For $\nu_R$, three candidates exist in principle:

1. **Colour** — $\nu_R$ is a colour singlet; irrelevant.
2. **$SU(2)_L$** — $\nu_R$ is an $SU(2)_L$ singlet; irrelevant.
3. **$U(1)_Y$** — the only gauge charge the model actually assigns $\nu_R$. F47 M2/M3 and F279 §4 show the Majorana bilinear $\nu_R^{\mathsf T}C\nu_R$ carries hypercharge $2y_\nu$, and $y_\nu=0$ (structurally forced, F47/F279) makes this **exactly zero** — gauge invariance is *satisfied*, not violated. $U(1)_Y$ permits the term; it does not protect against it.

That exhausts the model's *local* gauge content. The only way a symmetry could still forbid the term is a **separate global charge** — lepton number, or gauged $B\!-\!L$ — under which $\nu_R$ is charged independently of $Y$. Test `check_S1_no_protecting_symmetry_is_registered` inspects `casim.constants`, `casim.constants.electroweak`, and `casim.engine.gauge.hypercharge` directly and confirms **no such generator is registered anywhere** in the model. This is not merely an omission: [[F202-leptogenesis-from-intrinsic-L-violation]] treats the Majorana step's lepton-number violation as **load-bearing** — the Sakharov condition that lets the same sector explain both baryogenesis and the resonant keV-sterile production [[F266-sterile-neutrino-dark-matter]] needs. The model does not merely fail to protect $L$; it actively *uses* $L$-violation as physics.

So forbidding the Majorana term would require **inventing** a global lepton-number symmetry that plays no other role anywhere in the model's structure, purely to switch off one term — and that addition would then have to be reconciled with F202's leptogenesis account, which currently depends on the opposite. This is precisely the situation the field-theory **genericity principle** (Gell-Mann's "totalitarian principle": *everything not forbidden is compulsory*) addresses: absent a symmetry reason for a term's coefficient to vanish, it is not technically natural to set it to zero by hand, and a generic UV completion is expected to generate it. The principle is standard vocabulary in exactly this context in the neutrino-mass literature (any renormalizable or higher-dimension completion that produces a Dirac-only spectrum must *impose* a symmetry — often explicit lepton-number conservation or an unbroken gauged $B\!-\!L$ — precisely to *forbid* the otherwise-generic Majorana operator).

## Argument S2 — removing the term reopens an established, gate-tier result

This is the sharper and fully mechanical half. F279 A1/A2 already showed that the F47 Majorana row is what closes the model's hypercharge system to the one-dimensional, gate-tier-certified line matching the observed Standard-Model charge ratios. This finding re-derives that system independently (not by importing F279's code) and adds the form F279 stopped short of stating explicitly.

**Setup.** Carrying $\nu_R$ with a hypercharge $y_\nu$ and a Dirac-type mass step (the ordinary F27/F41 mechanism every other fermion gets its mass from), the anomaly-cancellation and mass-step rows are:

$$
3y_Q+y_L=0,\qquad 2y_Q-y_u-y_d=0,\qquad y_d=y_Q-y_\phi,\qquad y_e=y_L-y_\phi,\qquad y_\nu=y_L+y_\phi.
$$

**Without the Majorana row** (`check_S2a`): this system has rank 5 over the 7 unknowns $\{y_Q,y_u,y_d,y_L,y_e,y_\nu,y_\phi\}$ — a genuine 2-dimensional nullspace — and solving explicitly shows $y_\phi$ **appears as a free symbol in the general solution**, not merely "underdetermined in the abstract." $y_\phi$ is exactly the parameter that fixes the quark-charge fractions ($y_u=y_Q+y_\phi$, $y_d=y_Q-y_\phi$) and the lepton/quark charge ratios.

**With the Majorana row** ($2y_\nu=0$, `check_S2b`): rank rises to 6, the nullspace collapses to 1 dimension, and solving gives exactly the F165/F279 certified line

$$
y_u:y_d:y_L:y_e:y_\nu:y_\phi \;=\; 4:-2:-3:-6:0:3 \quad(\text{units of }y_Q),
$$

reproducing the observed quark charges $\tfrac23,-\tfrac13$ at $y_Q=\tfrac16$.

**Control** (`check_control_dirac_only_hypothesis_does_not_reproduce_certified_ratios`): with the Majorana row dropped, $y_\phi=3y_Q$ (the certified, observationally-correct value) is not singled out by anything else already in the system — $y_\phi=y_Q$ or $y_\phi=\tfrac12y_Q$ solve the Dirac-only system equally well, and give the **wrong** quark charges. `check_S2c` further confirms no linear recombination of the *existing* five rows can substitute for the missing Majorana row; a genuinely new constraint is required, and the Majorana row is the only one the model's structure already supplies.

**The consequence.** A Dirac-only $\nu_R$ is not merely "a different, equally valid choice" for this model. It **reopens** a result the project already advertises as derived, gate-tier, and machine-verified over $\mathbb{Q}$ (F165/F279): that the Standard-Model hypercharge assignment — including the specific fractional quark charges — follows from the model's own structure rather than being entered as an input. Keeping the Majorana term is what keeps that result true. Removing it would require *also* re-imposing $y_\phi=3y_Q$ as a second, independent, currently unmotivated input — precisely the kind of free parameter the project's stated design philosophy (CLAUDE.md decision 6: elegant, fully-determined, no unexplained coincidences) exists to avoid.

## What this does and does not establish

**Established, mechanically (exact, $\mathbb{Q}$):**
- No lepton-number/$B\!-\!L$/matter-parity generator exists anywhere in the model's registered structure (S1).
- Dropping the Majorana row leaves $y_\phi$ free in the general solution; restoring it uniquely reproduces the certified F165/F279 line; no other existing row can substitute (S2).

**Argued, not proven as a theorem:**
- This is **not** a gauge-invariance no-go of the kind that makes a Dirac-only $\nu_R$ *impossible*. A Dirac-only completion of this model remains logically constructible — but only by (a) adding a global lepton-number symmetry found nowhere else in the model's structure, in tension with F202's own use of $L$-violation, **and** (b) accepting that the model's own gate-tier F165/F279 hypercharge-quantisation result no longer closes, reintroducing $y_\phi$ as a second free input.
- The genericity ("totalitarian principle") step — that an unforbidden term in a theory built from a single local CA rule is expected to appear — is a standard field-theory heuristic, not a derivation from the model's own dynamics; it is the same heuristic the neutrino-mass literature invokes whenever a Dirac-only spectrum is defended by *positing* lepton-number conservation.

**Verdict for row C4:** promoted from PARTIAL to a **stated, reasoned resolution**: within this model's actual structure — as opposed to the generic Standard Model, which has no analogous hypercharge-closure dependency — Majorana is the structurally required completion, *conditional on* (i) the model keeping its own already-certified F165/F279 hypercharge-quantisation result, and (ii) no protecting symmetry being added purely to forbid the term. Neither condition is a theorem; both are the model's own existing, already-adopted commitments. Keeping row C4 open pending a symmetry *theorem* that forbids Dirac outright would be holding the model to a standard the Standard Model itself does not meet; the two-part structural argument here (no protecting symmetry + dependence of an established result) is the kind of resolution the project's own "promotes the grade" criterion calls for when a symmetry no-go is not available.

## External anchor — what would settle this empirically, independent of the model

Two established results outside this project bear directly on Dirac-vs-Majorana in general:

- **Schechter–Valle "black-box" theorem** (Schechter & Valle 1982): whatever the underlying mechanism, an observation of neutrinoless double-beta decay ($0\nu\beta\beta$) implies a nonzero Majorana mass for at least one neutrino species, even if only generated radiatively at some loop order. This is the standard theoretical anchor for why $0\nu\beta\beta$ searches are considered decisive for the Majorana question in general, not model-specific to this project.
- **Current experimental status**: the KamLAND-Zen 800 full-dataset search for $0\nu\beta\beta$ in $^{136}$Xe (2024, complete dataset) sets $T_{1/2}^{0\nu} > 3.8\times10^{26}$ yr (90% CL), corresponding to an effective Majorana mass bound $m_{\beta\beta} < 28$–$122$ meV depending on nuclear matrix elements — no observation yet, so this remains the open empirical test rather than a settled fact.

Neither result depends on this model; they are named here because they are the concrete, falsifiable test that would confirm (a positive $0\nu\beta\beta$ signal) or leave open (continued non-observation, which cannot itself exclude Majorana) the physical nature of the neutrino, separate from the structural argument this finding makes about the model's own internal consistency.

---

## Exactness

| Result | Type | Residual |
|---|---|---|
| No protecting-symmetry generator registered (S1) | exact (name search over `dir()`) | 0 hits |
| $2y_\nu=0$ (Majorana bilinear hypercharge) | exact ($\mathbb{Q}$) | 0 |
| Dirac-only system: rank 5, nullspace dim 2, $y_\phi$ free (S2a) | exact ($\mathbb{Q}$, `sympy`) | — |
| With Majorana row: rank 6, nullspace dim 1, ratios $4:-2:-3:-6:0:3$ (S2b) | exact ($\mathbb{Q}$) | 0 |
| Control: alternate $y_\phi/y_Q$ ratios solve Dirac-only system equally well | exact ($\mathbb{Q}$) | — |

## Tests

`tests/findings/test_F341_majorana_forced_by_hypercharge_closure.py`, registry record `F341-majorana-forced-by-hypercharge-closure` (`tests/registry/particles.yaml`, kind `assertion`, tier `battery`). 5/5 checks PASS (`check_S1_no_protecting_symmetry_is_registered`, `check_S2a_without_majorana_yphi_is_free_in_the_nullspace`, `check_S2b_majorana_row_uniquely_closes_it_to_the_certified_line`, `check_S2c_no_other_established_row_fixes_yphi_instead`, `check_control_dirac_only_hypothesis_does_not_reproduce_certified_ratios`). Verified via `casim test --id F341-majorana-forced-by-hypercharge-closure`: PASS, 0.9s.

## Status

**Closed as a stated structural argument**, not a symmetry no-go. Row C4 moves from PARTIAL to resolved-by-argument; the completeness rubric text should read: *"Majorana is structurally forced given the model's own design (no protecting symmetry exists, and a Dirac-only alternative would reopen the certified F165/F279 hypercharge closure); this is an argument from structural consistency and genericity, not a gauge-invariance exclusion of Dirac."*

**Not re-opened:** the $Y_{\nu_R}=0$ forcing (F47/F279) — necessary for either Dirac or Majorana, not a discriminator between them (unchanged).

**Left open, explicitly out of scope here** (ledger row D4, not this row): the absolute Majorana scale $M_R$, and the Dirac CP phase $\delta_{CP}$ — both remain OPEN/ABSENT per `docs/status/open-derivations.md` D4, unaffected by this finding.

**Possible future sharpening:** a genuinely dynamical argument (rather than a consistency/genericity argument) — e.g., whether the F92/F93 $E_g$-condensate mechanism that generates the charged-lepton Dirac masses has any structural obstruction to generating a *comparably-sized* Dirac mass for $\nu_R$ specifically (as opposed to the deliberately tiny $M_D$ the see-saw needs) — was not attempted here and would be a stronger form of forcing if it closed. Flagged as a follow-up, not started.

---

*End of finding.*

## Reviewed & corrected

**2026-08-31 - 16:19** — cold-subagent adversarial review (`docs/reviews/F341-review-2026-08-31.md`), no memory of this session, independent device_bash access, forbidden from reading this file, its test module, and CL290. Verdict **CONFIRMED-NARROWER**: independently re-derived S1 (grep of casim.constants / casim.engine.gauge -- no protecting-symmetry generator found) and S2 (own sympy script, from scratch -- reproduced rank 5/nullspace 2 without the Majorana row, rank 6/nullspace 1 with it, and the exact SM ratio 4:-2:-3:-6:0:3) exactly, and additionally verified S2's "genuinely free" claim by exhibiting multiple self-consistent-but-wrong y_phi solutions. Adversarially searched for an alternative route to fix y_phi (found none; independently disproved the one plausible candidate, a mixed gauge-gravitational anomaly row, by showing it is linearly dependent once nu_R is properly included) and checked the genericity/"totalitarian principle" reasoning against the neutrino-model-building literature (confirmed standard, non-fallacious usage). One correction made: the headline word "forced" was tightened, here and in CL290, to state its conditionality explicitly (conditional on keeping F165/F279 and on no ad hoc protecting symmetry being added) rather than only in the body's hedge paragraph -- no mechanical content changed.
