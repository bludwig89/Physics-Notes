# F380 — Cluster decomposition: F331's residual named as one object (completeness row A10, QUANT → PARTIAL)

**Status:** Confirmed — **3/3 PASS**, one declared control verified red **and red only where expected**.
**Checked:** 2026-09-10 - 12:15 — cold-subagent blind re-derivation + adversarial referee, 13-point attack pass: **CONFIRMED-NARROWER**. The central promotion claim (F331's mass-dependent residual table collapses to one named object) survived and was independently re-derived by a *different* route; the mechanism section and headline constant as originally written were wrong (p=1, "same as the continuum Yukawa propagator") and are corrected here (p=3/2, an axial branch point the original version missed). See "Reviewed & corrected" below.

2026-09-10 - 00:xx (mechanism corrected 2026-09-10 - 12:15, post review)

## The question

Completeness row A10 (cluster decomposition / no-signalling) is graded **QUANT**. F290 established no-signalling exactly and the free-field causal cone at machine precision; F331 extended cluster decomposition to the interacting, 3-D BCC theory (mean-field NJL), closing F290's residual 1. But F331's own free-fermion validation — the measured-vs-exact ratio of the (100)-axis decay rate $\kappa_{100}(m)$ against the model's own dispersion — left a **mass-dependent tolerance table** as its residual: ratio $1.53$ at $m=0.05$, shrinking monotonically to $0.95$ at $m=0.95$. The state-of-model rubric's QUANT→PARTIAL rung is specific about what promotes a row: *"name the residual — turn 'agrees to x%' into 'derived up to this one object' — a named seam is strictly more informative than a tolerance, even at the same number."* F331's table is a tolerance, not a named object.

The prompt for this row named a concrete first step: **compute $\kappa_{100}$ at the mass the self-consistent NJL gap equation actually selects** ($m^*$, F331 Sec.2) rather than the registry's default $m=0.5$, and check whether the ratio collapses to 1 there — which would mean the mass-dependence is a red herring, collapsing the whole table down to F290's separate 1-D exponent shortfall alone.

## First step: is $m^*$ special?

Using F331's own unmodified `axis100_measured_kappa` and `solve_gap_equation` (`casim.engine.interactions.qi_cluster_interacting_3d`, both untouched by this finding), at $g=2.9$ the gap equation gives $m^*=0.605496$ (matches F331 Sec.2 to the reported precision). Evaluating F331's measured/exact ratio there:

$$\kappa_{100}(m^*) = 1.21552 \ (\text{exact}), \qquad \kappa_\text{measured}(m^*) = 1.34874, \qquad \text{ratio} = 1.10960$$

L-converged: stable to 5 significant figures from $L=128$ through $L=512$ at the adaptive window $(3,8)$. **This is not 1 to the numerical floor.** The literal hypothesis — that $m^*$ is a special mass where the closed form and the numerics coincide exactly — is **falsified**.

But that is not the end of the question. What matters for the promotion is not whether $m^*$ is special, but whether it is *unremarkable* — i.e. whether it sits on the exact same curve as every other mass in F331's table, which would mean the entire table (mass-dependence included) is explained by a single mechanism rather than by 18+ separate coincidences.

## The mechanism

F331's `_fit_kappa` fits a **pure exponential**, $\ln|C(r)| = a - \kappa r$, to the model's own periodic (100)-axis correlator. A 3-D lattice Green's function does not decay as a pure exponential, and **two independent effects** contribute an algebraic prefactor $r^{-p}$ on top of it:

1. **Transverse (stationary phase).** Near the dominant saddle $(b,c)=(0,0)$ the pole-locus $R(b,c)^2$ is quadratic to leading order, so Gaussian-integrating the 2 real transverse momenta contributes $r^{-2/2}=r^{-1}$.
2. **Axial — a branch point, not a simple pole.** The dispersion is $\omega(a)=\arccos(n\,u(a))$, and *at* the pole condition $n\,u(a)=1$, $\omega$ vanishes as a **square root**: $\omega(a_0+\epsilon)\sim\sqrt{2\epsilon}$ (since $\arccos(1-\epsilon)\sim\sqrt{2\epsilon}$ for small $\epsilon$), not linearly. $1/(2\omega)$ therefore has an inverse-square-root **branch-point** singularity at the pole, not a simple pole. A 1-D Fourier transform of a $(k-k_0)^{-\alpha}$ branch-point singularity contributes $r^{\alpha-1}$ (Watson's-lemma endpoint asymptotics: a simple pole, $\alpha=1$, gives $r^0$ — the ordinary Yukawa case, and *not* this model's case); here $\alpha=1/2$, contributing an **extra** $r^{-1/2}$.

$$p = \underbrace{1}_{\text{transverse}} + \underbrace{\tfrac12}_{\text{axial branch point}} = \tfrac32$$

Fitting a pure exponential to a function with this $r^{-3/2}$ prefactor over any finite window biases the extracted slope by an amount set by *where the window sits*, not directly by the mass — the mass only enters `_adaptive_window`'s placement.

## The measurement

A free-power refit (fitting the prefactor exponent as a third parameter) was tried and **rejected**: on F331's short adaptive windows (as few as 3 points at the high-mass end) it is numerically ill-conditioned. What replaces it is not a floating fit at all — it is the **exact, closed-form OLS bias** that a *known, theoretically fixed* power $p$ produces in a plain 2-parameter $(a,\kappa)$ linear fit: if the true model is $\ln|C(r)| = \text{const} - p\ln r - \kappa r$, the OLS slope of a plain linear fit (which omits the $-p\ln r$ term) is biased by exactly

$$\kappa_\text{measured} - \kappa_\text{exact} = p \cdot \frac{S_{r,\ln r}}{S_{rr}}, \qquad S_{rr}=\sum(r_i-\bar r)^2,\ \ S_{r,\ln r}=\sum(r_i-\bar r)(\ln r_i - \overline{\ln r})$$

over F331's own fit window — ordinary linear-regression bookkeeping, no new fit, no free parameter. Solving for the *implied effective power*,

$$p_\text{eff}(m) := \bigl(\kappa_\text{measured}(m) - \kappa_{100}(m)\bigr) \Big/ \frac{S_{r,\ln r}}{S_{rr}}$$

should equal the theoretical $p=3/2$ if the mechanism above is the whole story (to the order this leading-term analysis captures).

Measured (`test-results/F380_cluster_asymptotic_series.json`), scanning 18 masses across the entire admissible range $0.05 \le m \le 0.90$ at $L=256$ (L-converged), using **F331's own $\kappa_{100}$, unmodified**:

$$p_\text{eff} = 1.489 \pm 0.039 \qquad (2.65\%\text{ relative spread}), \qquad \left|\frac{p_\text{eff}-3/2}{3/2}\right| = 0.71\%$$

against the raw ratio's own relative spread of $7.59\%$ (mean $1.161$) over the same 18 masses — a $2.9\times$ tighter descriptor, and one that lands **within measurement scatter of an independently, first-principles-derived number**. And at the dynamically-selected mass:

$$p_\text{eff}(m^*=0.6055) = 1.465, \qquad z = -0.62\sigma \text{ from the scan mean}$$

$m^*$ sits comfortably inside the same distribution as every other tested mass — **unremarkable**, which is exactly the useful negative result the first step was designed to surface: not "$m^*$ is special" (falsified above), but "$m^*$ needs no special treatment, because the entire table — $m^*$ included — is one object."

### Control

Using the closed form for the **wrong** BCC axis as the reference ($\kappa_{110}$, correct for the (110) axis, not (100)) while still measuring the (100)-axis correlator breaks $p_\text{eff}$'s meaning outright: mean shifts to $5.10$ (far from the theoretical $1.5$) and relative spread jumps to $33.6\%$. This shows $p_\text{eff}$'s meaning is tied to measuring against the *specific* closed form `axis100_kappa_exact`, not a generic artifact of the OLS-bias rescaling. Verified via `casim test --control --id F380-cluster-asymptotic-series-K`: C1 and C2 go red, C3 does not (expected — even against the wrong reference, $m^*$ remains unremarkable within that looser distribution).

## What this promotes

**QUANT → PARTIAL.** F331's Piece-1 residual is no longer an 18-entry (or continuum-of-masses) tolerance table; it is **one named quantity**, the algebraic-prefactor power $p_\text{eff} = 1.49 \pm 0.04$ — matching a theoretically **derived** value ($3/2$, from the dispersion's own branch-point structure) to under $1\%$, verified mass-independent across the entire admissible range **including** the dynamically NJL-selected mass $m^*$. This is exactly the shape of promotion `.claude/commands/state-of-model.md` Sec.7.1 names for QUANT→PARTIAL: a named seam in place of a tolerance, anchored to an independent theoretical target rather than merely self-consistent.

