# F368 — Toward a model-native replacement for the imported EH98 transfer function (K11/S2): the sound horizon integrated on the model's own background lands 0.11% from Planck (16× better than the fitting formula already in the tree), the hydrogen recombination redshift derived from the model's own Rydberg energy via Saha reproduces the textbook ~26% equilibrium bias honestly, and swapping the model-native sound horizon into $\sigma_8$ localises the ~1.15% residual away from the sound-horizon scale

**Date:** 2026-09-05 - 02:45
**Status:** Confirmed — **6/6 checks PASS**, plus a two-axis control (D9/H2). S1/S2 are **exact-algebraic** (sympy literal zeros). D1, D2, D3, D4 are **quantitative**, each compared against an independent published number it can genuinely fail.
**Module:** `src/casim/engine/interactions/cosmology_transfer_function.py`
**Registry record:** `F368-transfer-function-scoping` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, `entry: run`)
**Results:** `test-results/F368_transfer_function_scoping.json`
**Claims topic:** `docs/design/session-claims.yaml`, session `cowork-k11-radiation-era-transfer-function`
**Attacks:** `docs/status/open-derivations.md` row **S2** ("THREE NAMED IMPORTS, EACH PRICED"), item (i); [[F288-structure-formation-zero-free-functions]] section 7's own open item: *"the ≈1% σ₈ residual IS the EH98 no-wiggle fit ... replacing it needs the model's own radiation-era Boltzmann hierarchy ... a real piece of work, not a tightening."*
**Cross-references:** [[F288-structure-formation-zero-free-functions]] (K11 — the σ₈ computation this extends; **not re-derived, only extended**), [[F182-friedmann-pressure-cosmology]] / [[F188-multicomponent-lcdm-cosmology]] (the multi-component Friedmann background this module integrates, unchanged), [[F125-p5-hydrogen-atom-em-bound-state]] (`casim.engine.particles.atom.rydberg_eV`, the model's own machine-precision hydrogen binding energy this module consumes), [[F297-bbn-light-element-abundances]] (η₁₀, the BBN baryon-to-photon ratio this module imports unchanged, same external input S2 item (iii) already prices), [[F79-structural-newton-constant]] / [[F284-rigid-lattice-expansion-and-primordial-state]] (why the background integrator needs no new gravity physics). External: Eisenstein & Hu 1998 (the transfer function being partially replaced); Hu & Sugiyama 1996 (EH98's own predecessor fitting formulas); Planck 2018 VI Table 2 (z_drag, r_drag, z\*); Peebles 1968 (the non-equilibrium recombination correction this finding names but does not build); *Status of the S₈ Tension: A 2026 Review* (arXiv:2602.12238, the current S8 landscape, unchanged by this finding).

---

## 1. What this finding is, and is careful not to overclaim

F288 (S1–S3) already forces $\mu=\Sigma=1$ **exactly** in the sub-horizon quasi-static regime linear structure formation needs. That means the model requires **no new gravitational physics** to treat linear photon–baryon–CDM perturbations: the governing equations are the ordinary GR-identical Einstein–Boltzmann system, sourced by ordinary matter, exactly as in ΛCDM. What the model does **not** yet carry is the radiation-era *matter* content's own dynamics — the coupled photon monopole/dipole and baryon-velocity tight-coupling system whose solution sets the sound horizon, the acoustic-oscillation phase, and the Silk damping scale a full transfer function needs.

Building the complete multipole Boltzmann hierarchy — a CAMB/CLASS-equivalent solver, $l_\text{max}\sim O(10)$, with a non-equilibrium (Peebles) recombination history — is genuinely out of scope for one session. That is F288's own "real piece of work" line, and this finding does not contradict it. Per the research prompt's own instruction, the first output is an honest feasibility **scoping** (§2), followed by the two pieces the scoping shows are tractable without the full solver (§3, §4), and a measurement of what they actually do to $\sigma_8$ (§5).

