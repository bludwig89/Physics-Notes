# F143 — The lattice fermion loop of the induced $U(1)_Y$ wrap stiffness on $U(x)$: transverse channel exactly zero (conjugation no-go), longitudinal channel per-mille of $v^2$ — the F138 matching scale is pinned by the $E_g$ sector, not by fermion loops

**Date:** 2026-06-12 - 12:55
**Status:** Computed + decisive. A structural no-go (exact, from the code's own gauging convention) plus a quantitative lattice loop with a measured magnitude band. The F138 follow-up ("induced-$Y$-kinetic-term lattice loop") is answered: the loop **cannot** replace NDA with a number — it proves the number lives in the $E_g$ condensate sector and bounds the fermion-loop correction to $\mu_\star$ at $0.08$–$0.18\%$.
**Script:** `tests/findings/test_F143_wrap_loop_stiffness.py` (5/5 blocks PASS, ~30 s)
**Production scan:** `tests/runners/run_F143_wrap_stiffness_scan.py` (+ `_slab.py` for large $L$)
**Results:** `test-results/F143_wrap_loop_stiffness.json` (scan), `test-results/F143_wrap_loop_stiffness_test.json` (test)
**Cross-references:** [[F138-weinberg-gap-closure-4piv-matching]] (the follow-up this closes), [[F41-hypercharge-higgs-free]]/[[F42-quark-Y-and-dynamical-chi-kinetic]] (the wrap construction whose gauge structure drives everything here), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $E_g$ sector that must own the wrap stiffness), [[F115-coupling-magnitudes-running-rotor]] (CM2 relocated the gap to a TeV matching; F143 pins which sector sets it).

---

## 1. Question and answer

F138 derived $\sin^2\theta_W=\tfrac14$ as the matching condition at the scale $\mu_\star$ where the abelian (wrap) sector's kinetic term turns on, identified $\mu_\star=4\pi v$ by NDA, and left as the follow-up: *compute the induced $Y$ stiffness from a lattice fermion loop on $U(x)$, to replace NDA with a number.*

**Answer:** the loop is computed, in both channels, and it is structurally incapable of supplying the stiffness:

| Channel | Coupling route | Induced stiffness | Status |
|---|---|---|---|
| Transverse (field-strength $F_Y^2$) | F42 kinetic wrap | **exactly 0**, all orders, all scales | conjugation no-go (§2, machine $\varepsilon$) |
| Longitudinal (Goldstone $f_\theta^2(\partial\theta)^2$) | mass step (only non-conjugate entry) | $\hat f\in[0.17,0.38]$ contact term, **no large log** | lattice loop (§3–4) |

Consequence (§5): the fermion sea contributes $0.16$–$0.36\%$ of $v^2$ to the wrap stiffness; $\mu_\star=4\pi f_\theta$ shifts by $<0.2\%$. The wrap decay constant — and hence the F138 matching scale — is owned $\gtrsim99.6\%$ by the $E_g$ condensate sector (F118). NDA is *not* replaced by a number; it is shown that the number must come from the $E_g$ stiffness, with the fermion loop bounded at the per-mille level.

## 2. The conjugation no-go (exact)

The model's own gauging convention (F42, `ca_hypercharge.kinetic_half_step_chi_u1y`) makes the kinetic step $U(1)_Y$-covariant by a site-centred Stueckelberg sandwich:

$$W_\alpha \;=\; e^{+i\alpha(x)Y/2}\; W(k)\; e^{-i\alpha(x)Y/2}.$$

This is a **unitary conjugation** for *any* static $\alpha(x)$ — the sea spectrum is exactly invariant (verified $\max|\delta\theta|=1.3\times10^{-15}$, check A). Therefore the kinetic-sector fermion loop induces **zero** abelian field-strength stiffness identically — not merely at tree level: at all loop orders, at every scale. This is the rigorous form of F138's premise "no $Y$ kinetic term": the lattice does not even provide a coupling through which a transverse $X_\mu$ could acquire one from the fermion kinetic sea. The only non-conjugate entry of the wrap is the **mass step** ($\eta^\dagger U(x)e^{i\alpha\Delta Y/2}\chi$, F27/F41) — so any induced wrap stiffness is strictly tied to chiral-mass generation, i.e. to the EWSB sector. This *derives* (rather than assumes) F138's claim that the matching is pinned to the EWSB scale.

## 3. The longitudinal loop: method

The induced wrap (Goldstone) stiffness from the filled Dirac sea: perturb the massive BCC Dirac walk $U=M(\tfrac m2,\alpha)\,\mathrm{diag}(W_+,W_-)\,M(\tfrac m2,\alpha)$ — $\eta$ on the '+' branch, $\chi$ on the '−' branch (F37), mass mixing with the wrap phase on the off-diagonal — by a static $\alpha(x)=a\cos(qx)$, and measure the sea-energy response

$$\delta\varepsilon=\tfrac{a^2}{4}\Pi(q),\qquad \Pi(q)=f^2q^2+O(q^4),\qquad \hat f\equiv \frac{4\pi^2}{m^2}\,\frac{\Pi(q)}{q^2}.$$

