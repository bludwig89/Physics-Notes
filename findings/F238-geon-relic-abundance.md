# F238 — The geon relic **abundance** is a genuinely free input, and here is exactly why: closing the F228 residual by *proving* the primordial-black-hole fraction $\beta$ cannot be derived — Press–Schechter ties $\beta$ to a small-scale primordial amplitude $\sigma(k_\text{PBH})\sim0.06$–$0.08$ that must be $\sim\!2\times10^{6}$ above the CMB value, the only tuning-free spectrum (scale-invariant, $n_s=1$) under-produces $\Omega_\text{DM}$ by $\sim2\times10^{7}$ orders, there is no attractor, and the model has **no inflaton / primordial-spectrum sector** — so abundance is a **cosmological initial condition**, not a derivable particle-physics number

**Date:** 2026-07-03 - 15:42
**Numbering:** **F238** (reserved for prompt D3; current max finding on disk F235). If a concurrent session also claimed F238, renumber on merge.
**Status:** **Documented negative result** (a valid outcome under the House Rules: "a documented *abundance remains a free input, and here is exactly why* is a valid negative result if that is what the physics shows"). **Extends [[F228-geon-production-and-stability]]**: F228 settled the *mechanism* (PBH-remnant, geon $\equiv$ Planck relic) and named $\beta(M_\text{form})$ as "the residual, one external number." F238 proves that $\beta$ is **not derivable from the model as it stands** and pins the reason to a specific missing sector. 7/7 checks PASS.
**Exactness tier:** the geon side is **exact-algebraic** (one-cell $M_\text{rem}$, reused from F190/F107) and the yield coefficient is closed-form (F228 P_a); the derivation-attempt arithmetic (Press–Schechter inversion, scale-invariant no-go, required boost) is **order-of-magnitude** — but the *conclusion* (non-derivability) is **structural / exact** (there is no inflaton finding to fix $\sigma(k)$).
**Module:** `ca-simulation/forks/gr_fork_F238_geon_relic_abundance.py` (self-contained; real arithmetic + hand-rolled `erfc`/`log10 erfc` series so the huge-argument tail never underflows to zero — no chiral/complex transforms, per CLAUDE.md).
**Tests / results:** `tests/findings/test_F238_geon_relic_abundance.py` → `test-results/F238_geon_relic_abundance.json` (7/7).
**Cross-references:** [[F228-geon-production-and-stability]] (the parent: closes production mechanism, leaves $\beta$; **this closes the "is $\beta$ derivable?" question with a negative**), [[F223-spin2-bound-state-binding-and-relic]] (the geon binds at $\mu\simeq\sqrt2\,M_\text{Pl}$; §6 abundance obstruction), [[F216-massive-spin2-dark-mode]] (massive spin-2 must be a gauge-neutral bound state), [[F190-horizon-entropy-lattice-microstates]] (one-cell floor ⇒ $M_\text{rem}$), [[F107-canonical-a-adoption-L4-grb-gate]] (the F107 cell $a^2=8\pi\sqrt3\,\ell_P^2$), [[F79-structural-newton-constant]] ($M_\text{Pl}$), [[F183-blackhole-under-full-tensor]] (Hawking $\tau\propto M^3$; the evaporation endpoint), [[F182-friedmann-pressure-cosmology]] / [[F188-multicomponent-lcdm-cosmology]] (the hot-Big-Bang cosmology the model *does* have — and where it *starts*), [[F196-dilution-exponent-derived]] (the template of turning a "free number" into a derived one — contrast: here it stays free, for a stated reason), [[F198-angular-mode-relic-misalignment]] / [[F200-sterile-neutrino-dark-matter]] / [[F205-sterile-qke-boltzmann-margins]] (the "identity settled, one relic-normalisation number left" residual template). External: Press–Schechter 1974; Carr 1975, Carr–Kohri–Sendouda–Yokoyama 2010 (PBH formation $\beta$ and the collapse threshold $\delta_c\simeq0.4$–$0.5$); MacGibbon 1987 (Planck-mass relics as DM); Planck 2018 ($A_s=2.1\times10^{-9}$, $n_s=0.965$; $\Omega_\text{DM}h^2=0.120\pm0.001$); BICEP/Keck 2021 ($r<0.036$).

