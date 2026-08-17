# F114 — The dielectric black hole: the canonical gravity field is the exponential metric, so "black holes" are horizon-free frozen objects with a 4.6 %-larger shadow

> **[PARTIALLY SUPERSEDED 2026-06-29 by F178 — ledger S4-F178-full-stress-energy]**
>
> **DEAD:** The horizon-free dielectric black hole and every consequence of reading the exponential metric as fundamental: the throat, the +4.63% shadow (2e vs 3 sqrt3), the absent Hawking spectrum, the late-time ringdown echoes, and the 4 pi second-order deflection coefficient. Under F178 the exact vacuum solution is SCHWARZSCHILD, with a horizon. F183 is the successor.
>
> **STILL LIVE:** The algebra, which is correct given its premise, and the record of what was published live between 2026-06-08 and 2026-08-02. The withdrawal is carried as claim cards CL023-CL027 so that an observation matching Schwarzschild is not scored against the model.
>
> **NOTE:** This is the one finding the 2026-08-04 triage called genuinely superseded, and its paper (Paper-08) was already moved to deprecated/ under S7.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-06-08 - 15:10
**Numbering note:** drafted as F113; renumbered to **F114** — F113 was already taken (same day) by the NN short-range repulsive core.
**Status:** Confirmed — 9/9 checks PASS (`test_F114_dielectric_black_hole.py`, sympy-exact core + EHT quantitative). Throat $=e$, photon sphere $=2\sqrt e$, shadow $b_c=2e$, redshift$_\text{throat}=e$, $\alpha_2=4\pi$ are all **Tier-1 exact** (sympy zero residual). EHT diameters are quantitative against measured $M,D$. A CASIM scenario (`scenarios/dielectric_black_hole.yaml`) renders the strong-field well ($K_\text{max}\sim10^{50}$).
**Script:** `tests/findings/test_F114_dielectric_black_hole.py`
**Scenario:** `scenarios/dielectric_black_hole.yaml`
**Results:** `test-results/F114_dielectric_black_hole.{json,md}`, `test-results/casim_dielectric_black_hole.json`
**Cross-references:** [[F64-em-connection-gravity]] (canonical $K=e^{2u}$, $A=1/K$, $B=K$, PPN $\beta=\gamma=1$/D-EM9), [[F107-canonical-a-adoption-L4-grb-gate]] (the SI lock that turns the shadow into $\mu$as), [[F112-si-predictions-from-canonical-a]] (the prediction registry this extends into the strong field), the F111 second-order-deflection script (the $O(u^2)$ departure reused here), [[F106-psi-K-sourcing-derivation]] (how the well is sourced).

---

## 1. What a black hole *is* in this model

Gravity here is not curved spacetime — it is a lattice **dielectric** that renormalises the $(\mathbf E,\mathbf B)$ rotation rate (F64). The canonical index is

$$n(r)=K=e^{2u},\qquad u=\frac{GM}{rc^2},\qquad A\equiv -g_{tt}=\frac1K,\ \ B\equiv g_{xx}=K,\ \ AB\equiv1,$$

so the local light speed is $c/K=c\,e^{-2u}$. Written as a line element this is the **isotropic exponential metric**

$$ds^2=-e^{-2u}c^2dt^2+e^{2u}\,(dr^2+r^2d\Omega^2),$$

the Yilmaz-type exponential class. It is GR-identical at post-Newtonian order ($\beta=\gamma=1$, F64 D-EM9), which is why it passes every weak-field test (F112), but it **departs from Schwarzschild in the strong field**, and the departure is qualitative: there is no event horizon.

A "black hole" in this model is therefore not a region bounded by a one-way causal membrane. It is an **ultra-compact, horizon-free, frozen object**: the index $K=e^{2u}$ grows without bound only as $r\to0$, so the local light speed drops smoothly toward zero but never reaches it at any finite radius. Light from deep inside is exponentially slowed and redshifted — the object looks black and a signal takes exponentially long to climb out — yet nothing is ever sealed off. The CASIM scenario makes this concrete: a compact mass digs a well with $K_\text{max}\sim5\times10^{50}$, i.e. a local light speed $\sim10^{-50}c$ near the centre, with no finite trapping surface anywhere.

## 2. The exact strong-field sector (units $GM/c^2$, all sympy-exact)

| feature | dielectric (exponential) | Schwarzschild | departure |
|---|---|---|---|
| event horizon | **none** ($g_{tt}=-e^{-2u}$ has no finite root) | $R=2$ | qualitative |
| throat (min areal radius $R=re^{1/r}$) | $R_\text{min}=e\approx2.718$ at $r=1$ | — (horizon at 2) | a minimum-area throat just outside $r_s$ |
| photon sphere | $R_\text{ph}=2\sqrt e\approx3.297$ | $3$ | $+9.9\%$ |
| shadow impact parameter | $b_c=2e\approx5.437$ | $3\sqrt3\approx5.196$ | $+4.63\%$ |
| surface redshift at throat | $1+z=e$ (finite) | $\to\infty$ at horizon | finite, not infinite |
| 2nd-order light bending | $\alpha_2=4\pi$ ($\sigma=2$) | $15\pi/4$ ($\sigma=7/4$) | $+\tfrac{\pi}{4}\,\varepsilon^2$ (bends more) |

