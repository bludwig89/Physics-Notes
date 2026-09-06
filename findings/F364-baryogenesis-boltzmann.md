# F364 — Rubric row K6 (baryogenesis): a real Boltzmann computation of the baryon asymmetry — replacing F202's Sakharov-conditions checklist with an actual number. At the model's OWN native F201 texture masses (M₂≈0.40 GeV, M₃≈5.60 GeV), the free CP phase alone caps ~10–11 decades short of measured Y_B; the free N₂,₃ degeneracy alone can match it, but only in a window ΔM/M≈10⁻¹⁷ — sixteen orders of magnitude finer than the O(1) split the texture actually predicts

**Date:** 2026-09-04 - 17:10
**Numbering:** **F364** (claimed at write time; prior max F363).
**Status:** **Built and run.** A leading-order, unflavoured resonant-leptogenesis Boltzmann/QKE computation now produces an actual Y_B = n_B/s, using the model's own F201 heavy-neutrino masses and Casas-Ibarra Yukawas fit to measured neutrino oscillation data. Two independent scans (free CP phase; free N₂,₃ mass-splitting) both quantified. Sphaleron B-violation rate computed from the model's own sin²θ_W=2/9 (F320).
**Module:** `src/casim/engine/forks/darkmatter/dm_fork_F364_baryogenesis_boltzmann.py` (self-contained, real arithmetic — numpy + scipy.special/scipy.integrate; no chiral transforms).
**Tests / results:** `tests/findings/test_F364_baryogenesis_boltzmann.py` → `test-results/F364_baryogenesis_boltzmann_test.json`; fork dump `test-results/F364_baryogenesis_boltzmann.json`.
**Cross-references:** [[F202-leptogenesis-from-intrinsic-L-violation]] (the Sakharov-conditions check this finding turns into a number — **not re-attacked**, its 5/5 PASS stands), [[F201-kev-sterile-from-eg-texture]] (the Z₃/E_g texture supplying M₂, M₃, used at its own landing point, untuned), [[F47-majorana-seesaw-higgs-free]] (the seesaw the Casas-Ibarra construction sits on top of), [[F53-fg9-C-CP-per-species]] (the three-generation CP-phase freedom this finding's ω parametrises), [[F320-absolute-gauge-boson-masses]] (sin²θ_W=2/9, used for the sphaleron-rate magnitude). External: Sakharov 1967; Fukugita–Yanagida 1986 (leptogenesis); Akhmedov–Rubakov–Smirnov 1998 and Asaka–Shaposhnikov 2005 (ARS/νMSM); Casas–Ibarra 2001 (Yukawa parametrisation); Pilaftsis 1997, Pilaftsis–Underwood 2004 (regulated resonant CP asymmetry); Drewes–Garbrecht 2013 (GeV-seesaw leptogenesis without imposed degeneracy); Buchmuller–Di Bari–Plümacher 2004 ("vanilla" Boltzmann leptogenesis equations); Kolb–Wolfram 1980; Harvey–Turner 1990 (sphaleron B↔L↔B−L conversion factor); D'Onofrio–Rummukainen 2014 (lattice T_sph); NuFIT-class global oscillation fit (external, standard); Planck (Y_B).

---

## 1. The question this closes

F202 certified that all three Sakharov conditions are *available* in the model's own structure — L-violation **derived** (F47's anti-linear Majorana step), CP violation **available** (F53's three-generation Dirac+Majorana phases), out-of-equilibrium + SU(2)_L sphalerons present — but explicitly stopped short of a magnitude: *"the asymmetry's size (CP phases + N₂,₃ degeneracy) is the free, inherited residual"* and *"this is a conditions check, not a Boltzmann computation."* Rubric row K6 has stood at PARTIAL on exactly that gap: *"Condition 1 is met only in the sense of being available, never actually rated for magnitude."*

This finding does **not** re-attack the Sakharov-conditions check (closed, F202, 5/5 PASS, structural). It builds the machine that turns the two named free residuals into computed numbers, and quantifies the B-violation rate as well.

## 2. Method

**Heavy masses.** M₂, M₃ are read off the model's **own** F201 Z₃/E_g texture at its **own** landing point (M_R0 = 1 GeV, δ_ν = 134.86°) — the identical point F201 already used to land the keV DM sterile M₁ ≈ 5.6 keV. This gives

$$M_2 \approx 0.398\ \text{GeV}, \qquad M_3 \approx 5.602\ \text{GeV}, \qquad \frac{|M_3-M_2|}{\tfrac12(M_2+M_3)} \approx 1.73\ \ (\text{order-unity split}).$$

No new tuning is introduced to get these — the same input F201 already committed to. **The texture does not naturally deliver a near-degenerate N₂,₃ pair**, a fact this finding surfaces for the first time (F201 only checked the node that makes M₁ light, not the separate question of whether M₂, M₃ end up close to each other).

**Dirac mass / Yukawas.** The 3×2 Dirac mass matrix $M_D$ is fixed by the **Casas–Ibarra parametrisation**: for *any* complex orthogonal $R(\omega)$, $\omega=\omega_R+i\omega_I$,

$$M_D = i\,\hat U_\text{PMNS}\,\mathrm{diag}(\sqrt{m_2},\sqrt{m_3})\,R(\omega)\,\mathrm{diag}(\sqrt{M_2},\sqrt{M_3}),$$

$M_D$ **exactly reproduces** the measured light-neutrino masses and PMNS mixing (external: standard oscillation global-fit central values, normal ordering, $\Delta m^2_{21}=7.42\times10^{-5}\,\text{eV}^2$, $\Delta m^2_{31}=2.514\times10^{-3}\,\text{eV}^2$, $\theta_{12}=33.44°,\theta_{23}=49.2°,\theta_{13}=8.57°,\delta_{CP}=194°$; minimal seesaw, $m_1=0$, since only $N_{2,3}$ seed the active sector — $N_1$'s Yukawa is F201's feeble DM-sterile coupling, negligible here). Seesaw reproduction verified to residual $\sim10^{-8}$ (relative). $\omega$ is **exactly** the free CP phase F202 already named as not derived.

**CP asymmetry.** The **Pilaftsis–Underwood regulated resonant formula** (valid at *any* mass splitting, not only exact degeneracy — the same formula Drewes–Garbrecht 2013 use for GeV-seesaw leptogenesis without imposing degeneracy by hand):

$$\varepsilon_I=\sum_{J\ne I}\frac{\mathrm{Im}[(Y^\dagger Y)_{IJ}^2]}{(Y^\dagger Y)_{II}(Y^\dagger Y)_{JJ}}\cdot\frac{(M_I^2-M_J^2)\,M_I\,\Gamma_J}{(M_I^2-M_J^2)^2+M_I^2\Gamma_J^2},\qquad \Gamma_I=\frac{(Y^\dagger Y)_{II}M_I}{8\pi},\quad Y=\frac{\sqrt2\,M_D}{v},\ v=246.22\ \text{GeV}.$$

**Boltzmann equations.** Standard "vanilla" leptogenesis equations (Kolb–Wolfram 1980; Buchmuller–Di Bari–Plümacher 2004 form), $z=M_2/T$, $K_1/K_2$ Bessel time-dilation, decay + inverse-decay washout, **unflavoured** (single effective lepton-asymmetry channel — an explicit leading-order approximation, see §5):

$$\frac{dY_{N_I}}{dz}=-\frac{\Gamma_I}{Hz}\frac{K_1(z_I)}{K_2(z_I)}\bigl(Y_{N_I}-Y_{N_I}^\text{eq}\bigr),\qquad
\frac{dY_{B-L}}{dz}=\sum_I\varepsilon_I\frac{\Gamma_I}{Hz}\frac{K_1(z_I)}{K_2(z_I)}\bigl(Y_{N_I}-Y_{N_I}^\text{eq}\bigr)-\sum_I\frac12\frac{\Gamma_I}{Hz}\frac{K_1(z_I)}{K_2(z_I)}\frac{Y_{N_I}^\text{eq}}{Y_l^\text{eq}}Y_{B-L}.$$

Integrated with a **freeze-in initial condition** ($Y_N=0$ at $T_i=10^5$ GeV — these Yukawas never reach thermal equilibrium, satisfying Sakharov condition 3 automatically) down to the standard lattice sphaleron freeze-out $T_\text{sph}=131.7$ GeV (D'Onofrio–Rummukainen 2014); $Y_{B-L}$ at that point converts via the standard SM sphaleron factor $c_\text{sph}=28/79$ (Harvey–Turner 1990, $N_f=3,N_H=1$ — **inherited, not re-derived** for this model's own Higgs-free $U(1)_Y$ content, an explicit caveat).

**Condition-1 magnitude.** $\Gamma_\text{sph}/H$ in the symmetric phase, using the **model's own** $\sin^2\theta_W=2/9$ (F320) $\to\alpha_W=\alpha/\sin^2\theta_W\approx1/30$: $\Gamma_\text{sph}/H(T_\text{sph})\approx1.2\times10^{16}$, confirming sphalerons are parametrically fast ($\gg H$) at and above $T_\text{sph}$ — B-violation now has an actual rate attached, not just "present".

## 3. Results

### 3a. CP-phase-only scan (native F201 masses held fixed)

Scanning only $\omega_I$ (with $\omega_R=\pi/4$) over $[0,12]$, restricted to the perturbative window $|Y|_\text{max}\le1$:

| $\omega_I$ | $|Y|_\text{max}$ | $Y_B/Y_B^\text{obs}$ |
|---:|---:|---:|
| 0 | $7.6\times10^{-8}$ | $\sim-7\times10^{-33}$ |
| 4.6 (best) | $3.8\times10^{-6}$ | $-1.9\times10^{-11}$ |
| 10 | $8.3\times10^{-4}$ | $\sim+6\times10^{-19}$ (washout-suppressed) |

The ratio **peaks near $\omega_I\approx4.6$–5 at $\sim2\times10^{-11}$ of the observed value** — **not** close to 1 — then *collapses* at larger $\omega_I$ as growing Yukawas drive strong washout (a genuine physical turnover, not a numerical artefact). So: **the free CP phase alone, at the model's own native masses, cannot reach the observed asymmetry — it caps roughly 10–11 decades short**, at the edge of what perturbative Yukawas allow.

### 3b. Mass-splitting resonance scan (fixed small perturbative Yukawa, $\omega=0.3+0.5i$, $|Y|_\text{max}\approx2.3\times10^{-8}$)

$M_2$ held at its native F201 value; $M_3=M_2(1+r)$, $r$ scanned from $10^{-10}$ down to $10^{-22}$ (well-conditioned mass-squared-difference formula to avoid float64 cancellation at tiny $r$):

| $r=\Delta M_{23}/M$ | $Y_B/Y_B^\text{obs}$ |
|---:|---:|
| $10^{-10}$ | $-3.2\times10^{-9}$ |
| $10^{-14}$ | $-3.2\times10^{-3}$ |
| $\approx10^{-17}$ (peak) | $-1.47$ |
| $10^{-20}$ | $-3.5\times10^{-3}$ |

A **sharp resonance** (Breit–Wigner-shaped in $\log r$, peaking where $\Delta M\sim\Gamma_3/2$, exactly as expected from the regulated formula), with $|Y_B|$ **exceeding** the observed value at its peak. The window where $|Y_B/Y_B^\text{obs}|\ge1$ is

$$r=\Delta M_{23}/M \in [\,3.2\times10^{-18},\ 2.7\times10^{-17}\,]\quad\text{(roughly one decade wide)}.$$

Compare to the F201 texture's **own native split at the keV-DM-producing angle**: $r_\text{native}\approx1.73$ (order-unity). **Matching the observed asymmetry via this lever needs a degeneracy roughly 16–17 orders of magnitude finer than what the model's own mechanism naturally supplies.**

### 3c. Sphaleron rate (condition 1, magnitude)

$$\Gamma_\text{sph}/H\Big|_{T=131.7\,\text{GeV}}\approx1.2\times10^{16},\qquad \text{growing as}\ T^2\ \text{at higher }T.$$

Sphalerons are efficiently in chemical equilibrium throughout the symmetric phase down to freeze-out — condition 1 is not merely "present" but *fast*, using the model's own weak-mixing angle.

## 4. Verdict

The machine runs and produces real numbers. Both free residuals F202 already named — the CP phase and the $N_{2,3}$ degeneracy — are now **quantified**, not just flagged. Neither lever, taken alone at the model's own native inputs, reaches the observed baryon asymmetry without an additional, unexplained fine-tuning: the CP-phase lever caps ~10–11 decades short even pushed to the edge of perturbativity, and the degeneracy lever *can* succeed but only in a $\sim10^{-17}$-level near-degeneracy window some 16 orders of magnitude finer than the texture's own native prediction. Sphaleron B-violation is confirmed fast using the model's own $\sin^2\theta_W$.

**This promotes K6 from "condition-satisfaction, no number" to "a real Boltzmann computation exists, and it quantifies exactly how far — and in which of two specific, named directions — the model's own natural inputs fall short."** It does **not** promote K6 to a successful derivation of the baryon asymmetry: both required interventions are large, specific, and currently unexplained by anything else in the model.

## 5. Caveats (honest scope)

- **Unflavoured.** A single effective lepton-asymmetry channel is tracked; GeV-scale leptogenesis is deep in the fully-flavoured regime (all charged-lepton Yukawas in equilibrium at these temperatures), so a genuine flavour-covariant treatment could shift the result by a model-dependent $O(1)$–$O(10)$ factor. Not expected to close a 10–16 order-of-magnitude gap.
- **Not the full ARS density matrix.** This is a classical rate-equation (Boltzmann) treatment with a regulated resonant CP asymmetry, not the coherent flavour/helicity density-matrix QKE the ARS mechanism strictly requires at these masses. It captures the leading perturbative freeze-in source and the correct resonance structure and location, but not genuine quantum coherence effects, which the literature shows can matter at order-unity to order-of-magnitude level in the resonant regime — not the many-decade gaps found here.
- **No $\Delta L=2$ washout, no real-intermediate-state subtraction.** Leading decay+inverse-decay washout only.
- **$c_\text{sph}=28/79$ and $g_*=106.75$ are inherited SM values**, not re-derived for this model's own Higgs-free $U(1)_Y$/hypercharge-on-$U(x)$ construction (Decision 3, CLAUDE.md). A model-specific sphaleron/conserved-charge count is future work.
- **$\alpha_W$ uses the model's own $\sin^2\theta_W=2/9$ but a representative low-energy $\alpha$**; the symmetric-phase $\kappa=25$ coefficient is a literature-standard order-of-magnitude value, not fit to this model.
- **Only two of the three F201 texture states are used for seesaw** (minimal, $m_1=0$); $N_1$'s (F201-feeble) contribution to active masses is neglected as sub-percent.

## 6. Relation to other findings

Completes the magnitude half of the **F202** Sakharov-conditions check (not re-attacked; its 5/5 PASS stands unchanged) using the **F201** texture's own native masses and the three-generation CP freedom **F53** established. Surfaces a new, previously-unflagged structural fact about **F201**'s own Z₃/E_g texture: it does not naturally deliver a near-degenerate $N_{2,3}$ pair at the angle that lands the keV DM sterile — the two "free, inherited" parameters F202 named are now sized. Uses **F320**'s $\sin^2\theta_W=2/9$ for the sphaleron-rate magnitude. Net effect on rubric row K6: **PARTIAL, now with a real computed magnitude and two named, quantified gaps**, rather than a bare conditions checklist.
