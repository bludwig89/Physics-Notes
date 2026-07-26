# Dark Sector — Overview & Falsifiable Points

**Date:** 2026-06-30 - 22:30
**Scope:** Current state of the dark-energy and dark-matter program under F178 (exact GR, constant induced $G$), and the observational handles that could falsify it.

> **Numbering note:** the dark-sector chain runs F191→F192→F193→F194→F196→F197→F198→**F199**(amplitude-mode)→**F200**(sterile-ν)→F201. Concurrent lepton-sector sessions also wrote an `F199-angular-self-duality` and an `F200-eg-sextic-coupling` — those two are **not** dark sector. Numbers collided; content is distinct.

---

## 1. Where the sector stands

Under **F178** the gravity sector is exact GR with a *constant* induced $G$. That single decision drives everything below: the lattice dielectric only *responds* to mass, so it cannot itself be dark matter, and modified-gravity routes inherit the Bullet-Cluster failure. The sector therefore resolves into two genuinely separate objects, each reduced from "what is it?" to "what fixes the one remaining number?"

| | Identity | Status | Residual |
|---|---|---|---|
| **Dark energy** | Holographic back-reaction of the ontic vacuum ($w=-1$) | Identity settled (F193/F196) | The $\Omega_\Lambda\approx0.69$ coincidence |
| **Dark matter** | F47 keV sterile right-handed neutrino ($\nu$MSM) | Identity settled (F200/F201) | The keV scale + primordial lepton asymmetry |

A key structural result: the two are **not** the same object. The empty lattice gravitates as exactly zero (F193), so a uniform vacuum term can only ever be dark *energy* (non-normalizable, feeds only the Friedmann mode); dark *matter* must be a clustering, collisionless **source** (F191).

---

## 2. Dark energy chain (F164 → F192 → F193 → F196)

- **F164** — bare BCC zero-point density overshoots observed $\rho_\Lambda$ by $\log_{10}\approx120.8$; sign also wrong for an all-fermion vacuum. The classic CC problem, quantified.
- **F192** — under the full-tensor source, vacuum $w=-1$ gives $\rho+3p=-2\rho<0$, so it **accelerates** — the *sign* is now correct (the demoted energy-only law would decelerate). Magnitude still open.
- **F193** — the **ontic vacuum gravitates as exactly zero**: the beable $T^{00}$ on the empty lattice $=0$, so $K=1$ and the bare CC $=0$ in the ontology (kills both magnitude *and* sign of F164). The $+\tfrac12\hbar\omega$ zero-point is a superimposable that does not gravitate.
- **F196** — the small residual $\rho_\Lambda$ is the **holographic back-reaction**, diluted by one factor $(a/R_H)^2$. The exponent $p=2$ is **derived two ways** (black-hole $M\propto R$; area entropy + Gibbons–Hawking), landing $0.10$ dex from $\rho_\Lambda$. The 121-order CC problem is reduced to the leftover $\Omega_\Lambda\approx0.69$ coincidence.

**Net:** dark energy = $w=-1$ holographic vacuum residual. Magnitude predicted to within ~0.1 dex; the surviving open piece is an $O(1)$ coincidence, not a 120-order catastrophe.

---

## 3. Dark matter chain (F191 → F194 → F197 → F198 → F199 → F200 → F201)

