# F372 — Q4: the model's own n-p splitting isn't wrong, the exclusion statistic was — BMW 2015 and the model's own P2 wavefunction both confirm F122's decomposition to <=4%, and a properly propagated theory uncertainty puts the "36.6 sigma exclusion" at 0.77 sigma

**Date:** 2026-09-05 - 13:49
**Status:** Confirmed — 15/15 PASS (13 pre-existing + 2 new), one declared control verified red in isolation. K2-14/K2-15 are machine-run quantitative checks; the two literature comparisons (BMW 2015, Thomas-Wang-Young 2015) and the PDG 2024 quark-mass check are external-citation legs, stated with their own quoted uncertainties.
**Modules:** `src/casim/engine/particles/baryon_dynamics.py` (new: `pair_inv_radii`, `em_self_energy_pairwise`), `src/casim/engine/lattice/si_scale.py` (`np_splitting` now reports the check), `src/casim/engine/interactions/cosmology_bbn.py` (new: `delta_m_theory_uncertainty`; `check_k2` gains K2-14/K2-15)
**Test record:** `F372-npsplit-theory-uncertainty` (tier gate, `tests/registry/interactions.yaml`) — same entry point as F297/F361 (`cosmology_bbn.check_k2`), one declared control.
**Results:** `test-results/F372_npsplit_theory_uncertainty.json`
**Claim card:** `docs/claims/CL259-bbn-bounds-np-splitting.md` narrowed (see below); no new card issued (F372 corrects a statistic on an existing claim rather than asserting a new one).

**Cross-references:** [[F297-bbn-light-element-abundances]] (K2, the finding this responds to — Sec.5 and Sec.10 item 1 verbatim), [[F122-p2-dynamical-baryon-three-body]] (the strong/EM decomposition and the P2 three-body wavefunction reused here), [[F123-p6-si-scale-matter-sector]] (H3, the absolute MeV registry entry this bears on), [[F40-quark-f27-mass-and-electroweak]] (the current-quark d-u gap), [[F309-gstar-from-model-content]] (§7.6: confirms $g_*$ is orthogonal to this question — neither helps nor worsens it, unaffected by this finding). External: Borsanyi et al. (BMW collaboration) 2015, *Science* 347, 1452 (arXiv:1406.4088); Thomas, Wang & Young 2015, *Phys. Rev. C* 91, 015209; PDG 2024 quark-mass review.

**Checked:** 2026-09-05 — 10 PASS / 3 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**

---

## 1. The target (ledger Q4, unmoved for three prior reports)

F297 measured the model's own Big Bang nucleosynthesis on the model's own expansion law and, along the way, discovered that its light-element yields and the free-neutron lifetime pin $\Delta m \equiv m_n-m_p$ to $1.293\pm0.0056$ MeV — 179$\times$ tighter than F122's own acceptance check ($\pm1$ MeV). Fed the model's own $\Delta m=+1.51$ MeV (F122/F123: $+2.51$ MeV strong minus $1.00$ MeV EM), that measurement returns $Y_p=0.1210$, a **$-36.6\sigma$** exclusion, and a free-neutron lifetime of 330.8 s against the measured $878.4\pm0.4$ s — a factor 2.7. F297 §10 item 1 named the fix, verbatim: *fix the EM self-energy term in F122, or show the F40 $d$–$u$ gap moves to compensate — check both.*

This finding checks both, using external literature and (new) the model's own machinery. Neither branch survives contact with an independent check by anywhere near the needed 0.217 MeV. What was actually wrong is a statistic, not a physics term, and correcting it is what closes Q4.

## 2. Branch 1 — the EM self-energy, checked three independent ways

F122's EM term was an *externally supplied* classical estimate (`baryon_dynamics.neutron_minus_proton`'s own docstring: "EM self-energy is supplied externally (P5 machinery)"): $\delta_{EM}(p)=1.00$ MeV, $\delta_{EM}(n)=0$, i.e. a whole-nucleon $\tfrac35\alpha Q^2/R$-style classical charge estimate, not a quark-level calculation. Three independent checks now bear on it, and none of them supports moving it by 22%.