## 2. Scoping: what is already model-native, what is tractable, and what genuinely needs the full solver

| Bucket | Item |
|---|---|
| **Already model-native, no new physics needed** | Gravity sector: $\mu=\Sigma=1$ exactly (F288 S1–S3) — the perturbation equations are GR-identical. Background $H(a)$: full multi-component Friedmann (F182/F188). CDM long-wavelength growth shape (Meszáros stagnation): F288 D2, exact sympy zero. |
| **Built here, partial** | Sound horizon $r_s(z_\text{drag})$: direct integral on the model's own background (§3, D1/D2) — replaces a closed-form fitting formula. Recombination redshift: Saha equation with the model's own Rydberg energy (§4, D4) — replaces a fitted Hu–Sugiyama formula, its known equilibrium-approximation bias reported rather than hidden. |
| **Scoped, not built** | Silk damping $k_\text{Silk}$: needs the diffusion-order (quadrupole/polarization) tight-coupling expansion; EH98's own coefficient is itself only a phenomenological fit ($\pm20\%$), so no closed form exists to derive *against* — the target would be a genuine numerical diffusion integral, not a formula lookup. Non-equilibrium (Peebles effective 3-level atom) recombination: standard atomic physics, would close most of D4's bias — tractable, but not attempted this session. |
| **Still imported, named** | The CDM/baryon envelope $\alpha_c,\beta_c$ (EH98 eqs 11–12) and the baryon acoustic envelope $G(y)$ (eq. 14): EH98's own paper states these are calibrated against a numerical Boltzmann code (CMBFAST), with no closed form to derive. The acoustic oscillations themselves (EH98's full, non-no-wiggle eqs 15–19): need the actual multipole hierarchy solved as a function of $k$, not a scale. |
| **Requires the full multipole Boltzmann solver** | A minimal but genuine replacement of EH98's *shape* (not just its scale-setting numbers) needs photon monopole/dipole ($\Theta_0,\Theta_1$) + baryon velocity in the tight-coupling approximation, transitioning to a truncated free-streaming hierarchy ($l_\text{max}\sim6$–$10$) at recombination, sourced by the model's own $\Phi,\Psi$ (already GR-identical, F288), with the Peebles recombination history above. Estimated at several sessions of numerical development and validation against known Boltzmann-code output — not a single-session task. |

This is the honest reason this finding delivers two pieces rather than a rushed partial solver: the two pieces above are the ones the scoping shows are reachable with physics and constants the model **already owns** (F125's Rydberg energy, F182/F188's background integrator), everything else genuinely needs machinery the model does not yet have.

## 3. Sound horizon, by direct integration on the model's own background

The sound speed of the tightly-coupled photon–baryon fluid is standard:
$$c_s(a)=\frac{1}{\sqrt{3(1+R(a))}},\qquad R(a)=\frac{3\rho_b}{4\rho_\gamma}=\frac{3\,\Omega_b}{4\,\Omega_\gamma}\,a.$$

**Check S1 (exact).** As $a\to0$, $R\to0$ and $c_s\to1/\sqrt3$ — a sympy symbolic limit, literal zero residual against the target.

**Check S2 (exact).** $R(a)/a$ is a sympy-verified constant: $d(R/a)/da\equiv0$. $R$ is forced exactly linear in $a$ by $\rho_b\propto a^{-3}$, $\rho_\gamma\propto a^{-4}$ — no fit, no approximation.

The comoving sound horizon is then the ordinary conformal-time integral
$$r_s(a_\text{end})=\frac{c}{H_0}\int_0^{a_\text{end}}\frac{c_s(a)}{a^2E(a)}\,da,$$
with $E(a)=H(a)/H_0$ read from `cosmology_growth.E2` — **F182/F188's own confirmed multi-component background** (radiation + matter + $\Lambda$), not EH98's closed-form approximation (which drops $\Lambda$ and fits the radiation/matter transition). Hand-rolled Simpson quadrature, D8-compliant; the integrand is finite and smooth as $a\to0$ ($c_s\to1/\sqrt3$, $a^2E(a)\to\sqrt{\Omega_r}$), so a plain linear grid from $a\sim0$ is safe.