## What remains (PARTIAL, not MACHINE)

1. **$p_\text{eff}=1.489$ is measured against a theoretically derived target, not yet a full symbolic derivation of the sub-leading term.** The branch-point argument above is a leading-order Puiseux/Watson's-lemma argument; it explains the *power*, not the $\sim\!1\%$ mean offset from $3/2$ or the $\sim\!2.6\%$ point-to-point scatter. The next rung (PARTIAL→MACHINE) needs a full sympy expansion of the BCC dispersion's phase at the saddle to the order that fixes the sub-leading coefficient symbolically, verified to the numerical floor. Not attempted here.
2. **The high-mass edge is excluded, not hidden.** Above $m\approx0.92$, `_adaptive_window`'s underflow cap collapses the fit window to its 3-point floor and the measurement stops converging with $L$ (checked directly: $m=0.95$ gives inconsistent values between $L=256$ and $L=512$). The declared range $0.05\le m\le0.90$ is the region checked L-convergent.
3. **F290's separate 1-D exponent shortfall (its own item 2) is untouched.** This finding's object is a 3-D, different measurement; it does not settle F290's 1-D question.
4. **S-matrix-level clustering** is still not addressed, as in F290 and F331.

## Falsifiability

If a symbolic steepest-descent computation of the sub-leading coefficient at the BCC saddle gave an implied power inconsistent with $p\approx3/2$ (a direct numerical power-law fit at wide, well-converged windows should reproduce the same value — checked during review, see below), that would falsify the mechanism proposed here. If $p_\text{eff}$'s relative spread failed to hold under a genuinely independent numerical method (e.g. a non-FFT, arbitrary-precision direct summation of the correlator, which would also let the high-mass edge be checked), that would likewise undercut the claim.