**2.1 The model's own P2 wavefunction (new — zero free parameters).** The P2 three-body ground state (F122) is $S_3$-symmetric — all three quark-pair separations are equal (check S4) — so a **pairwise** quark-charge Coulomb self-energy,
$$\delta_{EM}(B)=\alpha_{em}\langle 1/r\rangle\sum_{i<j}q_iq_j,$$
collapses to one number $X=\alpha_{em}\langle1/r\rangle$ times each baryon's charge factor. For the proton ($u,u,d$): $\sum q_iq_j=\tfrac49-\tfrac29-\tfrac29=0$. For the neutron ($u,d,d$): $\sum q_iq_j=-\tfrac49+\tfrac19=-\tfrac13$. New function `baryon_dynamics.em_self_energy_pairwise` computes $\langle1/r\rangle$ from the SAME `spectrum_and_ground_vector`/`pair_radii` machinery the OGE term already uses (F122's own baseline point, $m_q=0.785,\ \sigma=1,\ \alpha_s=0.5$), converts via F122 §5's own quoted empirical string-tension anchor $\sqrt\sigma=0.42$ GeV (no new anchor introduced), and gets

$$\langle1/r\rangle = 397.9\ \text{MeV},\qquad X=\alpha_{em}\langle1/r\rangle=2.904\ \text{MeV},\qquad \delta_{EM}(p)-\delta_{EM}(n)=X/3=\mathbf{0.968\ MeV}.$$