- **F191** — rotation curves cannot separate a dark halo from modified gravity, but the **Bullet-Cluster lensing/gas offset** favours a dark *source*. The model needs dark matter, not modified gravity.
- **F194** — the model-native **emergent-gravity** ("DM without DM") route is **falsified** by the Bullet Cluster: its phantom density is a local functional of the baryons, so lensing tracks the gas, not the collisionless galaxies. The appealing $a_0=cH_0/6$ coincidence (within 3%) survives only as a hint that the *same vacuum sector* sets the scale — but it must enter as a clustering source.
- **F197** — discriminator: a near-vacuum channel can carry cold DM **iff** it has a gapped branch. The F93 $E_g$ second-shell condensate qualifies (VEV → $w=-1$; gapped modes → cold, clustering); the F69 paired-spinor photon is excluded (gapless → radiation). Tentatively named the $E_g$ light angular mode the DM candidate.
- **F198** — computes the $E_g$ relic abundance. The **angular mode under-produces by ~15 orders** (misalignment needs $f\sim10^{13}$–$10^{16}$ GeV, condensate gives $f\sim v/2$). The **amplitude mode** reaches the WIMP window via freeze-out — candidate flips heavy.
- **F199 (amplitude-mode no-go)** — but the $E_g$ amplitude mode **is the lepton-mass crystal field**, so it couples as $g_\ell=m_\ell/f$ and **decays in $\sim10^{-21}$ s** (~38 orders below cosmological). The whole $E_g$ route fails on **stability**, not abundance. DM needs a *conserved charge* the $E_g$ sector lacks.
- **F200 (sterile-ν)** — the model already contains one: the **F47 right-handed neutrino**, a total SM singlet with $Y=0$ **structurally forced** (the unique $U(1)_Y$-invariant Majorana term). At the viable $\nu$MSM benchmark ($m_s=7.1$ keV, $\sin^2 2\theta=5\times10^{-12}$) it is long-lived ($\tau/t_0\sim10^9$), warm-clustering, and collisionless. Naive see-saw and non-resonant Dodelson–Widrow mixings are X-ray excluded; **resonant (Shi–Fuller) production** reaches $\Omega_{\rm DM}$ in the surviving window.
- **F201** — the keV scale is not bolted on: the F93/F76 $Z_3$ ($E_g$) generation texture applied to the F47 Majorana matrix has **cancellation nodes** where one eigenvalue $\to0$. One light sterile is therefore **structural** (same reason the electron is the lightest lepton); with $M_{R0}\sim$ GeV and node-proximity $\delta_\nu\approx0.14°$ it lands $M_1\approx5.6$ keV, $M_3\approx5.6$ GeV — the $\nu$MSM split. keV is *natural*, not yet *pinned*.

**Net:** dark matter = the F47 keV sterile neutrino, tied to the same see-saw that explains the small active-neutrino mass (costs no new sector). Open: the keV eigenvalue and the lepton asymmetry resonant production needs.

---

## 4. Falsifiable points — what we can test against

These are ordered roughly by how cleanly a near-term measurement could kill the current picture. **All six are built out as quantified, currently-evaluable tests in finding F203** (`gr_fork_F203_dark_sector_falsifiers.py` + `test_F203_dark_sector_falsifiers.py`, 7/7 PASS): each carries a model prediction, a sourced 2025 datum, a margin, a status, and an explicit falsifier. Current tally: **0 falsified, 3 under_pressure (T1/T2/T3), 3 consistent (T4/T5/T6)**.

### 4.1 keV sterile-neutrino X-ray decay line  *(strongest, near-term)*
The relic decays radiatively $\nu_s\to\nu\gamma$, emitting a **monochromatic X-ray line at $E_\gamma=m_s/2$**. The model lands $m_s\approx5.6$ keV (F201) → line at **~2.8 keV**; the 7.1 keV $\nu$MSM benchmark (F200) → **3.5 keV** line. The allowed mixing is a *narrow* resonant window ($\sin^2 2\theta\sim5\times10^{-12}$), bounded above by existing X-ray non-detections and below by requiring $\Omega_{\rm DM}$.
- **Falsifier:** a clean X-ray survey (XRISM, Athena) that excludes a decay line across $\sim2$–$15$ keV at the predicted mixing rules out the model-native relic. Conversely, a confirmed line fixes $m_s$ and would be a direct hit.
- **Status in model:** falsifiable, *not* free — F200 flags this explicitly.
- **Quantified (F205):** the full Boltzmann solve gives non-resonant Dodelson-Widrow $\sin^2 2\theta=6.1\times10^{-9}$ for $\Omega_{\rm DM}$ — **2.55 dex above** the aggregate X-ray bound, so non-resonant DM is X-ray excluded. Resonant production is up to ~580× more efficient and clears the X-ray bound for a sufficient lepton asymmetry.

### 4.2 Warm-dark-matter small-scale structure  *(near-term)*
A keV mass is **warm**: free-streaming suppresses sub-galactic structure. Predicts a **cutoff in the halo mass function**, fewer Milky-Way satellites, and a Lyman-α forest power suppression.
- **Falsifier:** Lyman-α + satellite-count bounds already push $m_s\gtrsim$ few keV (non-resonant); resonant production relaxes this. If structure data force $m_s$ above the X-ray-allowed window, the candidate is squeezed out. This is a live two-sided constraint (X-ray from above on mixing, Lyman-α from below on mass).
- **Quantified (F205):** from the computed frozen sterile spectrum, the Lyman-α mass floor is **~41 keV (non-resonant, reproduces the cited combined bound) → ~15 keV (coldest resonant, Viel bound) → ~9 keV (coldest + conservative bound)**. The model's 5.6 keV (F201) and the 7.1 keV benchmark sit **below all of these** → the keV sterile is under quantified pressure as 100% DM, viable only sub-dominant or if the full lepton-number-depletion QKE threads the cold + X-ray-allowed corner.