Two implementations, cross-validated: (i) exact supercell diagonalisation (all orders in $a$, sea energy via the pair-symmetric functional $-\tfrac1{2V}\sum_i|\theta_i|$); (ii) second-order eigenvalue perturbation theory on the walk unitary ($U$ normal ⇒ Rayleigh–Schrödinger applies to eigenvalues; $\delta\theta=\mathrm{Im}[\lambda^{(2)}/\lambda]$; exact parity degeneracies masked — their linear splittings cancel pairwise in the sgn-weighted sea sum). Agreement: $6\times10^{-4}$ relative (check B1, consistent with the $O(a^2)$ truncation of (i)). The site-local mass-step vertex has **no ordering ambiguity** — unlike any attempt to minimally couple the spectral kinetic kernel, which we showed breaks the Ward identity (and is, by §2, not the model's coupling anyway).

Validations: Ward/Goldstone $\Pi\propto q^2$ with no $q^0$ piece (global $U(1)$ exact; check B2, ratio $4.74$ vs $4$ with the residual $O(q^2)$); positivity; $L$- and $q$-systematics mapped in the scan (offset Monkhorst grids; $n{=}1$ rows where $q$ equals the grid spacing are systematically high and excluded; $m\lesssim0.2$ IR-unresolved at reachable $L$, excluded).

## 4. The number(s)

Across the resolved window ($m\in[0.3,0.6]$, $L$ up to 96, $q$ down to $0.065$):

$$\boxed{\;\hat f \,=\, \frac{4\pi^2 f^2}{m^2}\;\in\;[0.17,\,0.38]\;}$$

per unit wrap charge (physical species carry $(\Delta Y/2)^2=\tfrac14$). Key features: the magnitude is a small **lattice contact term**; there is **no large-log (Pagels–Stokar) enhancement** visible — $\hat f$ *decreases* toward smaller $m$ in the matched-resolution series (slope $\approx-0.23$ in $\ln(1/m)$ over $m\in[0.4,0.6]$), the opposite of the continuum $\ln(1/m)$ growth; a continuum estimate with its UV log at these scales would give $\hat f\sim5$–$10$. The two birefringent BCC branches ($\hat n_+\neq\hat n_-$, F37) entering the mass vertex are the plausible structural origin of the IR suppression. The strict $m\to0$ asymptotics is left open (IR-resolution-limited; would need $L\gtrsim40/m$ or an analytic IR subtraction) — it does not affect the conclusion, which only needs the magnitude bound.

## 5. Consequence for the F138 matching scale

The wrap decay constant is $f_\theta^2 = f_{E_g}^2 + \delta v^2_\text{fermion}$ with the loop's share (top-dominated):

$$\delta v^2_\text{fermion}\;=\;\sum_f \left(\tfrac{\Delta Y_f}{2}\right)^2 N_c^{(f)}\,\frac{\hat f\,m_f^2}{4\pi^2}\;\approx\;\tfrac14\cdot3\cdot\frac{\hat f\,m_t^2}{4\pi^2}\;=\;96\text{–}215\ \text{GeV}^2,$$

i.e. **$0.16$–$0.36\%$ of $v^2=(246.22\ \text{GeV})^2$** (check C). Since $\mu_\star=4\pi f_\theta$, the fermion loop moves the F138 matching scale by $0.08$–$0.18\%$ — utterly negligible against the $+0.22\%$ residual and the $e^{0.099}$ NDA offset. Hence:

1. F138's prediction chain is **stable** against the fermion loop (its one computable correction is per-mille).
2. The NDA→exact closure of $\mu_\star$ is relocated, with proof, to the $E_g$ condensate stiffness — the $\kappa_E<0$ spontaneous-gap sector of F118 ($W=1.46$, $\lambda_6\approx0.243$). Computing $f_{E_g}$ (the condensate's phase stiffness in lattice units) is now the single remaining item between NDA and an exact $\mu_\star$.
3. The no-go sharpens F138 §2: above the chiral-mass scale the abelian sector has *identically* zero induced kinetic term — the Landau-pole condition $\sin^2\theta_W=\tfrac14$ is exact at all scales above EWSB, not merely at one matching point.

## 6. Check summary (5/5)

| Check | Statement | Tier | Result |
|---|---|---|---|
| A | kinetic wrap = conjugation ⇒ sea spectrum invariant under any $\alpha(x)$ | exact / machine | $1.3\times10^{-15}$ PASS |
| B1 | walk-unitary eigenvalue PT == exact supercell | machine ($O(a^2)$) | rel $5.8\times10^{-4}$ PASS |
| B2 | $\Pi\propto q^2$, $\Pi>0$ (Goldstone Ward, positivity) | numeric | ratio 4.74 (q² ratio 4) PASS |
| B3 | $\hat f$ in measured band, no large-log | numeric | 0.30–0.37 (test pts) PASS |
| C | fermion share of $v^2<0.5\%$ ⇒ $\mu_\star$ shift $<0.2\%$ | exact arithmetic | 0.16–0.36% PASS |

## 7. Honest scope

- The longitudinal loop is a **static** response of the walk's filled sea; discrete-time effects enter only through the eigenphase structure (handled exactly).
- The mass step used is the canonical F27/F41 $\eta\!\leftrightarrow\!\chi$ rotation with the wrap phase on the off-diagonal; the repo's species-level conventions (Higgs vs conjugate branch) only flip the phase sign, which $\Pi$ is even in.
- $\hat f$'s strict $m\to0$ form is unresolved (IR-limited numerics); the physics conclusion uses only the magnitude bound over the resolved window plus the absence of log growth.
- $m_t=172.57$ GeV, $v$ from $G_F$; the share scales linearly in $\hat f$ — even $\hat f=1$ would give $0.94\%$, leaving the conclusion intact.

## 8. Files

- `findings/F143-wrap-loop-stiffness-nogo.md` — this finding
- `tests/findings/test_F143_wrap_loop_stiffness.py` — A/B1/B2/B3/C verification
- `tests/runners/run_F143_wrap_stiffness_scan.py`, `run_F143_wrap_stiffness_slab.py` — production scan
- `test-results/F143_wrap_loop_stiffness.json` — consolidated scan table
- `test-results/F143_wrap_loop_stiffness_test.json` — test output
