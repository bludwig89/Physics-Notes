# F237 — The keV-sterile resolution attempt (open-derivation D2): can resonant Shi-Fuller production plus late **entropy dilution** thread the current X-ray + Lyman-α windows for the F47/F200 keV sterile? **No — clean exclusion.** The two levers are anti-correlated through the mixing: passing Lyman-α requires dilution $S$, which needs $S\times$ more production, which raises $\sin^2 2\theta$ (X-ray line rate) by exactly $\log_{10}S$ dex — the X-ray margin worsens as $S$ while the Lyman-α floor improves only as $S^{-4/9}$, so **no $S$ co-satisfies both**. The keV sterile is excluded as 100% DM; hand off to the **F223/F228 Planck-mass spin-2 geon** (the viable 100%-DM candidate). The keV sterile survives only as a bounded sub-dominant component

**Date:** 2026-07-03 - 14:20
**Numbering:** **F237** (reserved for open-derivation prompt D2; do not renumber).
**Status:** **Clean exclusion (a valid, publishable negative result per House Rules).** Reuses the validated F205 QKE production solver and adds one new physical lever — post-production entropy dilution — then scans the full $(m_s, L, S)$ space. No point clears both the current X-ray line bound and even the *conservative* (3.5 keV) Lyman-α floor, at either the 5.6 keV texture mass or the 7.1 keV benchmark. The exclusion is mechanism-level (opposite-sign scaling exponents), not a grid artifact. 7/7 acceptance checks PASS.
**Module:** `ca-simulation/forks/dm_fork_F237_kev_sterile_resolution.py` (imports and reuses `dm_fork_F205_sterile_qke_boltzmann`; numpy + stdlib, real arithmetic — no chiral transforms).
**Tests / results:** `tests/findings/test_F237_kev_sterile_resolution.py` → `test-results/F237_kev_sterile_resolution.json` (7/7); fork dump `test-results/F237_kev_sterile_resolution_fork.json`.
**Cross-references:** [[F205-sterile-qke-boltzmann-margins]] (the QKE solver reused here; the fixed-$L$ edge tension this resolves), [[F200-sterile-neutrino-dark-matter]] (the F47 keV-sterile relic identity being tested), [[F201-kev-sterile-from-eg-texture]] (the 5.6 keV texture landing that fails as 100% DM), [[F202-leptogenesis-from-intrinsic-L-violation]] (the GeV $N_{2,3}$ sector that both sources the lepton asymmetry *and* supplies the late-decay entropy dilution tested here), [[F203-dark-sector-falsifiability-battery]] (the T1/T2 falsifiers this now closes on the exclusion side), [[F223-spin2-bound-state-binding-and-relic]] / [[F228-geon-production-and-stability]] (**the hand-off**: the Planck-mass spin-2 geon = one-cell BH remnant, the viable 100%-DM candidate). External: Dodelson–Widrow 1994; Shi–Fuller 1999 (resonant); Bezrukov–Hettmansperger–Lindner 2009, King–Merle 2012, Nemevšek–Senjanović–Zhang 2012 (entropy-dilution cooling of sterile DM); Viel et al. 2005/2013 (Lyman-α thermal WDM bound); XRISM Collaboration 2025 (X-ray line limit).

---

## 1. The acceptance test (stated up front)

D2 accepts either **(a)** a viable $(m_s, \sin^2 2\theta, \Omega_\text{DM})$ point that passes all §4 falsifiers — production channel identified — or **(b)** a clean exclusion with an explicit hand-off. The pass condition for a viable point is:

$$\sin^2 2\theta \le \text{X-ray bound}(m_s)\quad\textbf{AND}\quad m_s \ge m_\text{Lyman-}\alpha^\text{floor}(\langle\varepsilon\rangle_\text{eff}),$$

evaluated with the F205 momentum-resolved QKE abundance and frozen spectrum, for the model mass $m_s = 5.6$ keV (F201) and the $\nu$MSM benchmark 7.1 keV. **Residual reported honestly in dex.** Outcome: **(b), a clean exclusion.**

## 2. What F205 left, and the one new lever

F205 computed, with the full quantum-kinetic (Boltzmann) solver:
- non-resonant Dodelson-Widrow (DW) for 100% DM at 7.1 keV needs $\sin^2 2\theta = 6.1\times10^{-9}$, **2.55 dex** above the aggregate X-ray bound → DW X-ray excluded;
- resonant Shi-Fuller production reaches $\Omega_\text{DM}$ at up to $\sim\!580\times$ smaller (X-ray-clearing) mixing, and *can* produce a cold spectrum ($\langle\varepsilon\rangle$ down to 1.57 vs DW 3.29) — but in the fixed-$L$ pass the X-ray-allowed point is **warm** and the cold point is **X-ray-excluded** (the 7.1 keV edge tension);
- even the coldest-resonant + conservative Lyman-α floor is **8.8 keV**, above the 5.6/7.1 keV masses.

F205 named the one open door: the full **$L$-depletion QKE**, which might thread the cold + X-ray-allowed corner the fixed-$L$ pass forbids. **F237 attacks that door with the standard additional cooling mechanism it did not include: post-production entropy dilution.**