### 4.3 Dark energy is strictly $w=-1$ (no evolution)  *(near-term, topical)*
F192/F196/F197 make dark energy the **homogeneous condensate VEV / holographic residual** → $w=-1$ exactly, with no quintessence-like field rolling. The picture predicts **no measurable $w(z)$ evolution**.
- **Falsifier:** a robust DESI/Euclid detection of evolving dark energy ($w\neq-1$, or $w_0$–$w_a$ away from $(-1,0)$) would contradict the pure-VEV identity and force a dynamical component the current chain does not have. (This is the most observationally *active* tension to watch.)

### 4.4 Lensing always tracks the collisionless component  *(passed; standing falsifier)*
F178+F191+F194 require a real collisionless dark *source*; modified-gravity/dielectric reweighting is excluded. The model **predicts lensing mass follows the collisionless matter**, never the gas — the Bullet-Cluster behaviour.
- **Falsifier:** a merging-cluster system where lensing demonstrably sits on the X-ray gas (no collisionless offset) would break the dark-source requirement. Current data (Bullet, and similar mergers) are consistent.

### 4.5 DM is *not* a WIMP and *not* a QCD axion  *(consistency check)*
F198 kills the ALP-misalignment route; F199 kills the $E_g$ WIMP route on stability. The model-native identity is specifically a keV sterile neutrino.
- **Falsifier (soft):** a confirmed GeV–TeV WIMP direct-detection signal, or a QCD-axion detection, would sit outside the model's predicted identity. Current null results from direct-detection and axion searches are *consistent* with the model. (Soft because a second sub-dominant component is not strictly excluded.)

### 4.6 $a_0 = cH_0/6$ coincidence  *(diagnostic, not a clean falsifier)*
F194's emergent-gravity route is dead as a DM mechanism, but the numerical coincidence $a_0^{\rm model}=1.16\times10^{-10}$ m/s² (ratio 0.97 to empirical) suggests the vacuum sector sets the MOND-like scale. Not a standalone falsifier since the mechanism it belonged to is falsified; retained as a hint that DE and the galactic acceleration scale share one number.

---

## 5. Open residuals (what would *complete* the sector)

| Sector | Settled | Outstanding number |
|---|---|---|
| Dark energy | Identity ($w=-1$ holographic residual), sign, magnitude to ~0.1 dex | The $\Omega_\Lambda\approx0.69$ coincidence |
| Dark matter | Identity (F47 keV sterile ν), stability, clustering, collisionless | keV eigenvalue $M_1$ (needs $M_{R0}$ + node-proximity $\delta_\nu$); primordial lepton asymmetry for resonant production |

Both have been driven from "what is the dark sector?" to "what fixes one remaining scale/coincidence" — the same posture for DE (F196) and DM (F201).

### Highest-value next steps
1. **Pin the keV eigenvalue** — derive (or bound) $M_{R0}$ and $\delta_\nu$ from the QCA rule rather than the $\nu$MSM scale, turning the X-ray line position into a sharp prediction.
2. **Lepton asymmetry / full L-depletion QKE** — F205 shows the fixed-$L$ pass cannot simultaneously deliver a cold spectrum *and* X-ray-allowed mixing at 7.1 keV; a depletion-tracking QKE (F202 sector) is the one door that could relieve the T2 pressure.
3. **Confront $w=-1$ with current DESI/Euclid** $w(z)$ data directly — the cleanest live test of the dark-energy half.
4. **Real CMB + structure-growth battery** for the keV warm relic (F205 did the linear free-streaming; the CMB third-peak + growth confrontation with a proper transfer function is the remaining piece; F191/F197 used toy profiles only).

---

## 6. Caveat on rigor

Several dark-sector findings still use **toy galactic/cluster profiles** (F191/F194/F197). The keV-sterile abundance and free-streaming, however, are **no longer order-of-magnitude**: F205 does the momentum-resolved Boltzmann (QKE) production and the free-streaming → thermal-equivalent-mass mapping, narrowing the T1/T2 margins to computed numbers (DW X-ray exclusion 2.55 dex; Lyman-α floor ~41 keV non-resonant / ~9–15 keV coldest resonant). Residual uncertainties there are the standard ~factor-2 QCD-epoch normalisation and the fixed-lepton-number resonant pass (no back-reaction depletion); full 3D hydrodynamic Lyman-α simulations remain out of scope (linear free-streaming is matched to published simulated bounds, as is standard). The *directions* (dark source required, emergent gravity falsified, $E_g$ unstable, sterile-ν viable-but-pressured) are robust.
