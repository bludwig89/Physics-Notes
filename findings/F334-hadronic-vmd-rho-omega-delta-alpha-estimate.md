# F334 — A first model-internal handle on the hadronic piece: rho+omega narrow-resonance VMD captures ~10.2% of $\Delta\alpha_\text{had}^{(5)}(M_Z)$ from the model's existing couplings, and closes a tenth of B9's EW-leg gap

**Date:** 2026-08-30 - 11:34
**Checked:** 2026-08-30 — 8 PASS / 4 WEAKENS / 1 FAIL / 0 NOT RUN — **OVERSTATED**
**Test record:** record `F334-hadronic-vmd-estimate` (`tests/registry/interactions.yaml`, gate tier, entry-driven)
**Claim:** CL288 (see `docs/claims/CL288-hadronic-vmd-rho-omega-delta-alpha.md`)
**Module:** `casim.engine.interactions.running_alpha_lattice_bound` (L5 additions: `hadronic_vmd_narrow_resonance`, `ew_leg_with_hadronic_vmd`, `check_f334_hadronic_vmd`)
**Results:** `test-results/F334_hadronic_vmd_estimate.json`
**Cross-references:** [[F322-b9-running-alpha-ew-rederived-post-f277]] (§7 — the EW-leg residual this closes a fraction of; the missing $3.795$ in $\alpha^{-1}$), [[F311-gap5-three-numbers-adjudicated]] (the sibling B9 residual, a **different** open piece — the two-loop leptonic non-log constant — untouched here), [[F138-weinberg-gap-closure-4piv-matching]] / [[F231-weinberg-2over9-onshell-face-of-1over4]] (B6's own closed legs, not re-attacked), [[F103-p3-dynamical-pion-goldstone]] (KSRF $g_{\rho\pi\pi}=m_\rho/\sqrt2 f_\pi$, the model output this reuses), [[F128-nn-short-range-omega-repulsion]] / [[F240-omega-coupling-from-vector-sector]] ($\rho$–$\omega$ degeneracy and the vector universality posit — the **same class** of posit, applied here to the photon instead of the nucleon), [[F41-hypercharge-higgs-free]] / [[F42-quark-Y-and-dynamical-chi-kinetic]] (the quark hypercharge assignment $Q_u=2/3,\,Q_d=-1/3$ this derivation's $\times3$ isoscalar factor comes from), [[F151-scheme-constant-determined]] / [[F152-ir-coupling-the-irface]] (the strong-sector "hadronic piece" G3 defers to — a different face of the same declared gap), `docs/status/completeness-2026-08-20-prompts.md` §B6/§B9/§G3 (the shared open target this addresses).

---

## 1. What this addresses

Rubric row **B6** (Weinberg angle, with scale) is graded `QUANT`, and its stated residual — shared verbatim with **B9** and **G3** — is that the hadronic vacuum-polarization (VP) piece of $\Delta\alpha(M_Z)$ is declared out of scope everywhere in the model. F322 §7 quantified what that costs: feeding the model's own **leptonic-only** $\alpha(M_Z)$ (rather than the PDG value, which includes hadronic VP) into the $\sin^2\theta_W$ running **doubles** B6/B9's EW-leg residual, $+0.222\%\to+0.450\%$ — a factor $2.02$ traced to one missing number, $3.795$ in $\alpha^{-1}_{\overline{\text{MS}}}(M_Z)$.

Until now the model's position on that number was total silence: G3 states plainly that hadronic VP, HLbL, and the EW piece are "NOT claimed, by declared scope." This finding does not close that gap — closing it needs either the data-driven dispersion integral (external, as the Standard Model itself requires) or a genuine nonperturbative lattice-correlator computation of the model's own quark/gluon dynamics (a substantially larger undertaking, noted in §6 as future work). What it does is give the model its **first non-imported, quantitative estimate of a piece of it**, using machinery the model already has and has already validated elsewhere — the vector-meson sector built in F103/F128/F240 — rather than leaving the row at pure silence about a number every other closed leg of B6/B9 depends on.