## Prior art

The algebraic prefactor of an asymptotically exponential lattice/continuum Green's function is standard lattice-QFT and mathematical-physics content. What is new here is (a) identifying that the model's dispersion has a *branch-point*, not a simple-pole, axial singularity — giving $p=3/2$ rather than the naive continuum-massive-propagator $p=1$ — and (b) showing this single power explains F331's entire mass-dependent residual table via the exact OLS bias formula, with no free parameters.

## Reviewed & corrected

**2026-09-10 - 12:15** — cold-subagent review (blind re-derivation + adversarial referee, both independent of each other and of the author). **Verdict: CONFIRMED-NARROWER.**

The central promotion claim — F331's 18-entry mass-dependent tolerance table collapses to one named, mass-independent object, and $m^*$ is unremarkable within it — survived and was *strengthened*: both the blind subagent (working from a non-leading claim card, forbidden from reading this finding) and the adversarial referee (reading everything, including the first agent's report) independently derived that the model's dispersion $\omega(a)=\arccos(n\,u(a))$ has a square-root **branch point** at the axial pole, not a simple pole — contributing an extra $r^{-1/2}$ to the correlator's algebraic prefactor beyond the $r^{-1}$ from the 2 transverse stationary-phase dimensions, for a total power $p=3/2$. This is a genuine correction: **the version of this finding written before review claimed $p=1$** ("2 transverse real momenta integrate out via stationary phase… EXACTLY the continuum static Yukawa propagator's $e^{-\kappa r}/r$… same structure, same reason"), used a crude window-midpoint proxy $K:=(\kappa_\text{measured}-\kappa_{100})\cdot\bar r_\text{mid}$, and reported $K=1.71\pm0.04$ as the named residual — a number with no independent theoretical anchor to check it against.

Both cold agents, working independently, found the $p=1$ mechanism wrong (verified three ways: (a) direct expansion of $\arccos(1-\epsilon)\sim\sqrt{2\epsilon}$ at the pole, confirmed numerically to be a clean square-root branch, not a linear zero; (b) a direct free-power fit at wide, well-converged windows ($L=512$) with $\kappa$ fixed to the exact closed form gives $p_\text{fit}\in[1.48,1.52]$ across $m=0.1$–$0.5$; (c) the exact OLS bias formula, using $p=3/2$, gives a mean normalized bias of $0.996$–$0.999$ (essentially exactly 1) across the whole mass range, versus $1.49$–$1.494$ at the wrong $p=1$ — a materially cleaner, theoretically anchored result). Both routes converged on the same corrected power independently, which is the review's strongest evidence: this is not model-fitting after the fact.

**Fixed at the source**, not just re-labelled: the module's mechanism docstring, the `effective_power`/`check_named_residual_K` functions (replacing the crude $r_\text{mid}$ proxy with the exact OLS-weighted $p_\text{eff}$, and the registry gate's C2 check from "beats the raw ratio" to "matches the theoretically derived $p=3/2$ to $<5\%$"), the test driver, the registry record's `notes`, `docs/claims/CL286`, and `docs/status/completeness-2026-09-08.md` row A10 were all updated to the corrected mechanism and the corrected headline number ($p_\text{eff}=1.489\pm0.039$, replacing $K=1.71\pm0.04$). The review's other finding — that "3× tighter than the raw ratio" is a normalization-invariant fact true for *any* choice of assumed power, and therefore does not by itself validate the specific mechanism — is accepted; the finding now leads with the match to the independently-derived theoretical power ($<1\%$ deviation) as the load-bearing evidence, not the tightening factor alone. The row-level promotion (QUANT→PARTIAL) is unaffected by the correction — the central claim survives on corrected, and now stronger, grounds. Full report: `docs/reviews/F380-review-2026-09-10.md`.