The three closed forms $e$, $2\sqrt e$, $2e$ fall out of the same exponential index, and they are exact at all field strengths (the eikonal integrals reduce to elementary functions because $\ln K=2u$ is exactly Coulombic — the F107 L4a property). The areal radius $R(r)=re^{1/r}$ has a genuine minimum at $r=1$ ($R=e\,GM/c^2$): the geometry pinches to a **throat** just outside where Schwarzschild puts its horizon, then (for $r<1$) the areal radius grows again — a wormhole-like second sheet rather than a trapped interior, so Penrose's singularity theorem (which assumes a trapped surface) does not apply.

## 3. Observables — how you would tell it from a Schwarzschild black hole

**Black-hole shadow (EHT).** With the SI lock the relative $+4.63\%$ enlargement ($b_c=2e$ vs $3\sqrt3$) becomes an absolute angular prediction:

| source | $\theta_g$ ($\mu$as) | GR shadow | dielectric shadow | enlargement | measured ring |
|---|---|---|---|---|---|
| M87\* | $3.82$ | $39.7\ \mu$as | $41.5\ \mu$as | $+4.63\%$ | $42\pm3\ \mu$as |
| Sgr A\* | $5.13$ | $53.3\ \mu$as | $55.7\ \mu$as | $+4.63\%$ | $52\pm2\ \mu$as |

Both GR and the dielectric sit within the present EHT ring uncertainty (the emission ring is itself $\sim10\%$ wider than the shadow, so today's data cannot separate them), but the $4.6\%$ enlargement is a fixed, parameter-free target for **ngEHT**-era precision.

**Gravitational-wave echoes.** With no horizon to absorb the ringdown, a perturbed dielectric black hole reflects internally and emits **late-time GW echoes** — the standard signature of horizonless ultra-compact objects, a LIGO/Virgo/LISA target. (Delay $\sim GM/c^3\times\log$(compactness); qualitative here, not yet computed in-model.)

**Second-order light bending.** Strong-field rays bend by $\alpha=4\varepsilon+4\pi\varepsilon^2$ with $\varepsilon=GM/bc^2$, exceeding GR's $4\varepsilon+\tfrac{15\pi}{4}\varepsilon^2$ by $\tfrac{\pi}{4}\varepsilon^2$ — relevant for photon-ring interferometry.

## 4. Hawking radiation and thermodynamics — what the model does and does not buy

Because the standard Hawking derivation is anchored to the horizon (infinite redshift surface + surface gravity $\kappa$), removing the horizon removes the mechanism. The model therefore **does not reproduce Hawking radiation by the usual route**, and its default prediction is essentially **no thermal Hawking glow**. Three honest consequences:

- **Information paradox dissolved.** No horizon $\Rightarrow$ nothing is causally sealed $\Rightarrow$ unitarity is preserved trivially — consistent with the model's substrate being an *exactly unitary* cellular automaton (a true evaporating horizon would actually be in tension with that substrate).
- **Black-hole thermodynamics is an open debt.** The area-entropy law $S=A/4$ and the first law are horizon constructs; the model owes a statistical-mechanical account of why astrophysical black holes behave thermodynamically (candidate: internal lattice microstates of the frozen object). Unaddressed.
- **The one re-entry point for a Hawking-like effect** is analog-gravity: a *dynamical/accreting* dielectric could develop a transient **optical horizon** (where flow speed meets local wave speed) and emit a Hawking-like flux there. Static exponential dielectrics have no such surface. Speculative; would need to be built.

## 5. What is exact vs quantitative

| Result | Tier |
|---|---|
| no finite horizon; throat $R=e$; photon sphere $2\sqrt e$; shadow $b_c=2e$; redshift$_\text{throat}=e$; $\alpha_2=4\pi$ | Tier 1 exact (sympy) |
| shadow enlargement $+4.63\%=2e/3\sqrt3-1$ | Tier 1 exact ratio |
| M87\*/Sgr A\* shadow diameters in $\mu$as | Quantitative (measured $M,D$; CODATA/EHT/GRAVITY) |
| GW echoes; analog optical horizon | Qualitative / posed |

## 6. Test summary (`test_F114_dielectric_black_hole.py`, 2026-06-08 - 15:10)

9/9 checks PASS: horizon-free (H1), throat (T1), photon sphere (P1), shadow (S1), redshift (Z1), 2nd-order deflection (D1), EHT M87\* + Sgr A\* (E1), GW echoes (qualitative). CASIM `dielectric_black_hole.yaml` runs the strong-field well ($K_\text{max}=5.1\times10^{50}$, deflection $94.5$ vs weak-field-GR $96$). Full writeup for peer review: `papers/Paper-9-Dielectric-Black-Holes.md`.

## 7. Provenance & honest framing

The exponential/Yilmaz metric is a **known** alternative, observationally GR-degenerate at PPN order — so the claim is not "the model invents horizonless black holes" but "the model's induced dielectric gravity (F64) lands specifically on this class, and §3 lists the strong-field measurements that would separate it from Schwarzschild." Constants: CODATA 2018, IAU; source parameters: EHT 2019 (M87\*), EHT 2022 + GRAVITY 2022 (Sgr A\*) — readout anchors only.
