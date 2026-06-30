# F199 — Working out the amplitude mode from F73/F93: $\Omega_\text{DM}=0.26$ does **not** fall out, because stability fails before abundance — the EW radial mode is the observed 125 GeV Higgs, and the $E_g$ second-shell amplitude mode couples to leptons as $g_\ell=m_\ell/f$ (its defining role) and decays in $\sim10^{-21}$ s ($\sim$38 orders below cosmological); the dark-matter obstruction moves from abundance to a missing conserved charge

**Date:** 2026-06-30 - 20:40
**Numbering:** **F199** (re-checked; prior max F198).
**Status:** **No-go for the $E_g$ sector as the dark-matter relic; redirects the search.** The decay kinematics are standard and the lifetime gap ($\sim$38 orders) is far too large for any input uncertainty to rescue. Honest negative that corrects F197/F198 and relocates the dark-matter candidate. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F199_amplitude_mode_stability.py` (self-contained, real arithmetic).
**Tests / results:** `tests/findings/test_F199_amplitude_mode_stability.py` → `test-results/F199_amplitude_mode_stability_test.json` (5/5); fork dump `test-results/F199_amplitude_mode_stability.json`.
**Cross-references:** [[F198-angular-mode-relic-misalignment]] (the freeze-out route this examines), [[F197-first-excitation-dark-source]] (the candidate identification this corrects), [[F73-spin0-bound-pair-scalar]] (the EW radial mode = 125 GeV Higgs; the composite-mass kinematics), [[F93-orthorhombic-Eg-vacuum]] (O1: the $E_g$ condensate IS the lepton-mass crystal field — the coupling that kills stability), [[F191-dark-matter-rotation-curves-bullet]] (the "sterile-sector excitation" hint, now the leading direction), [[F97-baryon-no-go-centre-closure]] (the $Z_3$ centre charge — template for a conserved-charge stabiliser). External: SM Higgs width $\Gamma_H\approx4$ MeV; Yukawa scalar decay $\Gamma(S\to\ell\bar\ell)=\frac{g_\ell^2 m_S}{8\pi}\beta^3$.

---

## The question, taken at face value

F198 found that the heavy amplitude mode could reach $\Omega_\text{DM}h^2\approx0.12$ via thermal freeze-out (the WIMP window), unlike the light angular mode. The next step is to work out that mode's actual mass and annihilation channels from F73/F93 and see whether $\Omega_\text{DM}=0.26$ falls out. It does not — and the reason is more basic than the abundance.

## Two "amplitude modes" must be separated (the F197/F198 fix)

**Mode 1 — the electroweak radial mode.** F73 identifies the radial/breathing mode of the *symmetry-breaking* condensate as the Cooper-pair scalar = the **observed 125 GeV Higgs**. It decays ($\Gamma_H\approx4$ MeV → $\tau\approx1.6\times10^{-22}$ s) and has been seen at the LHC. Not dark matter, by observation.

**Mode 2 — the $E_g$ second-shell amplitude mode.** This is the scalar F197/F198 actually meant: the radial fluctuation of the F93 orthorhombic condensate. But F93 O1 establishes that this condensate **is the crystal field that sets the charged-lepton mass hierarchy** — it lives on the $T_{1u}$ generation triplet and splits the three lepton masses. So a fluctuation $\delta e$ of its amplitude **modulates the lepton masses directly**, i.e. couples linearly to the lepton mass operator:
$$\mathcal L \supset \frac{\delta e}{f}\sum_\ell m_\ell\,\bar\ell\ell,\qquad g_\ell=\frac{m_\ell}{f}.$$

## The stability no-go

With $f\simeq v/2=123$ GeV (F44/F73) the dominant decay is to $\tau^+\tau^-$, $g_\tau=m_\tau/f=0.014$, giving
$$\Gamma=\sum_\ell\frac{g_\ell^2 m_S}{8\pi}\Big(1-\tfrac{4m_\ell^2}{m_S^2}\Big)^{3/2},\qquad \tau=\hbar/\Gamma.$$

| $m_S$ | lifetime | orders below age of universe |
|---|---|---|
| 10 GeV | $9.7\times10^{-21}$ s | 38 |
| 50 GeV | $1.6\times10^{-21}$ s | 38 |
| 123 GeV (natural) | $6.4\times10^{-22}$ s | 39 |
| 500 GeV | $1.6\times10^{-22}$ s | 39 |
| 3 TeV | $2.6\times10^{-23}$ s | 40 |

Across the entire EW–TeV range the $E_g$ amplitude mode decays in $\sim10^{-21}$ s — **roughly 38 orders of magnitude below cosmological time** ($t_0\approx4.4\times10^{17}$ s). A thermal relic must be cosmologically stable; this one is not. Even restricting to the electron channel ($g_e=4\times10^{-6}$) gives $\tau\sim10^{-14}$ s — still instantaneous.

**Therefore $\Omega_\text{DM}=0.26$ does not fall out.** The F198 freeze-out window is *moot*: the relic abundance is undefined for a state that decays before nucleosynthesis. The very coupling that would set the abundance ($g_\ell=m_\ell/f$, the condensate's reason for existing) is what makes it decay.

## The obstruction relocated: from abundance to a missing conserved charge

A stable thermal relic needs a **conserved charge** (a $Z_2$ or $U(1)$) under which it is the *lightest* carrier, forbidding decay to SM. The $E_g$ condensate has no such charge: its amplitude mode is even under the $D_{2h}$ stabiliser (F93 O3) and couples linearly to leptons — nothing forbids $S\to\ell\bar\ell$. This is why the $E_g$ sector, despite having the right *kinematics* in F197 ($w=-1$ VEV + gapped clustering modes), fails as the dark-matter relic: kinematic suitability was necessary but not sufficient — **stability was the unchecked assumption.**

This also corrects the F197 "collisionless" check: that proxy used the small self-coupling $\lambda_6$, but the dominant interaction is the lepton coupling $m_\ell/f$, which is not small — the $E_g$ modes are both unstable *and* not dark-sector-decoupled.

Model-native directions where a conserved charge *does* exist (flagged speculative, not derived):

- a **sterile-sector excitation** with no SM gauge charge (the F191 "sterile-sector" hint) — automatically long-lived if its only coupling is gravitational/tiny;
- a **topologically conserved** lattice excitation — a winding/texture of $U(x)$ or an orthorhombic-domain skyrmion carrying a conserved winding number;
- the lightest state of a **hidden conserved lattice charge** — a "dark baryon," the analog of the $Z_3$ centre closure that stabilises ordinary baryons (F97).

## What is derived vs computed vs posited

| Piece | Status |
|---|---|
| EW radial mode = observed 125 GeV Higgs, decays | **Identified** (F73) + known $\Gamma_H$ |
| $E_g$ amplitude mode couples to leptons as $g_\ell=m_\ell/f$ | **Derived** (F93 O1: it is the lepton crystal field) |
| lifetime $\sim10^{-21}$ s, $\sim$38 orders below cosmological | **Computed** (standard Yukawa-scalar width) |
| instability generic across EW–TeV | **Computed** (mass scan) |
| freeze-out abundance moot (no stable relic) | **Inferred** |
| DM needs a conserved charge $E_g$ lacks | **Derived** (symmetry argument) |
| sterile / topological / hidden-charge candidates | **Posited** — directions, not derivations |

## Caveats (honest scope)

- The 38-order lifetime gap dwarfs every input uncertainty (mass, exact $f$, sub-leading channels), so the no-go is robust; this is not a near-miss.
- It is *logically possible* to bolt a $Z_2$ onto a new scalar by hand, but that scalar would then **not** be the $E_g$ amplitude mode (it could not set lepton masses) — so this is a no-go specifically for the F197/F198 identification, not for "any scalar."
- The constructive candidates (sterile/topological/hidden-charge) are stated as the next search directions; none is derived here.

## Relation to other findings

Corrects **F197** (kinematic suitability of the $E_g$ sector is necessary but not sufficient — stability fails) and closes the **F198** freeze-out route (the WIMP window cannot be realised by an unstable state). Uses **F73** (EW radial mode = Higgs) and **F93 O1** (the $E_g$ condensate is the lepton-mass crystal field — the fatal coupling). Relocates the dark-matter candidate to a conserved-charge sector, promoting the **F191** "sterile-sector excitation" hint and the **F97** $Z_3$-centre stabiliser template to the leading directions. Leaves dark matter as an **open identity problem** (a stable, neutral, conserved-charge relic), distinct from the now-settled dark-energy sector (F193/F196).
