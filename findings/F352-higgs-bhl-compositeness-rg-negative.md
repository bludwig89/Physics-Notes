# F352 — A Bardeen–Hill–Lindner compositeness/RG attempt at the F73 Cooper-pair Higgs, anchored at the model's own F79/F107 UV cutoff: a quantified negative result

**Date:** 2026-09-02 - 22:20
**Reviewed:** 2026-09-02 - 23:10 (inline self-review; see `docs/reviews/F352-review-2026-09-02.md`. Not an independent cold-context review — the session that built this finding also attacked it. Flagged, not hidden.)
**Status:** Confirmed (as a negative result) — 7/7 checks PASS (`tests/findings/test_F352_higgs_bhl_compositeness.py`, ~20 s). RG-improving the F73/F77 Cooper-pair compositeness condition down from the model's own derived UV cutoff predicts $m_t=226.56$ GeV (+31.3%) and $m_H=248.76$ GeV (+98.6%, essentially double), decisively excluded against the measured $172.57$ / $125.25$ GeV. This closes out the specific route asked for on ledger row **E8** (parameter **#18**) without closing the row itself: the model still has no derivation of $m_H$, and this finding narrows the space of remaining candidates by removing minimal single-channel top condensation at a Planck-scale cutoff from it.
**Script:** `tests/findings/test_F352_higgs_bhl_compositeness.py` (~20 s, stdlib only)
**Module:** `src/casim/engine/particles/derive_higgs_bhl_compositeness.py`
**Results:** `test-results/F352_higgs_bhl_compositeness.json`
**Cross-references:** [[F73-spin0-bound-pair-scalar]] (the exact kinematic ceiling and the missing-dynamics diagnosis this answers), [[F74-two-constituent-bound-state-binding]] (the contact-well no-go: gauge exchange is $\sim10^5\times$ too weak, deep binding needs criticality fine-tuning), [[F77-njl-gap-rpa-selfconsistent]] (the self-consistent mean-field/RPA no-go this RG-improves: $m_\sigma=2m_c$ at *every* coupling, and names "a full Bethe–Salpeter treatment" as the remaining hard build), [[F107-canonical-a-adopted]] (the exact lattice cutoff $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ used here as $\Lambda_\text{model}$, with no freedom to choose it), `docs/status/open-derivations.md` row **E8**.

---

## What was asked, and why this route

`docs/status/open-derivations.md` row E8 / parameter #18 asks for $m_H=125.25$ GeV as a bound-state mass (the model is Higgs-free by decision, CLAUDE.md #3/F27/F41), naming the F103/F104/F126 hadronic-binding programme as the template and flagging that "nobody has tried" the electroweak analogue. F73 supplies exact kinematics for the candidate object — a spin-0 singlet Cooper pair of two spin-½ constituents, the antisymmetric partner of the F69 photon's spin-1 pairing — but leaves the *binding dynamics* undetermined. F74 (a non-relativistic contact-well solver) and F77 (the same physics made fully self-consistent, an NJL gap equation + RPA ladder) both establish that **no natural coupling in the model's gauge sector produces sub-threshold binding**: the composite sits at or above $m_\sigma=2m_c$ for every value of the coupling, at every scale — this is an *identity* of mean-field/RPA order, not a numerical accident that a bigger coupling could fix. F77 names the remaining hard build explicitly: *"a full Bethe–Salpeter treatment with the F46 lattice dispersion... is where any genuine 125 GeV claim would still have to be earned."*

A literal lattice Bethe–Salpeter ladder is a substantial numerical build (still open). This finding attempts a different, standard, and directly comparable route to the same question: **renormalisation-group improvement of the compositeness condition**, following Bardeen, Hill & Lindner's treatment of Standard-Model top condensation (Phys. Rev. D41 (1990) 1647). The physics content is the *same* F77 relation ($m_H=2m_t$ at the compositeness scale) lifted from a single scale — where F77 shows it is an inescapable identity — to a running one, integrated down through 30+ decades of renormalisation-group flow. This is new relative to F77 (which works at one scale with no RG improvement) and is exactly the kind of dynamics the ledger row's OBE analogy was gesturing at: not a literal one-boson-exchange potential, but a genuine additional piece of dynamics (here, RG resummation) beyond the static mean-field result.

**The one respect in which this is *not* just a repeat of the 1990s literature:** BHL and its successors had to *choose* a compositeness/GUT scale by hand. This model does not get to choose. F79 derives the lattice cell size in closed form, and F107 adopts it as the canonical ruler:

$$a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.59782\ldots\quad(\text{exact, F79/F107}),$$