**Entropy dilution.** A late-decaying heavy species — here the GeV $N_{2,3}$ steriles of the F201 texture (which decay *after* keV-sterile freeze-in but before BBN, the F202/$\nu$MSM–ARS setting) — releases entropy $S \equiv s_\text{after}/s_\text{before} \ge 1$. Two standard consequences (Bezrukov–Hettmansperger–Lindner 2009; King–Merle 2012):

| effect | scaling | direction |
|---|---|---|
| abundance dilution $Y_s \to Y_s/S$ ⇒ need $S\times$ more production; production **linear** in $\sin^2 2\theta$ (F205 V1) | $\sin^2 2\theta_\text{needed} = S\,\sin^2 2\theta_\text{undiluted}$ | X-ray line rate $\propto \sin^2 2\theta$ grows $\propto S$ — **worse** |
| plasma reheat cools the frozen spectrum | $\langle\varepsilon\rangle_\text{eff} = \langle\varepsilon\rangle / S^{1/3}$ | Lyman-α floor $\propto \langle\varepsilon\rangle_\text{eff}^{4/3} \propto S^{-4/9}$ — **better** |

## 3. The result: a mechanism-level exclusion

The two levers pull in **opposite directions in $\log S$**. Fitting the F205-mapped floor and the required mixing against $S$ (verified numerically, exact rational slopes):

$$\frac{d\log \sin^2 2\theta_\text{needed}}{d\log S} = +1 \quad(\text{X-ray margin worsens}),\qquad
\frac{d\log m_\text{Lyman-}\alpha^\text{floor}}{d\log S} = -\tfrac{4}{9} \quad(\text{Lyman-}\alpha\ \text{improves}).$$

Because the signs are opposite, **no value of $S$ improves both windows simultaneously.** The undiluted resonant point is already X-ray-optimal, and it fails Lyman-α; any dilution that helps Lyman-α re-breaks X-ray. Concretely:

- **Full $(L, S)$ grid** (14 lepton asymmetries × 11 dilution factors = 154 points, at each mass): **zero** points clear X-ray AND the conservative Lyman-α floor, for **both** 7.1 keV and 5.6 keV.
- **Maximally-generous best case:** *assume* the full $L$-depletion QKE delivers the coldest resonant spectrum ($\langle\varepsilon\rangle = 1.57$) placed **exactly at** the X-ray bound (the corner F205 forbids). Passing the Viel Lyman-α floor then needs $S\approx6$ at 7.1 keV — which costs $\log_{10}6 = +0.8$ dex **over** the X-ray bound. At 5.6 keV it needs $S\approx10$, costing $+1.0$ dex. **The door is closed even in the most generous assumption.**
- **Non-resonant + dilution** is strictly worse: $S=10$ pushes the DW mixing from 2.55 to **3.55 dex** over the X-ray bound.

So the keV sterile is **excluded as 100% dark matter** through the entire resonant + entropy-dilution production space. This confirms and *strengthens* the F205 pressure to a decisive result: the F205 caveat that the fixed-$L$ pass might over-sharpen the cold↔X-ray anti-correlation is answered — even granting the coldest spectrum at the X-ray-allowed mixing, dilution cannot close the remaining $\sim$1 dex.

## 4. §4 falsifiers checklist

Evaluated for the keV sterile as **100% DM** (the claim under test). Status vocabulary as F203: `consistent` / `under_pressure` / `falsified`.

| # | Falsifier (from `dark-sector-overview.md` §4 / F203) | F237 evaluation | Verdict |
|---|---|---|---|
| **T1 (X-ray)** | keV sterile → line at $E_\gamma = m_s/2$; mixing must sit below the aggregate X-ray bound | resonant X-ray-allowed point exists at $\sin^2 2\theta \approx 1.0\times10^{-11}$ ($L=2\times10^{-3}$), but **only for a warm spectrum**; any cooling (dilution) raises the mixing $\propto S$ back over the bound | **failed for 100% DM** (passes only sub-dominant) |
| **T2 (Lyman-α)** | warm-DM cutoff; $m_s$ must exceed the free-streaming floor | coldest-resonant + conservative floor $= 8.8$ keV $>$ 7.1 $>$ 5.6 keV; dilution lowers it as $S^{-4/9}$ but only at T1 cost | **failed for 100% DM** |
| **T1 ∧ T2 (joint)** | the two windows must **overlap** for some $(m_s, \sin^2 2\theta, S)$ | opposite-sign exponents ($+1$ vs $-4/9$) ⇒ **empty overlap**; 0/154 grid points; best case still $+0.8$–$1.0$ dex short | **no overlap → excluded** |
| **T5 (identity)** | relic is keV sterile, not WIMP/axion | keV sterile fails as 100% DM; the model's 100%-DM identity migrates to the **F223/F228 spin-2 geon** (cold, collisionless, non-fuzzy, $\Delta N_\text{eff}\approx0$ — all screens pass) | **hand-off** |
| **Sub-dominant** | keV sterile as a fraction $f<1$ of DM | X-ray ($\propto f$) and Lyman-α (fractional-WDM bound weaker) both relax; the sterile is X-ray-saturated at $f=1$ on the resonant point, so a bounded $f<1$ survives | **consistent (bounded role)** |