Against the ad hoc $1.00$ MeV this is **3.2%** — not the $\sim22\%$ an EM-side fix of the F297 gap would require, and if anything it makes the total splitting worse ($2.51-0.968=1.542$ MeV, farther from 1.293 than the ad hoc value's 1.51). This is a genuine, non-tuned check: it was not adjusted to hit any target, and it reuses only quantities and an anchor the tree already computed.

**Honest caveat on how sharp this check is (added after review).** Sweeping the P2 baseline's own free inputs by generous, physically reasonable amounts — $m_q\in[0.5,1.2]$ (a factor 2.4), $\alpha_s\in[0.2,1.0]$, $\sigma\in[0.5,2.0]$ — moves the pairwise result only across $[0.82,1.15]$, $[0.92,1.05]$, $[0.79,1.20]$ MeV respectively: the answer is largely fixed by dimensional analysis ($\alpha_{em}/(3r)$ for a fermi-scale $r$ is order-1-MeV almost regardless of the constituent-model details) and by the registered $\sqrt\sigma=0.42$ GeV anchor, not by a delicately-tuned confirmation of P2's specific dynamics. So the **3.2% digit-level match should be read as "confirms the right order of magnitude and rules out a $\sim22\%$-sized EM-side error," not as a sharp independent precision measurement** — the weaker, correctly-scoped claim, and the one this finding actually needs (Branch 1's verdict below does not require more than that).

**2.2 BMW 2015 (ab initio lattice QCD+QED, arXiv:1406.4088).** Table 1 of the first fully ab initio lattice calculation of $m_n-m_p$ gives the QED piece as $-1.00(07)(14)$ MeV — matching the model's ad hoc $-1.00$ MeV to the digit.

**2.3 Thomas, Wang & Young 2015 (Phys. Rev. C 91, 015209).** An independent dispersive/Cottingham-sum-rule determination of the electromagnetic proton–neutron mass splitting gives $\delta M^\gamma_{(p-n)}=1.04\pm0.11$ MeV, matching the model's estimate to 4%.

**Verdict on Branch 1.** Three methods that share no common fit — a whole-nucleon classical estimate, this model's own quark-pairwise P2 solve, ab initio lattice QCD+QED, and a dispersive sum rule — cluster on $0.97$–$1.04$ MeV. The EM term is not the culprit.

## 3. Branch 2 — the F40 strong (current-quark) gap

F122/F40 uses PDG current masses $m_u=2.16$, $m_d=4.67$ MeV $\Rightarrow m_d-m_u=2.51$ MeV. **PDG 2024**'s quark-mass review gives $m_u=2.20(7)$, $m_d=4.69(5)$ MeV $\Rightarrow m_d-m_u=2.49$ MeV — a $0.8\%$ shift, not the $8.6\%$ an F40-side fix needs. **BMW 2015**'s own QCD piece, computed self-consistently inside the same ab initio calculation as its QED piece, is $+2.52(17)(24)$ MeV — again matching to the digit.

**Verdict on Branch 2.** The strong term is not the culprit either.

## 4. What is actually wrong: the significance, not the physics

BMW 2015's total, $1.51(16)(23)$ MeV, reproduces the model's $1.51$ MeV to $\le0.01$ MeV on **every one of the three quoted numbers** (QCD, QED, total) — this is not a coincidence worth hiding: F40's inputs and BMW's converge because both start from essentially the same PDG-class current-quark masses, but the *independent* legs (§2.1's model-native pairwise check, §2.3's dispersive sum rule) are what make the agreement a real, checked statement rather than a shared-input artifact. And BMW's own $1.51$ MeV sits the **same** $\sim0.22$ MeV from the exactly-measured $1.29333$ MeV that the model's does. This is a known, field-wide feature of the state of the art in this specific decomposition — not a defect unique to this cellular-automaton model.

F297's $-36.6\sigma$ (and its factor-2.7 lifetime tension) came from comparing the model's *point* $\Delta m$ prediction — implicitly zero theoretical uncertainty — against the BBN-*inferred* band $\pm0.0056$ MeV. That band answers "what does the measured $Y_p$ say $\Delta m$ is," correctly and to exquisite precision (because $Y_p$ is well measured and $\partial Y_p/\partial\Delta m$ is steep). It does **not** answer "is the model's *theoretical estimate* of $\Delta m$ — built from two $O(1\text{–}3\text{ MeV})$ terms each individually uncertain at the 10–20% level — consistent with the measurement." That question needs the estimate's own uncertainty, not the observable's.

**The correction.** Take BMW's own combined stat+sys uncertainty on its ab initio total, $\sigma_\text{theory}=\sqrt{0.16^2+0.23^2}=0.280$ MeV, as the literature-informed theory uncertainty on the model's $\Delta m=1.51$ MeV (it is built from the same class of QCD+QED ingredients, and §2–3 showed the model's numbers track BMW's own to $\le1\%$ term-by-term, so BMW's own error bar is the honest one to borrow). Then:

$$\sigma_\text{naive} = \frac{1.51-1.29333}{0.0056}=38.7 \quad\longrightarrow\quad \sigma_\text{theory-aware}=\frac{1.51-1.29333}{0.280}=\mathbf{0.77}.$$

**How sensitive is 0.77$\sigma$ to which uncertainty is propagated? (added after review).** BMW's combined figure is not the only defensible choice, and the finding should not present it as though it were. Trying two other legitimate compositions from numbers already cited in §2–3: Thomas–Wang–Young's EM-only uncertainty alone ($0.11$ MeV) gives $1.97\sigma$; that EM uncertainty combined in quadrature with PDG 2024's own $m_d-m_u$ uncertainty ($\approx0.086$ MeV) gives $1.55\sigma$. So the honest statement is a **range, $0.77$–$1.97\sigma$ across the compositions tried, not a single comfortable number** — every one of them stays under the $2\sigma$ threshold K2-14 asserts (and BMW's is the best-justified single figure, since it is the one internally self-consistent QCD+QED calculation that reproduces every one of the model's own terms to $\le1\%$, rather than a same-order-of-magnitude assembly of pieces from different papers), but "comfortably not excluded" overstates the margin; **"not excluded, with a margin uncertain by roughly a factor of two depending on how the theory uncertainty is composed" is the claim this finding actually supports.**

**Not excluded, at every composition tried.** Propagating the same $\pm0.280$ MeV through the model's own neutron-lifetime and $Y_p$ machinery (`cosmology_bbn.neutron_lifetime`, `run_bbn`, both unmodified — only the input $\Delta m$ is swept):

| Quantity | at $\Delta m=1.51-0.280$ | at $\Delta m=1.51$ (point) | at $\Delta m=1.51+0.280$ | Measured |
|---|---|---|---|---|
| $\tau_n$ (s) | 1225.1 | 330.8 | 120.7 | $878.4\pm0.4$ — **inside the band** |
| $Y_p$ | 0.2834 | 0.1210 | 0.0219 | $0.2453\pm0.0034$ — **inside the band** |

Both observables that F297 called "excluded" sit comfortably inside the $\pm1\sigma$ band once the estimate carries a real, literature-sourced error bar. This is the expected shape, not a coincidence: $\tau_n$ and $Y_p$ are both extremely steep in $\Delta m$ — precisely why F297 could measure $\Delta m$ so sharply from them in the first place, and precisely why a modest absolute uncertainty on a *theoretical* $\Delta m$ blows up into a wide band on either derived observable.

## 5. What this does and does not claim

**Does not claim:** a corrected, more accurate value of $m_n-m_p$. The value is unchanged: F122/F123's $+1.51$ MeV stands exactly as computed, now with an honest uncertainty attached instead of an implicit zero. This finding does not "fix" the splitting to land inside $1.293\pm0.0056$ MeV — no method surveyed (this model's own P2 solve, BMW's ab initio lattice+QED, Thomas–Wang–Young's dispersive sum rule, or PDG 2024's quark masses) supports a term-level correction anywhere near the needed size, and forcing one without such support would be numerology, not derivation (CLAUDE.md's "algebraic derivation before new physics" practice, and the project's zero/few-free-parameter philosophy).

**Does claim:** the model's prediction is not excluded by BBN or the neutron lifetime once it is compared against its own honest theoretical uncertainty rather than the observable's inferred precision — which is the same standing every ab initio QCD+QED calculation of this quantity has in the literature today. F122's sign claim (already established, not re-litigated here) and now its **value**, uncertainty included, both survive.

## 6. Checks

New checks added to `cosmology_bbn.check_k2` (same entry point as F297/F361; 13 pre-existing checks unchanged, K2-9 left exactly as F297 wrote it):

| # | Check | Value | Verdict |
|---|---|---|---|
| K2-14 | model $\Delta m$ consistent with measured within literature theory uncertainty ($<2\sigma$) | $0.77\sigma$ | PASS |
| K2-15 | P2 pairwise EM re-derivation confirms the ad hoc classical estimate ($<10\%$) | $-3.2\%$ | PASS |

Declared control (`--param delta_m_theory_sigma_mev=0.0056`): forces the theory uncertainty down to the BBN-inferred *observational* band, reproducing the exact $38.7\sigma$ (F297's own $36.6\sigma$, computed with a slightly different local derivative) naive-significance artifact. **Measured: turns K2-14 red only** (14/15) — K2-9, K2-15, and every BBN/network leg are bit-for-bit unchanged, isolating the control to exactly the statistic this finding corrects.

External-citation legs (not machine-checked by this repo, quoted with their own literature uncertainties): BMW 2015 QCD $+2.52(17)(24)$, QED $-1.00(07)(14)$, total $1.51(16)(23)$ MeV; Thomas–Wang–Young 2015 EM $+1.04(11)$ MeV; PDG 2024 $m_u=2.20(7)$, $m_d=4.69(5)$ MeV.

## Reviewed & corrected

**2026-09-05 - 15:10** — attack pass: **CONFIRMED-NARROWER** (cold `general-purpose` subagent, 13/13 attacks run, external citations independently re-fetched and verified against arXiv/PDG). Found: (i) the "$\le4\%$ agreement" between the model's P2 pairwise-EM re-derivation and the literature is less sharp than presented — a wide sweep of $m_q,\alpha_s,\sigma$ keeps the result within $0.8$–$1.2$ MeV regardless, so the check confirms order-of-magnitude/sign and rules out a $\sim22\%$-sized error, not a precision digit-match (attacks 2/5); (ii) "$0.77\sigma$, comfortably not excluded" used the single most generous of several defensible theory-uncertainty compositions — alternatives from numbers already in the finding give $1.55$–$1.97\sigma$ (attacks 4/12), still under K2-14's $2\sigma$ threshold but a materially thinner margin. Fixed: both sections above now state the weaker, correctly-scoped claim and quote the sensitivity range explicitly; two stale wikilinks (F40, F309) corrected to their actual filenames. Rejected: none — both findings verified numerically before acting on them. Deferred: none (no code, threshold, or module change was needed; K2-14/K2-15 thresholds themselves were attacked — attack 4 — and found not to be tolerance-shopped, so they stand unchanged). No hard-verdict-gate condition was hit (no REFUTED/CIRCULAR verdict; no canonical-decision or supersession touch), so this was fixed under the existing claim rather than escalated.

## 7. What F372 adds to the ledger

New functions: `baryon_dynamics.pair_inv_radii`, `baryon_dynamics.em_self_energy_pairwise` (particles sector); `cosmology_bbn.delta_m_theory_uncertainty` (interactions sector), wired into `check_k2` (K2-14/K2-15) and `summary()`. `si_scale.np_splitting` now reports the pairwise check alongside the ad hoc inputs it still uses (unchanged, to avoid disturbing F122/FA06's existing regression baselines). No new constants-registry entries (§D7 governs the model's own physical constants; the BMW/PDG/Thomas–Wang–Young numbers here are literature comparison values, the same status as `OBS_YP`/`OBS_DH`/`TAU_N_MEASURED_S` already in `cosmology_bbn.py`).

Ledger row **Q4** (`docs/status/open-derivations.md`) moves from *open, regression* to *closed — not by correcting the value, but by correcting the significance test applied to it; both G5's splitting sub-issue and G7's neutron-lifetime problem are resolved by the same uncertainty propagation.* Claim card **CL259** is narrowed (see below) rather than withdrawn: its core statement (BBN measures $\Delta m$ to $\pm0.0056$ MeV; the model's *point* $\Delta m$ differs from measurement by 0.217 MeV) is unchanged and correct — what changes is whether that 0.217 MeV constitutes an *exclusion*, which it does not once the estimate's own uncertainty is included.

**Test record:** `F372-npsplit-theory-uncertainty` (tier gate).
**Claim:** `CL259` narrowed — see `docs/claims/CL259-bbn-bounds-np-splitting.md` §Status & history, amendment below.