so the natural, parameter-free compositeness scale for a model-native contact interaction between two lattice constituents is the model's own UV cutoff,

$$\Lambda_\text{model}=\frac{E_\text{Planck}}{a/\ell_P}=1.8504\times10^{18}\text{ GeV}.$$

Nothing here is tuned to land anywhere convenient.

## Construction

Standard SM 1-loop RGEs for $(y_t,\lambda)$ (top-Yukawa-only; other Yukawas negligible), with $g_1,g_2,g_3$ supplied by their own decoupled closed-form 1-loop running from measured low-energy values ($\alpha_\text{em}(m_Z)=1/127.9$, $\sin^2\theta_W(m_Z)=0.23122$, $\alpha_s(m_Z)=0.1179$, all PDG):

$$16\pi^2\frac{dy_t}{dt}=y_t\Big[\tfrac92y_t^2-8g_3^2-\tfrac94g_2^2-\tfrac{17}{12}g_1^2\Big],$$
$$16\pi^2\frac{d\lambda}{dt}=24\lambda^2+12\lambda y_t^2-6y_t^4-9\lambda g_2^2-3\lambda g_1^2+\tfrac98g_2^4+\tfrac34g_1^2g_2^2+\tfrac38g_1^4,$$

$t=\ln\mu$, $g_1$ GUT-normalised. The BHL compositeness boundary conditions at $\Lambda_\text{model}$ are $y_t(\Lambda)\to\infty$ (the pair is point-like at the cutoff — a Landau-pole/triviality statement) and $\lambda(\Lambda)/y_t(\Lambda)^2\to\tfrac12$ (the same $m_H=2m_t$ ratio F77 derives as an exact identity, now imposed as a UV condition). Numerically, $y_t(\Lambda)\to\infty$ is implemented as a large finite stand-in $Y_0$, with $\lambda(\Lambda)=Y_0^2/2$, and the coupled system is integrated **down** from $\Lambda_\text{model}$ to $\mu=m_t$ (fixed-step RK4, stdlib-only per the D8 numerics-ratchet discipline — no new numpy/scipy import site). This is the standard BHL numerical procedure: as $Y_0\to\infty$ the down-integrated infrared values become $Y_0$-independent, because the nonlinear $y_t^3$ term erases the boundary value long before $\mu$ reaches $m_t$ (the "quasi-infrared-fixed-point" mechanism that is *why* minimal top condensation is predictive at all).

## Results

**A — Y0-convergence (the compositeness-ray criterion).** Scanning $Y_0\in\{50,100,300\}$ at fixed step count, $m_t$ and $m_H$ vary by $<0.01\%$ — the boundary stand-in has washed out, confirming the numerics are actually probing the compositeness ray and not an artefact of the chosen $Y_0$. A separate scratch cross-check against `scipy`'s adaptive Radau and RK45 integrators (session-local, not shipped — the module stays stdlib-only) agrees with the production RK4 result to $<10^{-4}$ relative.

**B — Headline, at the model's own cutoff.**

| quantity | predicted | measured | deviation |
|---|---|---|---|
| $m_t$ | $226.56$ GeV | $172.57$ GeV (PDG) | $+31.3\%$ |
| $m_H$ | $248.76$ GeV | $125.25$ GeV (PDG) | $+98.6\%$ (essentially double) |
| $m_H/m_t$ | $1.098$ | $0.726$ | still $51\%$ high |

**C — RG improvement does something, but not enough.** F77's flat mean-field ceiling is $m_H/m_t\equiv2$ at *every* coupling and *every* scale (no running). Here, 30+ decades of RG flow pull the ratio down to $1.098$ — real movement, driven mostly by $-8g_3^2$ suppressing $y_t$'s growth relative to $\lambda$'s — but the absolute masses do not move nearly enough: both $m_t$ and $m_H$ land far above measured.

**D — Not an artefact of the chosen $\Lambda$.** Scanning $\Lambda$ from $10^6$ to $10^{19}$ GeV, both predicted masses *decrease* monotonically as $\Lambda$ increases (the well-known BHL quasi-fixed-point plateau) and asymptote to a floor still far above measured even letting $\Lambda$ run several decades past the Planck scale ($\Lambda=10^{25}$ GeV still gives $m_t\approx218$ GeV) — so the exclusion is not sensitive to exactly which large $\Lambda$ is used, and in particular is not an artefact of $\Lambda_\text{model}$ specifically.