**Net:** 0 falsified in the sense of "model dead" — the *dark-matter identity* cleanly migrates. The **keV-sterile-as-100%-DM hypothesis** is falsified/excluded; the model's 100%-DM candidate is the geon, and the keV sterile is demoted to a sub-dominant component.

## 5. The hand-off (explicit)

Per the D2 acceptance clause "show the keV-sterile route is excluded and hand off":

- **100% DM →** [[F223-spin2-bound-state-binding-and-relic]] / [[F228-geon-production-and-stability]]: the graviton–graviton $J=2$ **geon**, $\mu\simeq\sqrt2\,M_\text{Pl}$, stable as the F190/F107 **one-cell Planck-mass black-hole remnant**. It passes every kinematic/collisionless DM screen; its one residual is the primordial-black-hole fraction $\beta$ (an external number), not an X-ray/Lyman-α tension. This is the model's viable 100%-DM identity.
- **keV sterile →** retained as a **bounded sub-dominant** relic (the F47/F200 singlet still exists, is long-lived, and is produced; it simply cannot be *all* of DM). This is a genuine, falsifiable sub-component prediction: a future X-ray line at $m_s/2$ with sub-critical flux would *confirm* the sub-dominant role.

## 6. Derived vs computed vs open

| Piece | Status |
|---|---|
| abundance dilution $\sin^2 2\theta_\text{needed} = S\,\sin^2 2\theta_\text{undiluted}$ (production linear, F205 V1) | **Derived** (dilution + linearity) |
| spectral cooling $\langle\varepsilon\rangle_\text{eff} = \langle\varepsilon\rangle/S^{1/3}$ | **Derived** (standard reheat redshift; limiting cases $S\to1$ checked) |
| opposite-sign exponents $+1$ (X-ray) vs $-4/9$ (Lyman-α) | **Computed exactly** (rational slopes, verified to $<10^{-6}$) |
| 0/154 grid points viable at 5.6 and 7.1 keV (X-ray ∧ conservative Lyman-α) | **Computed** (reusing the F205 QKE solver) |
| best-case door-closed: $S\!\sim\!6$–$10$ costs $+0.8$–$1.0$ dex over X-ray | **Computed** (coldest resonant spectrum assumed at the bound — generous) |
| keV sterile excluded as 100% DM through resonant + dilution | **Established** (mechanism-level, not grid-limited) |
| hand-off to the F223/F228 geon as the 100%-DM candidate | **Recorded** (its own findings supply the passing screens) |
| exact sub-dominant fraction $f$ (needs the full $L$-depletion QKE + a fractional-WDM Lyman-α fit) | **Open** (bounded; does not affect the exclusion) |
| absolute production normalisation | **±factor ~2** (QCD-epoch $g_*$; inherited from F205, does not move the $\sim$1 dex gap) |

## 7. Caveats (honest scope)

- The exclusion rests on the F205 abundance normalisation (±factor ~2 QCD-epoch $g_*$). This uncertainty is $\ll$ the decisive quantity: the opposite-sign scaling and the best-case $+0.8$–$1.0$ dex X-ray cost survive any factor-2 shift, because the levers pull *against each other* regardless of the shared normalisation.
- The best case assumes the full $L$-depletion QKE can place $\langle\varepsilon\rangle=1.57$ at an X-ray-allowed mixing — a corner the fixed-$L$ pass forbids. Granting it (the maximally model-favourable assumption) still leaves $\sim$1 dex, so a genuine $L$-depletion code cannot rescue the route.
- Lyman-α floors use the linear free-streaming → Viel thermal-equivalent mapping (F205), not a 3D hydro flux-power fit — the standard field methodology, and the same on both sides of the comparison.
- Entropy dilution here is treated as a single effective factor $S$ (the $N_{2,3}$ decay); a fully time-resolved dilution history would not change the sign of the exponents, only the numerical $S$.

## 8. Relation to other findings

Closes the open door F205 left (the full $L$-depletion / additional-cooling question) by testing the strongest available cooling lever, **entropy dilution from the F202 $N_{2,3}$ sector**, and finding it **cannot** thread the X-ray + Lyman-α windows: the two constraints are anti-correlated through the mixing ($+1$ vs $-4/9$ in $\log S$). This converts the F203 T1/T2 `under_pressure` status to a clean **exclusion of the keV sterile as 100% dark matter**, and migrates the model's 100%-DM identity to the **F223/F228 Planck-mass spin-2 geon**. The F47/F200 sterile neutrino remains a real, long-lived relic — now a **bounded sub-dominant** component, not the whole of dark matter. Net: the dark-matter identity is settled (the geon), and the keV sterile's role is sharpened from "candidate 100%-DM under pressure" to "excluded at 100%, surviving sub-dominant."