**Check D1.** Integrating to the (imported) Planck drag redshift $z_\text{drag}=1059.94$:
$$r_s^\text{model}=146.923\ \text{Mpc}\qquad\text{vs}\qquad r_\text{drag}^\text{Planck}=147.09\ \text{Mpc}\qquad(-0.114\%).$$

**Check D2.** `cosmology_growth.transfer_eh98` already carries a closed-form fitting-formula approximation for this same scale (its internal `s = 44.5·ln(9.83/ωm)/√(1+10 ωb^0.75)`, EH98's own eq.-26-style shape approximation):
$$s_\text{EH98 fit}=149.824\ \text{Mpc}\qquad(+1.859\%\ \text{vs Planck}).$$

The model's direct integration is **16.4× closer to Planck's own measured $r_\text{drag}$** than the fitting formula already coded in the tree. This is a genuine, quantified improvement: it replaces one imported approximation with a first-principles integral of physics the model already owns (F182/F188), at no new cost.

## 4. Hydrogen recombination redshift, from the model's own Rydberg energy

The plain (equilibrium) Saha equation for hydrogen,
$$\frac{X_e^2}{1-X_e}=\frac{1}{n_b(z)}\left(\frac{m_eT}{2\pi\hbar^2}\right)^{3/2}e^{-B_\text{ion}/T},$$
needs exactly two inputs the model already has: the ionisation energy $B_\text{ion}$ (F125's Rydberg formula at the physical $e$–$p$ reduced mass, `atom.rydberg_eV`, giving $13.5983$ eV against CODATA's $13.6057$ eV) and the baryon-to-photon ratio $\eta_{10}=6.137$ (`cosmology_bbn.ETA10_PLANCK` — the same external BBN input S2 item (iii) already prices, unchanged here).

**Check D4.** Solving $X_e(z)=0.5$ by bisection:
$$z_\text{rec}^\text{Saha}=1378.62\qquad\text{vs}\qquad z_*^\text{Planck}=1089.92\qquad(+26.49\%).$$

This is **not a bug** — it is the textbook Saha-vs-true discrepancy, reproduced from the model's own atomic-physics constant. Plain Saha assumes instantaneous equilibrium; the true recombination history is delayed by the 2s–1s two-photon decay bottleneck (Peebles 1968), so equilibrium recombination happens too early (too high a redshift). The ~25–30% band is the well-known size of this omission in the literature, and the model's own Rydberg energy reproduces it to the percent, honestly reported rather than hidden. Closing it needs the Peebles effective-3-level-atom treatment — standard atomic/recombination physics, not model-specific, and correctly scoped in §2 as tractable-but-not-attempted this session.

## 5. What the sound-horizon substitution actually does to $\sigma_8$ — a diagnostic, not a fix

Substituting the model-native $r_s$ (§3) for EH98's internal fitting-formula $s$ inside the (otherwise completely unchanged) EH98 no-wiggle shape formula, and re-running F288's own $\sigma_8$ integral exactly (same $A_s$, $n_s$, $D(1)$, growth factor, window function):

| | $\sigma_8$ | vs Planck ($0.8111$) |
|---|---|---|
| EH98 internal fitting-formula $s$ (F288, unchanged) | $0.820389$ | $+1.146\%$ |
| Model-native $r_s$ substituted | $0.820495$ | $+1.158\%$ |
| **Shift** | $+0.0129\%$ | — |

**Check D3.** The shift is *two orders of magnitude* smaller than the residual itself. This is informative precisely because it is small: it shows the ≈1.15% $\sigma_8$-vs-Planck residual F288 reports is **not located in the sound-horizon scale** — which the model reproduces to 0.11% (§3, D1) — but in EH98's missing acoustic wiggles and Boltzmann-calibrated envelope functions (§2, "still imported, named"), which this finding does not touch. That is a genuine diagnostic result: it tells the next session exactly where the residual lives and, as importantly, where it does *not* — the sound-horizon integral is not the bottleneck, so a future attempt at closing S2 should not spend effort re-deriving it more precisely; it should go straight at the acoustic-wiggle / envelope machinery named in §2's last two rows.

## 6. Control (D9/H2)

Two independent perturbation handles, each required to redden a named subset of checks:

| Perturbation | Reddens | Measured |
|---|---|---|
| `z_drag_multiplier=1.1` (10% high) | D1, D2 | $r_s^\text{model}$ moves to $-6.19\%$ vs Planck (past the 1% tolerance); EH98's own $z_\text{drag}$-independent internal fit does not move, so D2's comparison flips too |
| `b_ion_multiplier=1.2` (+20% ionisation energy) | D4 | Saha bias moves to $+52.8\%$, outside the known $15$–$40\%$ band |
| `b_ion_multiplier=0.8` (−20%) | D4 | Saha bias moves to $+0.34\%$ — spuriously near zero, which would look like an improvement but is actually the check losing its grip on the real physics; caught in either direction |

Sweep handles: `casim test --id F368-transfer-function-scoping --param z_drag_multiplier=1.1` and `--param b_ion_multiplier=1.2`.

## 7. Checks (6/6, plus control)

| # | Check | Class | Result |
|---|---|---|---|
| S1 | $c_s(a\to0)=1/\sqrt3$ exactly (sympy limit) | exact | PASS |
| S2 | $R(a)/a$ constant, $d(R/a)/da\equiv0$ (sympy) | exact | PASS |
| D1 | Model-native $r_s(z_\text{drag})$ vs Planck $r_\text{drag}$: $-0.114\%$ | quantitative | PASS |
| D2 | Model-native $r_s$ vs the EH98-internal fitting formula: $16.4\times$ improvement | quantitative | PASS |
| D3 | $\sigma_8$ shift from the substitution: $+0.013\%$, two orders below the residual — localises it | quantitative | PASS |
| D4 | Saha $z_\text{rec}$ from model's own Rydberg energy: $+26.49\%$ bias, in the known $15$–$40\%$ band | quantitative | PASS |
| C1a | Control: `z_drag_multiplier=1.1` reddens D1, D2 | control | PASS |
| C1b | Control: `b_ion_multiplier=1.2` reddens D4 | control | PASS |

## 8. What this moves, and what it does not

**Moves:** S2 (`docs/status/open-derivations.md`) item (i) from "imported, priced, untouched" to "two of its scale-setting numbers replaced with model-native derivations, the gap to a full replacement precisely scoped and localised." K11 stays `PARTIAL` — this finding does not change F288's grade, its σ₈ headline number (which still uses the unchanged EH98 envelope, §5), or its falsifier. The DES Y6 $S_8$ tension discussion is untouched.

**Does not move:** F288's own zero-free-function structure result (S1–S3, D1, D2 of F288 — not re-derived here, per the research prompt's own instruction). The recombination-redshift bias (D4) is *reported*, not closed; closing it is atomic physics (Peebles), correctly named as future work, not a defect of this finding.

**Open, and specified:** (1) the Peebles effective-3-level-atom non-equilibrium recombination correction — would close most of D4's ~26% bias, standard physics, not attempted. (2) The Silk damping scale — scoped in §2 as needing a genuine diffusion-order tight-coupling integral, for which EH98's own coefficient is only a phenomenological fit, so there is no closed form to derive against; a numerical attempt is the natural next piece. (3) The full multipole Boltzmann hierarchy needed to replace EH98's shape (not just its scale-setting numbers) — sized in §2's last row as several sessions of numerical development, not a single-session task.