**E — Matches the historical verdict on minimal BHL top condensation.** The historical literature on minimal (single-condensate, no extra "topcolor" dynamics) top condensation at a GUT/Planck-scale cutoff states the model "predicted a Higgs mass roughly double the observed value" and is excluded by the measured masses. This run reproduces that qualitative and quantitative verdict (98.6% $\approx$ double) independently, at a cutoff fixed by the model rather than chosen for convenience — a nontrivial cross-check that the RG implementation is correct before trusting its verdict on the model-specific question.

## Verdict — negative, and honestly so

**Not derived here:** a value of $m_H$ matching $125.25$ GeV. Minimal single-channel top(-mass-scale) condensation, anchored at this model's own derived Planck-scale lattice cutoff, is **excluded** as the simultaneous origin of $m_t$ and $m_H$ — both predicted masses overshoot measured by $>30\%$ and the Higgs mass specifically by very close to a factor of 2, exactly the historically known failure mode of the minimal BHL scenario.

**What this adds beyond F74/F77:** those findings show the *static* mean-field/RPA theory cannot sub-threshold-bind at any coupling. This finding shows that RG-improving the *same* compositeness relation over the model's own full 30-decade hierarchy moves the mass ratio in the right direction (away from the flat ceiling of 2) but by nowhere near enough, and does so at a cutoff the model does not get to choose — closing off "maybe RG running rescues it" as an escape hatch from F77's no-go, with an actual number rather than an assumption.

**What remains open (ledger row E8 stays OPEN):** a literal lattice Bethe–Salpeter ladder (F77's own named next step) is not attempted here and could in principle behave differently from both the mean-field theory and its RG improvement — vertex corrections beyond the RPA bubble sum are the one channel not yet excluded by any of F73/F74/F77/F352. Extra strong dynamics beyond a single condensate coupling (the historical "topcolor" fix to minimal BHL) is also not excluded by this model — it would require a genuinely new force sector, which is a much larger claim than this finding attempts. Whether the F73 constituents are even correctly identified with top-scale quanta, versus some other condensate excitation (e.g. the second-shell $E_g$ sector of decision #7 — a *different* condensate, not shown here to be the same channel as F73's), is also untouched.

## Honest accounting of inputs

**Model-native (zero freedom):** $\Lambda_\text{model}=E_\text{Planck}/(a/\ell_P)$ — the *entire* reason this calculation is more than a repeat of BHL 1990 is that this number is fixed by F79/F107, not chosen. **External, standard SM low-energy anchors (not model outputs, exactly as F73/F74/F77 use PDG $m_t$, $m_H$ inline) — six of them, named in full rather than folded into "one input":** $m_Z=91.1876$ GeV, $m_t=172.57\pm0.29$ GeV, $v=246.22$ GeV, $\alpha_\text{em}(m_Z)=1/127.9$, $\sin^2\theta_W(m_Z)=0.23122$, $\alpha_s(m_Z)=0.1179$ — all PDG. $m_H^\text{obs}=125.25\pm0.17$ GeV (PDG) is the comparison target, not an input to the integration. **Method, not input:** the 1-loop SM RGEs for $g_1,g_2,g_3,y_t,\lambda$ are the standard textbook equations (e.g. Buttazzo et al., arXiv:1307.3536), used unmodified. **Approximation, flagged:** 1-loop only (2-loop would shift the headline numbers by a few percent, not by the factor of ~1.3–2 needed to reach measured); top-Yukawa-only (bottom/tau Yukawas are $10^3$–$10^4\times$ smaller and negligible at this precision); tree-level $y_t(m_t)=\sqrt2\,m_t/v$ (ignores $O(\alpha_s)$ threshold corrections that shift $y_t(m_t)$ by a few percent in the literature — again far short of what would be needed).

## Scope / next

- A literal lattice Bethe–Salpeter ladder (relativistic, full F46 dispersion, vertex corrections beyond RPA) is the one channel this finding does not touch and is where F77 already pointed.
- Extending the RG treatment to 2-loop, or adding a second (topcolor-like) contact channel, would sharpen this result further but is very unlikely to close a 30–100% gap.
- Whether the F73 pairing is the same physical channel as the second-shell $E_g$ condensate of CLAUDE.md decision #7 (a different sector entirely, governing charged-lepton generation structure) is an open identification question, not attempted here.

## Files
- Module: `src/casim/engine/particles/derive_higgs_bhl_compositeness.py`
- Script: `tests/findings/test_F352_higgs_bhl_compositeness.py`
- Results: `test-results/F352_higgs_bhl_compositeness.json`
- Review: `docs/reviews/F352-review-2026-09-02.md`