---

## 1. The acceptance test (stated up front)

**Prompt D3:** attempt to *derive* a non-tunable abundance — compute the relic yield from a specific channel and test whether it hits $\Omega_\text{DM}h^2\approx0.12$ (Planck band $[0.117,0.123]$) without fine-tuning. **Acceptance:** either a derived $\Omega_\text{DM}$ in the Planck band from a stated channel, **or** a documented account of why abundance remains a free input.

The stated channel is fixed by F228: **PBH remnants** are the *only* viable production route (every field-theoretic channel is exponentially forbidden because $\mu\simeq\sqrt2\,M_\text{Pl}$ is $\sim5$ orders above every available energy scale). So "deriving the abundance" means **deriving the initial PBH mass fraction $\beta(M_\text{form})$**. This finding does that derivation attempt and reports the outcome.

**Outcome: the negative branch of the acceptance test.** Abundance remains a free input — specifically a **cosmological initial condition** (the small-scale primordial power spectrum), not a particle-physics coupling — and F238 pins *exactly why*.

## 2. What F228 pinned, and the one thing it did not

F228 closed the production *mechanism* and reduced the geon relic to a single formula (its P_a),
$$\Omega_\text{rem}h^2 = M_\text{rem}\,\beta\,\tfrac34\,\frac{T_\text{form}}{M_\text{form}}\,\frac{s_0}{\rho_c/h^2},$$
in which **every factor except $\beta$ is pinned by the model**: $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}$ is exact-algebraic (F190 area law + F107 cell), the entropy-conserved yield $\tfrac34 T_\text{form}/M_\text{form}$ is closed-form, and $T_\text{form}(M_\text{form})$ follows from the radiation-era horizon mass. Inverting for $\Omega=0.12$ gives the F228 band
$$\beta \approx 6.6\times10^{-15}\ (M_\text{form}=10^4\,\text{g}),\quad 6.6\times10^{-12}\ (10^6\,\text{g}),\quad 6.6\times10^{-9}\ (10^8\,\text{g}),\qquad \beta\propto M_\text{form}^{3/2}.$$
(Check S1 re-derives all of this from F190/F107 independently.) **The sole unpinned quantity is $\beta(M_\text{form})$.** D3 asks: can the model fix it?

## 3. Derivation attempt — fix $\beta$ from the primordial spectrum (Press–Schechter)

$\beta$ is **not** a knob of the geon sector: it is the fraction of horizon patches that collapse to black holes, a *cosmological initial condition*. For Gaussian curvature fluctuations of RMS density contrast $\sigma(M)$ at the horizon-crossing scale of mass $M$, a patch collapses iff its smoothed contrast exceeds the critical-collapse threshold $\delta_c\simeq0.45$, so (Press–Schechter / Carr)
$$\boxed{\ \beta(M) = \tfrac12\,\mathrm{erfc}\!\left(\frac{\delta_c}{\sqrt2\,\sigma(M)}\right).\ }$$
This is the bridge from "abundance" to "the small-scale power spectrum." **Inverting** the F228 $\beta$ band (S2) gives the amplitude the spectrum must carry at the PBH-formation scale:

| $M_\text{form}$ | $\beta$ (for $\Omega=0.12$) | required $\sigma(k_\text{PBH})$ |
|---|---|---|
| $10^4$ g | $6.6\times10^{-15}$ | $0.058$ |
| $10^6$ g | $6.6\times10^{-12}$ | $0.066$ |
| $10^8$ g | $6.6\times10^{-9}$ | $0.079$ |

