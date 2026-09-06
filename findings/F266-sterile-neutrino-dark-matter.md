# F266 — The model-native dark-matter relic: the F47 sterile right-handed neutrino. It is a total SM singlet ($Y=0$ structurally forced), cosmologically long-lived ($\tau/t_0\sim10^9$ at the viable mixing — passing where the $E_g$ modes failed by ~38 orders, F199), clustering (warm), and collisionless; it is the $\nu$MSM keV sterile neutrino, viable via resonant production in the X-ray/Lyman-$\alpha$ window and tied to the F47 see-saw that already explains the small active-neutrino mass

> **Renumbered F200 → F266 on 2026-07-31 (roadmap C8.2 close-out).** F200 was used by two unrelated findings — this dark-sector relic and the saturated-condensate E_g sextic-coupling computation — with no recorded age difference, equal citation counts and no way to pick a side. Rather than suffix one arbitrarily, this file moved to the next free number; `F200-eg-sextic-coupling-computed.md` keeps F200 outright. Recorded in `docs/design/finding-numbers.yaml`.


**Date:** 2026-06-30 - 21:15
**Numbering:** **F200** (re-checked; prior max F199).
**Status:** **Identifies a viable, model-native dark-matter candidate.** Existence and stability are derived/computed from the model's own F47 sterile sector; the keV mass and the production mechanism are accommodated within the established $\nu$MSM window, not derived. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F200_sterile_neutrino_dm.py` (self-contained, real arithmetic).
**Tests / results:** `tests/findings/test_F200_sterile_neutrino_dm.py` → `test-results/F200_sterile_neutrino_dm_test.json` (5/5); fork dump `test-results/F200_sterile_neutrino_dm.json`.
**Test record:** record `F200-sterile-neutrino-dm` (tier battery) — the five-check fork dump above. The record id and the test filename keep the pre-renumber `F200` tag (see the banner); the record names **F266** on its side of the join, and no longer names F200, which is a different finding. Declared 2026-08-19.
**Cross-references:** [[F199b-amplitude-mode-stability-nogo]] (the no-go that set the requirement: a sterile, conserved-charge / super-weakly-coupled relic — this finding supplies it), [[F47-majorana-seesaw-higgs-free]] (the $\nu_R$ total singlet with $Y=0$ forced, and the see-saw — the load-bearing structure), [[F41-hypercharge-higgs-free-su2]] / [[F165-hypercharge-quantisation-from-anomaly-and-mass]] (the $U(1)_Y$ that forces $Y_{\nu_R}=0$), [[F191-dark-matter-rotation-curves-bullet]] (the dark-source requirement + the "sterile-sector excitation" hint, now realised), [[F197-first-excitation-dark-source]] / [[F198-angular-mode-relic-misalignment]] (the $E_g$ route this supersedes for the relic). External: $\nu$MSM (Asaka–Blanchet–Shaposhnikov 2005); Dodelson–Widrow 1994; Shi–Fuller 1999 (resonant); Boyarsky et al. review (X-ray + Lyman-$\alpha$ bounds).

---

## The requirement, and that the model already meets it

F199 closed the $E_g$ route: its modes decay to leptons in $\sim10^{-21}$ s because the condensate's defining job is to set lepton masses. It named the requirement for a real relic — a state with **no SM gauge charge** (sterile), whose only coupling is super-weak, so it is cosmologically long-lived — and flagged the F191 "sterile-sector excitation" as the leading direction.