## 2. The derivation

### 2.1 VMD leptonic width (standard)

A vector meson $V$ mixes with the photon through $\mathcal L\supset (e\,m_V^2/g_V)\,V_\mu A^\mu$, giving the standard leptonic width

$$\Gamma(V\to e^+e^-)=\frac{4\pi\alpha^2 m_V}{3\,g_V^2}.$$

### 2.2 Narrow-resonance dispersion integral (standard)

The dispersion relation $\Delta\alpha_\text{had}(s)=-\frac{\alpha s}{3\pi}\,\mathrm P\!\!\int ds'\,\frac{R(s')}{s'(s'-s)}$ with the zero-width limit of the standard spin-1 Breit–Wigner (PDG *Cross-section formulae*, §51.1; $\sigma_\text{peak}=12\pi\Gamma_{ee}/(m_V^2\Gamma)$, integrated) gives $\int\sigma(s')\,ds'=12\pi^2\Gamma_{ee}/m_V$, hence

$$R_V(s')=\frac{9\pi\,\Gamma_{ee}\,m_V}{\alpha^2}\,\delta(s'-m_V^2)\quad\Longrightarrow\quad \Delta\alpha_V(s)=\frac{3\Gamma_{ee}}{\alpha\,m_V}\cdot\frac{s}{s-m_V^2}.$$

At $s=M_Z^2\gg m_V^2$ ($m_V^2/M_Z^2\sim7\times10^{-5}$; V1 verifies the asymptotic form against the exact expression to $7.4\times10^{-5}$ relative), this reduces to $\Delta\alpha_V(M_Z^2)\simeq 3\Gamma_{ee}/(\alpha m_V)$.

### 2.3 Combine — $m_V$ cancels identically

Substituting §2.1 into §2.2, **the mass drops out**:

$$\boxed{\;\Delta\alpha_V(M_Z^2)=\frac{4\pi\alpha}{g_V^2}\;}$$

so the only input is the vector meson's photon coupling $g_V$ — and the model already has one, model-internal: F103/F240's KSRF output $g_{\rho\pi\pi}=m_\rho/(\sqrt2 f_\pi)=6.0109$ (model $f_\pi=92.07$ MeV, F123). Adopting F240's **same** universality posit — $g_{\rho,\text{EM}}=g_{\rho\pi\pi}$, flagged there as "the one modelling posit in the chain, not a theorem of the CA rule," here applied to the photon coupling instead of the nucleon coupling — gives

$$\Delta\alpha_\rho(M_Z^2)=\frac{4\pi\alpha}{g_{\rho\pi\pi}^2}=2.538\times10^{-3},$$

with **no new external input introduced by this finding**: $\Gamma_{ee}$ is not separately imported (it cancels algebraically, leaving only $g_V$), and $m_\rho$ drops out of *this* combination — but the honest input count for the *chain* is not zero. $g_{\rho\pi\pi}$ itself is built from F123's $f_\pi=92.07$ MeV, registered `exactness="external"` in the constants registry (an anchored, not derived, value), and from F128's **adopted** (not derived) $\rho$–$\omega$ mass degeneracy. What this finding adds beyond F103/F128/F240 is zero new inputs — it reuses those pre-existing external/adopted inputs rather than introducing any new ones.

### 2.4 The $\omega$ channel — quark-charge weighting, not baryon coherence (V2)

F128/F240 already used a factor of 3 for the $\omega NN$ *baryon* coupling ($g_{\omega NN}=3g_{\rho NN}$, coherent sum over three quarks' baryon number $\tfrac13$ each). The **photon** coupling is a different object — it weights by *electric charge*, not baryon number — and the model's own quark hypercharge assignment (F41/F42: $Q_u=\tfrac23,\,Q_d=-\tfrac13$) fixes it exactly:

$$\rho^0\sim\frac{Q_u-Q_d}{\sqrt2}=\frac{1}{\sqrt2},\qquad \omega\sim\frac{Q_u+Q_d}{\sqrt2}=\frac{1}{3\sqrt2}\qquad\Longrightarrow\qquad \frac{g_{\omega,\text{EM}}}{g_{\rho,\text{EM}}}=3\ \text{exactly}$$

(V2, sympy-exact rationals — `_quark_charge_photon_weights()`). This $\times3$ ratio is the standard $SU(3)$-flavour VMD relation between isoscalar and isovector photon couplings — textbook bookkeeping given quark electric charges, not novel physics specific to this model's CA rule. What V2 actually checks is narrower and still load-bearing: that the model's *own* quark-charge assignment (F41/F42) reproduces that known relation exactly (a control that flattens the ratio to 1 breaks V2 and only V2). That it numerically equals F128/F240's *different* baryon-coherence factor of 3 is a coincidence of $SU(3)$ charge bookkeeping across two distinct physical mechanisms (electric charge vs. baryon number) — not a re-derivation of one from the other, and not claimed as independent corroboration. With $g_{\omega,\text{EM}}=3g_{\rho\pi\pi}=18.03$:

$$\Delta\alpha_\omega(M_Z^2)=\frac{4\pi\alpha}{g_{\omega,\text{EM}}^2}=\frac{\Delta\alpha_\rho}{9}=2.820\times10^{-4}.$$

### 2.5 The total, and its honest fraction of the data-driven value

$$\Delta\alpha_{\rho+\omega}(M_Z^2)=2.820\times10^{-3}$$

Against the current data-driven anchor, Davier–Hoecker–Malaescu–Zhang 2020 (EPJC 80 (2020) 241): $\Delta\alpha_\text{had}^{(5)}(M_Z^2)=(276.0\pm1.0)\times10^{-4}=0.02760$ — **used only as an external comparison point, never as an input to §2.1–2.4** — the two-resonance model captures

$$\frac{\Delta\alpha_{\rho+\omega}}{\Delta\alpha_\text{had}^{(5),\,\text{DHMZ2020}}}=\mathbf{10.2\%}.$$

## 3. Honest self-check: how good is the universality posit? (V5)

Rather than asserting the universality posit is reasonable, this finding measures it, the same way F240 measured its own NN-coupling posits against the deuteron. Using the model's $g_{\rho\pi\pi}$ and $m_\rho=782.66$ MeV (F128 degeneracy) in §2.1's width formula predicts $\Gamma(\rho^0\to e^+e^-)=4.83$ keV, against the PDG measured $7.04$ keV — the universality-predicted width **undershoots** by $31\%$, i.e. the true photon coupling needs a **downward quench on $g_{\rho,\text{EM}}$ of $0.828$** relative to $g_{\rho\pi\pi}$ to match data.

This is not a new, ad hoc correction — it matches the **direction** F240 already found in two *other* channels built from the identical universality posit: $g_{\rho NN}$ needed a quench of $0.43$ and $g_{\sigma NN}$ needed $0.45$ (F240 §2, F126) to match the deuteron. The **magnitude** does not match — $0.828$ is a much smaller correction than $0.43$–$0.45$ — so this is not evidence of one universal quench factor; the claim is narrower: all three channels independently need a *downward* correction (none needed enhancement), a directional consistency check on the universality posit, not a magnitude one. Universality-derived couplings tend to overshoot their true values in this model in every channel checked so far, now measured a **third** time, independently, through the electromagnetic channel rather than either hadronic one. If the $17\%$ coupling quench (equivalently a $\times1.457$ enhancement of $\Gamma_{ee}$, since $\Gamma\propto1/g^2$) is applied, the captured fraction of DHMZ2020 rises toward $\sim15\%$ — still far short of $100\%$, and this finding does **not** apply that correction to its headline number (§2.5's $10.2\%$ is reported on the bare universality posit, unadjusted), because the quench itself is only measured for the $\rho$, and extending it to $\omega$ is unverified.

## 4. Effect on B6/B9's EW-leg residual (V6)

F322 §7's chain: leptonic-only $\alpha^{-1}_{\overline{\text{MS}}}(M_Z)=131.746$ (one loop $+$ F261's two-loop leading log, scheme-matched by the on-shell$\to\overline{\text{MS}}$ offset $0.976$) against PDG's $127.951$ — a gap of $3.795$, giving $\sin^2\theta_W=0.23226$ ($+0.450\%$) instead of the PDG-alpha result $0.23173$ ($+0.222\%$).

Subtracting this finding's $\Delta\alpha_{\rho+\omega}$ from the leptonic-only input (as a $\Delta(1/\alpha)=\alpha_0^{-1}\Delta\alpha_{\rho+\omega}=0.386$ shift):

| $\alpha^{-1}_{\overline{\text{MS}}}(M_Z)$ | source | $\sin^2\theta_W(M_Z)$ | residual |
|---|---|---:|---:|
| $127.951$ | PDG (full, incl. hadronic) | $0.231734$ | $+0.222\%$ |
| $131.746$ | model, leptonic-only (F322 §7) | $0.232260$ | $+0.450\%$ |
| $131.359$ | model, leptonic $+\ \rho{+}\omega$ VMD (**this finding**) | $0.232208$ | $\mathbf{+0.427\%}$ |

$$\text{gap closed}=\frac{3.795-3.408}{3.795}=\mathbf{10.2\%}$$

Small in absolute terms, but it is the **first non-zero, structurally-motivated movement** of this residual in the correct direction, at zero *new* free parameters (the only posit, universality, is inherited unmodified from F240 and is now cross-checked, not merely assumed, per §3).

**Note — these are the same ratio, not two independent confirmations.** §2.5's $10.2\%$ (captured fraction of DHMZ2020) and this section's $10.2\%$ (fraction of the $\alpha^{-1}$ gap closed) agree to within $0.33\%$ of each other because they are, to good approximation, the *same* quantity: the pre-existing gap of $3.795$ in $\alpha^{-1}_{\overline{\text{MS}}}(M_Z)$ is itself approximately $\alpha_0^{-1}\times\Delta\alpha_\text{had}^{(5),\text{DHMZ2020}}$ (both trace back to the same DHMZ2020 external value), so dividing this finding's $\Delta\alpha_{\rho+\omega}$ by either denominator lands close to the same number almost by construction. This is one result stated two ways, not two separate pieces of corroborating evidence.

## 5. Checks (6/6 + 2 controls, `test_F334_hadronic_vmd_estimate.py`)

| leg | statement | tier | result |
|---|---|---|:---:|
| V1 | $s\gg m_V^2$ asymptotic form matches the exact narrow-resonance dispersion integral | convergent | $7.4\times10^{-5}$ rel. err |
| V2 | $g_{\omega,\text{EM}}/g_{\rho,\text{EM}}=3$ exactly, from $Q_u=2/3,\,Q_d=-1/3$ alone | exact (sympy) | $0$ |
| V3 | $\Delta\alpha_{\rho+\omega}$ positive and $<\Delta\alpha_\text{had}^{(5)}$(DHMZ2020) | sanity | PASS |
| V4 | captured fraction $\in(3\%,30\%)$ — the physically sane band for two light resonances out of the full spectrum | quantitative | $10.2\%$ |
| V5 | universality coupling quench $\in(0.5,1.0)$, same direction as F240's two other channels | consistency | $0.828$ |
| V6 | adding the VMD piece moves $\sin^2\theta_W(M_Z)$ toward PDG and closes a bounded, nonzero fraction of the gap | quantitative | $10.2\%$ closed |

**Controls (D9/H2), verified red-and-only-there:**

| perturbation | reddens | why it must |
|---|---|---|
| `charge_weight_control=1.0` | **V2 only** | replaces the exact quark-charge $\times3$ with $\times1$ — breaks the one check built to test it |
| `dhmz_reference_control=0.001` | **V4 only** | replaces the DHMZ2020 external anchor with a wrong value — breaks only the plausibility-range comparison, not the physics (V1,V2,V3,V5,V6 do not reference it) |

8/8 PASS overall (6 legs + 2 controls verified).

## 6. What this closes, and what it does not

**Adds, does not close.** B6/B9/G3's grades are unchanged: the row's honest state remains that the *majority* of $\Delta\alpha_\text{had}$ is undetermined by the model. What changes is that "declared out of scope, unattempted" becomes "attempted with the model's own machinery, quantified at $10.2\%$ of the data-driven value, and the reason the rest is missing is now named precisely" — namely:

* **$\phi$ and heavier vector resonances are absent.** The model's vector sector (F103/F128/F240) only built $\rho$ and $\omega$; $\phi$ would need the model's strange-quark content wired into the same VMD chain, not attempted here.
* **The $\omega$ is treated as an idealized, unmixed isoscalar** (V2's exact $\times3$ assumes zero $\phi$ admixture). The physical $\omega$–$\phi$ system has a small but nonzero mixing angle away from ideal; this finding does not correct for it, so the exact-$3$ ratio is a model-internal idealization, not a claim about the physical $\omega$'s coupling to better than that approximation.
* **The multi-hadron continuum is absent.** Real $R(s')$ above $\sim1$ GeV is dominated by multi-pion and multi-hadron states this two-resonance model has no representation of.
* **Charm and bottom continuum contributions are absent** (part of DHMZ2020's "5-flavour" figure this finding compares against, not reproduced here).
* **The narrow-width approximation is a known, measured underestimate for the real $\rho$** (§3: the true coupling needs a $0.83\times$ quench, i.e. $\Gamma_{ee}$ needs enhancing by $1.46\times$ — the *physical* $\rho$ is broad, $\Gamma/m\approx19\%$, and a broad resonance's true dispersive contribution is known in the literature to exceed its zero-width approximation, "duality violation" — not corrected for here because the correction is only cross-checked for $\rho$, not $\omega$).

**This is structurally the same barrier the Standard Model itself faces**, stated precisely rather than left implicit: hadronic VP is *not* computable from a local perturbative QFT calculation at the needed precision even in the real Standard Model — it requires either the data-driven dispersion integral (what every other precision EW fit uses, external by necessity) or genuinely nonperturbative lattice QCD (a large, ongoing program even for the real theory). The model's own real-time lattice quark/gluon dynamics (F86, F94, F317, ...) is in principle the *right* kind of object to attempt the latter — computing the model's own electromagnetic current–current correlator and its spectral density directly, the lattice-QCD-style route — but that is a substantially larger undertaking than this finding and is left as the named next step (§7 of the B9 prompt already identifies the qualitatively-different open item — the two-loop leptonic non-log constant — as separate and untouched by this finding).

## 7. Provenance

* **New:** the VMD-narrow-resonance $\Delta\alpha_V=4\pi\alpha/g_V^2$ closed form (§2.1–2.3) applied to this model's fields; the confirmation that the model's own quark-charge assignment reproduces the standard $SU(3)$ isoscalar/isovector VMD ratio of 3 (§2.4 — the ratio itself is textbook, not new; what's new is checking the model's assignment against it), which numerically coincides with F128/F240's separate baryon-coherence factor of 3; the model-internal $10.2\%$ capture fraction and its effect on B6/B9's EW residual (§4, the same ratio stated two ways, not two independent results); the cross-check of the universality posit against the real $\rho\to e^+e^-$ width, agreeing in *direction* (not magnitude) with the two quenches F240 found already (§3).
* **Reused:** F103/F240's $g_{\rho\pi\pi}$ (KSRF, model $f_\pi$), F128/F240's $m_\rho=m_\omega=782.66$ MeV degeneracy, F41/F42's quark hypercharge assignment, F322's `two_loop_leading_log` and `_sin2_MZ`/`ew_leg_alpha_dependence` machinery (extended, not modified).
* **External anchors (comparison only, never inputs to the derivation):** Davier–Hoecker–Malaescu–Zhang, *A new evaluation of the hadronic vacuum polarisation contributions to the muon anomalous magnetic moment and to $\alpha(m_Z^2)$*, Eur. Phys. J. C 80 (2020) 241, $\Delta\alpha_\text{had}^{(5)}(M_Z^2)=(276.0\pm1.0)\times10^{-4}$; PDG $\Gamma(\rho^0\to e^+e^-)=7.04$ keV; PDG *Cross-section formulae for specific processes* §51.1 (the narrow-resonance Breit–Wigner normalisation used in §2.2).
* **Verification:** `tests/findings/test_F334_hadronic_vmd_estimate.py` (2026-08-30, 8/8 PASS incl. 2 controls), results `test-results/F334_hadronic_vmd_estimate.json`.

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| $g_{\omega,\text{EM}}/g_{\rho,\text{EM}}=3$ from $Q_u,Q_d$ | exact (sympy rationals) | $0$ |
| asymptotic $s\gg m_V^2$ form vs exact dispersion integral | machine/convergent | $7.4\times10^{-5}$ |
| $\Delta\alpha_{\rho+\omega}(M_Z)/\Delta\alpha_\text{had}^{(5)}$(DHMZ2020) | quantitative | $10.2\%$ |
| universality coupling quench vs PDG $\Gamma(\rho\to e^+e^-)$ | quantitative | $0.828$ ($-17\%$) |
| B9 EW-leg gap ($\alpha^{-1}$) closed | quantitative | $10.2\%$ ($3.795\to3.408$) |

## Tests

`tests/findings/test_F334_hadronic_vmd_estimate.py` — 8/8 PASS (6 checks V1–V6 + 2 D9/H2 controls, both verified red-and-only-there). Registry record `F334-hadronic-vmd-estimate` (gate tier).

## Reviewed & corrected

**2026-08-30 - 12:05** — attack pass: **OVERSTATED**. Found: Attack 2 (input laundering) FAIL — the "zero imported couplings" framing ignored that $g_{\rho\pi\pi}$ is built from F123's externally-anchored $f_\pi$ and F128's adopted (not derived) $m_\rho$; also a redundant unregistered `M_RHO_MEV` literal duplicating `nuc.M_OMEGA_DEFAULT`. Attacks 3/4/5/13 WEAKENS — the idealized (unmixed) $\omega$ assumption behind V2's exact $\times3$ went unstated; §3's quench-direction match with F240's two channels was stated without flagging the magnitude mismatch (0.828 vs 0.43/0.45); §2.4's $\times3$ ratio is standard $SU(3)$/VMD bookkeeping oversold as a fresh coincidence; CL288's `falsifier: stated` overstated present testability. Unprompted: the two headline "10.2%" figures ($\S$2.5, $\S$4) are the same ratio expressed two ways, not independent confirmations. Fixed: title and §2.3 reworded to name $f_\pi$/$m_\rho$ as reused external/adopted inputs rather than "zero imported"; module's redundant `M_RHO_MEV` literal removed in favor of `nuc.M_OMEGA_DEFAULT` (numerics re-verified bit-identical, 8/8 PASS incl. both controls); §2.4 reframed as confirming the model's charge assignment against a known $SU(3)$ relation, not an independent coincidence; §3 restated as direction-only agreement; §6 given an explicit idealized-$\omega$-mixing caveat; §4 given an explicit same-ratio note; Provenance's "New" bullet reworded to match; CL288's statement and falsifier reworded to match (see its own history). Rejected: none. Deferred: none — all four WEAKENS and the one FAIL were prose/registration fixes, not new physics.

## Status

Open: extending the same VMD chain to $\phi$ (needs the model's strange-quark sector wired into this coupling, not yet done); applying the §3 quench cross-check to $\omega$ as well as $\rho$ (untested, not applied to the headline number); the multi-hadron continuum and charm/bottom contributions (genuinely absent, not a gap this finding's method can close); the larger, separate undertaking of a first-principles lattice-correlator computation of the model's own electromagnetic current–current spectral function (the qualitatively correct route to a real closure, not attempted here). B9's *other* open target — the two-loop leptonic non-log constant (F311 §2.2, F322 §9) — is untouched and is a different residual entirely.