The required small-scale amplitude is $\sigma\sim0.06$–$0.08$ — enormous compared with the **measured CMB-scale amplitude** $\sqrt{A_s}=\sqrt{2.1\times10^{-9}}=4.6\times10^{-5}$.

## 4. The scale-invariant no-go (the only tuning-free spectrum) — the acceptance test itself

The single spectrum shape that needs **no extra inflaton knob** is exact scale invariance (Harrison–Zel'dovich, $n_s=1$) anchored to the observed CMB amplitude: $\sigma(k)=\text{const}=\sqrt{A_s}$ at all scales. Then (S3)
$$x_\text{HZ}=\frac{\delta_c}{\sqrt2\,\sqrt{A_s}}=6944,\qquad \beta_\text{HZ}=\tfrac12\,\mathrm{erfc}(6944)\sim10^{-2.1\times10^{7}},\qquad \Omega_\text{DM}h^2\sim10^{-2.1\times10^{7}}\ \lll\ 0.12.$$
The tuning-free spectrum **under-produces the geon relic by $\sim2\times10^{7}$ orders** — its $\log_{10}\Omega$ sits astronomically below $\log_{10}(0.117)$. This *is* the D3 acceptance test on the natural channel, and it **fails**: a scale-invariant primordial spectrum cannot make the geon dark matter.

## 5. The size of the missing input, and the absence of an attractor

**Required boost (S4).** Power $\propto\sigma^2$, so lifting $\sqrt{A_s}\to\sigma_\text{req}$ at the PBH scale needs the small-scale spectrum enhanced by
$$\left(\frac{\sigma_\text{req}}{\sqrt{A_s}}\right)^2 \approx 1.6\times10^{6}\text{–}3.0\times10^{6}.$$
Spread over $\sim18$ decades in $k$ between the CMB scale and the PBH scale, that is a strong blue tilt $\Delta(n_s-1)\sim0.35$ (or a localized spike). This boost is a **feature of the inflaton potential** — precisely the object the model does not specify. (Note it also *contradicts* the measured near-scale-invariance $n_s=0.965<1$ on CMB scales, so the boost must be an engineered small-scale departure, not a global tilt.)

**No attractor (S5).** One might hope $\beta$ is a dynamically selected critical value. It is not: $\beta(\sigma)=\tfrac12\mathrm{erfc}(\delta_c/\sqrt2\,\sigma)$ is **strictly monotone** in $\sigma$ with no interior fixed point (verified on a grid via the asymptotic $\log_{10}\beta$). $\beta$ tracks $\sigma$ one-for-one, so there is no attractor to pin it — deriving $\beta$ *requires* deriving $\sigma(k_\text{PBH})$, i.e. the spectrum.

## 6. The missing sector (S6) — the structural reason it stays free

A search of `findings/` and `ca-simulation/` returns **no inflaton finding, no preheating finding, and no primordial-power-spectrum module** — `ca_cosmology.py` (F182/F188) starts at the hot Big Bang and takes the radiation content as given. The model therefore has **no structure that fixes $\sigma(k)$ at the PBH scale**. The full causal chain is
$$\Omega_\text{DM}\ \longleftarrow\ \beta(M_\text{form})\ \longleftarrow\ \sigma(k_\text{PBH})\ \longleftarrow\ \text{primordial }P(k)\ \longleftarrow\ \text{inflaton potential (absent)}.$$
Every arrow after $\beta$ leaves the model. So $\sigma(k_\text{PBH})$ — and hence $\beta$, and hence $\Omega_\text{DM}$ — is an **external cosmological initial condition**, in exactly the same way $H_\text{inf}$, $T_\text{RH}$, $g_*$ were external inputs for F198/F205/F223/F228.

## 7. Verdict

> **The geon relic abundance $\Omega_\text{DM}h^2=0.12$ is not derivable from the model as it stands.** It is inherited one-for-one from the initial PBH fraction $\beta(M_\text{form})$, which Press–Schechter fixes from the small-scale primordial amplitude $\sigma(k_\text{PBH})$. That amplitude must be $\sim2\times10^{6}$ times the CMB value; the only tuning-free spectrum (scale-invariant) under-produces by $\sim2\times10^{7}$ orders; $\beta(\sigma)$ has no attractor; and the model has no inflaton / primordial-spectrum sector to fix $\sigma(k_\text{PBH})$. **Abundance is a free cosmological *initial condition*, isolated to a single external number — not a derivable particle-physics coupling.**

This is the honest, defensible closure of the D3 question, and it **sharpens** F228: F228 called $\beta$ "the residual, one external number" and left open whether it could be derived; F238 proves it *cannot* (from the model as it stands) and identifies the precise missing ingredient (the inflaton/spectrum sector) — turning "the abundance is tunable" into "the abundance is provably a free cosmological initial condition, for a stated structural reason." It also localizes what a *future* derivation would require: a model-native inflaton whose potential produces a small-scale spectral feature of amplitude $\sigma\sim0.07$ at the $M_\text{form}\sim10^4$–$10^8$ g horizon scale — a concrete, falsifiable target for a later finding, not a free-floating fudge.

## 8. What is derived vs computed vs open

| Piece | Status |
|---|---|
| Geon side fully pinned; $\beta$ is the sole residual (reuse F228 $M_\text{rem}$, yield) | **exact-algebraic** (F190/F107) + closed-form yield |
| Press–Schechter bridge $\beta=\tfrac12\mathrm{erfc}(\delta_c/\sqrt2\,\sigma)$; required $\sigma\sim0.06$–$0.08$ | **derived** (standard PBH formation) + **computed** inversion |
| Scale-invariant no-go: $\beta_\text{HZ}\sim10^{-2.1\times10^{7}}$, under-produces by $\sim2\times10^{7}$ orders | **computed** (order-of-magnitude; hand-rolled asymptotic $\mathrm{erfc}$) |
| Required spectral boost $\sim2\times10^{6}$ ($\Delta(n_s-1)\sim0.35$ / a spike) | **computed** (order-of-magnitude) |
| $\beta(\sigma)$ strictly monotone ⇒ **no attractor** | **derived** (property of $\mathrm{erfc}$) |
| No inflaton / preheating / primordial-spectrum sector in the model | **structural fact** (directory search) |
| **Verdict: abundance is a free cosmological initial condition** | **inferred / structural** (the chain leaves the model at $\sigma(k_\text{PBH})$) |
| Exact $\Omega_\text{DM}h^2=0.12$ from a **model-derived** spectrum | **open** — needs a model-native inflaton (the concrete future target this finding names) |

## 9. Honest scope

The strong content is the **provable non-derivability with a named cause**: not "we couldn't find $\beta$," but "$\beta$ is pinned to the small-scale primordial spectrum, that spectrum must depart from the observed CMB amplitude by $\sim2\times10^{6}$, the only assumption-free spectrum fails by $\sim2\times10^{7}$ orders, there is no attractor, and the sector that would fix it does not exist in the model." The arithmetic is order-of-magnitude (the collapse threshold $\delta_c$, the O(1) Press–Schechter prefactor, and $M_\text{form}$ each carry factor-level uncertainty), but none of that touches the conclusion, which spans tens of millions of orders and rests on a structural absence. This is the *same shape* of residual as F198 (freeze-out $(m,g)$), F200 (keV scale + asymmetry) and F196 (the $\Omega_\Lambda$ coincidence) left — with the added value that F238 says precisely **what kind** of residual it is (a cosmological initial condition) and **what** would be needed to remove it (a model-native inflaton), rather than leaving it as an undifferentiated "free number."

## 10. Files
- Module/fork: `ca-simulation/forks/gr_fork_F238_geon_relic_abundance.py`
- Test: `tests/findings/test_F238_geon_relic_abundance.py`
- Results: `test-results/F238_geon_relic_abundance.json`