The model already contains exactly that, and it was **not bolted on**. F47 builds the right-handed neutrino $\nu_R$ as a **total SM singlet**: no colour, no $SU(2)_L$, and hypercharge $Y_{\nu_R}=0$. Crucially, $Y=0$ is **structurally forced** — it is the unique value for which the Higgs-free Majorana mass term is $U(1)_Y$-invariant (F47 M2/M3). So the model's own consistency *requires* a genuinely sterile fermion, whose only link to the visible sector is the small Dirac mixing $M_D$ (mixing angle $\theta\sim M_D/M_R$). F47's 3×3 extension (follow-up #2) gives three sterile masses, so a light (keV) eigenvalue is allowed — the $\nu$MSM structure.

## It passes every bar the $E_g$ sector failed

**Existence (derived).** Genuine sterile singlet, $Y=0$ forced (S1).

**Stability (computed).** A sterile neutrino decays only through its tiny mixing, dominantly $\nu_s\to3\nu$ (NC) with $\Gamma=G_F^2 m_s^5\sin^2\!2\theta/(768\pi^3)$ and the radiative $\nu_s\to\nu\gamma$. At the viable benchmark ($m_s=7.1$ keV, $\sin^2\!2\theta=5\times10^{-12}$):
$$\tau\approx1.3\times10^{27}\ \text{s},\qquad \tau/t_0\approx2.9\times10^{9}.$$
Long-lived by ~9 orders — versus the $E_g$ amplitude mode, which was **~38 orders below** the age of the universe (F199). The contrast is the whole point: a sterile state's decay is mixing-suppressed, a lepton-mass condensate's is not.

| $m_s$ (keV) | $\tau/t_0$ ($\sin^2\!2\theta=5\times10^{-12}$) | stable? |
|---|---|---|
| 1 | $5\times10^{13}$ | yes |
| 3 | $2\times10^{11}$ | yes |
| 7.1 | $2.9\times10^{9}$ | yes |
| 30 | $2\times10^{6}$ | yes |

**Clustering + collisionless (computed/structural).** A keV mass clusters (warm dark matter); the only coupling is the mixing, so $\sigma/m$ is far below the Bullet-Cluster bound (F191 D2 satisfied). The caveat is that keV $\Rightarrow$ *warm*: free-streaming suppresses sub-galactic structure, and Lyman-$\alpha$ sets a lower mass bound ($m_s\gtrsim$ few keV for non-resonant, lower for resonant).

## The abundance window (accommodated, with the real constraints)

| mixing benchmark | $\sin^2\!2\theta$ | X-ray (bound $1.7\times10^{-11}$ at 7 keV) | role |
|---|---|---|---|
| naive single-flavour see-saw ($4m_\nu/m_s$) | $2.8\times10^{-5}$ | **excluded** | would over-mix |
| non-resonant DW for 100% DM | $7.9\times10^{-9}$ | **excluded** | DW alone is ruled out |
| resonant ($\nu$MSM, Shi–Fuller) | $5\times10^{-12}$ | **allowed** | reaches $\Omega_\text{DM}$ |

This reproduces the real status of keV sterile-neutrino dark matter: the naive see-saw mixing and non-resonant Dodelson–Widrow production for the full abundance are X-ray excluded, but **resonant production** (Shi–Fuller, driven by a primordial lepton asymmetry) reaches $\Omega_\text{DM}$ at a smaller, X-ray-allowed mixing — the surviving $\nu$MSM window. The $\nu$MSM consistency is that the DM sterile's Yukawa is decoupled (it contributes negligibly to the active masses), so its mixing is a free parameter in the window, while the two heavier ($\sim$GeV) steriles do the see-saw and baryogenesis.

## What is derived vs computed vs accommodated

| Piece | Status |
|---|---|
| a genuine sterile $\nu_R$ exists; $Y=0$ forced | **Derived** (F47 $U(1)_Y$ invariance) |
| lifetime $\tau/t_0\sim10^9$ at viable mixing | **Computed** (standard sterile-$\nu$ decay) |
| passes where $E_g$ failed by ~38 orders | **Computed contrast** (F199) |
| clusters (warm) + collisionless | **Structural** (massive singlet, mixing-only coupling) |
| naive/DW mixings X-ray excluded; resonant allowed | **Computed** (calibrated X-ray bound) |
| keV mass scale | **Accommodated** — free Majorana eigenvalue $M_R$, not derived |
| resonant production reaching exactly $\Omega_\text{DM}=0.26$ | **Accommodated** — needs the primordial lepton asymmetry, an input |

## The remaining obstruction

Dark matter now has a **viable, model-native identity** — the F47 sterile neutrino — that is stable, clustering, collisionless, and tied to the same see-saw that explains the small active-neutrino mass (so it costs no new sector). What is *not* derived is the **keV scale** (a free eigenvalue of the 3×3 $M_R$) and the **lepton asymmetry** that resonant production needs. That is the dark-matter analog of where F196 left dark energy (the $\Omega_\Lambda$ coincidence) and F198/F199 left the relic (an undetermined scale): the *identity* is settled, a *scale/asymmetry* is the residual.

## Caveats (honest scope)

- The X-ray bound and DW/resonant abundances are order-of-magnitude parametrisations calibrated to the literature, not a full Boltzmann computation; the qualitative window (naive/DW excluded, resonant allowed) is robust, the exact edges are not.
- keV warm DM faces live Lyman-$\alpha$ and Milky-Way-satellite constraints; the surviving window is narrow and is an active observational target (X-ray line searches), which makes this **falsifiable**, not free.
- The keV mass and the lepton asymmetry are inputs; the model accommodates the $\nu$MSM, it does not yet derive it.
- Absolute stability is not claimed — the relic is *long-lived by tiny mixing* (lepton number is violated by the Majorana mass, F47), which is the standard and sufficient situation for sterile-neutrino DM.

## Relation to other findings

Supplies the relic that **F199** showed the $E_g$ sector cannot be, using the **F47** sterile $\nu_R$ ($Y=0$ forced by the **F41/F165** $U(1)_Y$) — realising the **F191** "sterile-sector excitation" hint. Supersedes the **F197/F198** $E_g$ dark-matter route (kept only for dark energy, F193/F196). With this, the dark sector is: dark **energy** = the holographic vacuum back-reaction (F193/F196, residual $\Omega_\Lambda$ coincidence); dark **matter** = the F47 keV sterile neutrino (residual: the keV scale + lepton asymmetry). Both reduced from "what is it?" to "what fixes the one remaining number?"
