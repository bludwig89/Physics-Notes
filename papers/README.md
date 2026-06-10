# A Universe in a Bottle — The Eleven-Paper Series

A peer-review-style write-up of the BCC quantum-cellular-automaton (QCA) model of physics. Each paper is self-contained and replication-grade: it states the construction, gives the derivations, quotes the verification residuals, names the underlying findings (`findings/F*.md`) and modules (`ca-simulation/ca_*.py`), and lists external references.

*Issued 2026-06-08. Supersedes the ten-paper draft in `deprecated/papers-v1/` (the matter sector is now split into three papers — fermions, leptons, baryons — and the dielectric black hole has its own paper). Canonical SI cell aligned to Finding F107 throughout: $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.5978\,\ell_P=1.0664\times10^{-34}$ m.*

## Reading order

| # | Paper | What it establishes |
|---|---|---|
| I | [Base Structure](Paper-01-Base-Structure.md) | BCC Weyl QCA substrate; speed of light as a rotation rate ($c_\text{lat}=1/\sqrt3$); Maxwell as a linearised rotation; the spherical-Pythagorean mass shell. |
| II | [The Photon](Paper-02-Photon.md) | The photon as a bound pair of two spin-½ lattice quanta; massless, luminal, transverse, exactly non-birefringent; supersedes the chiral σ-bilinear. |
| III | [Higgs-Free Mass](Paper-03-Higgs-Free-Mass.md) | Chiral-$SU(2)$ complex-mass step (no Higgs); the $SU(2)_L$ Ward identity; the NJL constituent-mass scale; the Koide relation as cubic equipartition. |
| IV | [Electromagnetism](Paper-04-Electromagnetism.md) | Maxwell from the rotation rule; $U(1)$ minimal coupling forces the paired photon; Aharonov–Bohm + sourced curl end-to-end; charge quantisation and anomaly freedom. |
| V | [Strong Force](Paper-05-Strong-Force.md) | Dynamical $SU(3)$ gluons (even propagator, forced); confinement from exact 2D area law → colour-dielectric dual superconductor → gauge Monte-Carlo; centre-phase closure. |
| VI | [Weak Force](Paper-06-Weak-Force.md) | Chiral $SU(2)_L\times U(1)_Y$ without a Higgs; rank-1 Stueckelberg masses; the derived Weinberg angle ($\sin^2\theta_W=\tfrac14$); end-to-end $\beta$-decay. |
| VII | [Gravity](Paper-07-Gravity.md) | Gravity as an impedance-matched lattice dielectric; $K=e^{2GM/rc^2}$; PPN $\beta=\gamma=1$; the structural Newton constant $G=a^2c^3/(8\pi\sqrt3\,\hbar)$. |
| VIII | [Dielectric Black Hole](Paper-08-Dielectric-Black-Hole.md) | The exponential metric: horizon-free; throat $e$, photon sphere $2\sqrt e$, shadow $2e$ (+4.63% vs Schwarzschild); no Hawking glow; GW echoes. (Reviews F114.) |
| IX | [Fermion Sector](Paper-09-Fermion-Sector.md) | Weyl/Dirac quanta; chirality–helicity correspondence; exactly three generations from $O_h$ (no fourth); anomaly-free first generation. |
| X | [Lepton Sector](Paper-10-Lepton-Sector.md) | Higgs-free hypercharge; the Koide $45^\circ$ equipartition as an EM-selected critical point; the Higgs-free see-saw neutrino. |
| XI | [Baryon Sector](Paper-11-Baryon-Sector.md) | The colour-singlet proton; centre-phase closure (baryon mass = field energy); the dynamical pion; the deuteron bound by the tensor force; the derived NN repulsive core. |

## Headline verified numbers

- $c_\text{lat}=1/\sqrt3=0.5773503$ (rotation-rate slope, axis and body diagonal)
- $\sin^2\theta_W=\tfrac14\Rightarrow m_Z/m_W=2/\sqrt3=1.1547$ (zero-parameter; $1.77\%$ from PDG)
- Koide $Q=0.6666605$ ($0.91\sigma$ from $\tfrac23$); $m_\tau^\text{pred}=1776.97$ MeV ($6.1\times10^{-5}$)
- $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$; $G=6.6743\times10^{-11}$ SI ($3\times10^{-8}$, CODATA round-off)
- Black-hole shadow ratio $2e/3\sqrt3=1.0463$ (+4.63%); throat $e$, photon sphere $2\sqrt e=3.297$, shadow $2e=5.437$ (units $GM/c^2$)
- Deuteron $E_b=2.224$ MeV, $\kappa=0.2316$ fm$^{-1}$; baryon constituent-mass fraction $0.96\%$ of $m_p$

## Standing design decisions (deviations from the Standard Model)

1. Speed of light = rotation rate, not phase velocity (F26).
2. Mass from chiral-$SU(2)$ complex coupling, not a Higgs field; hypercharge on the same gauge field (F27/F41).
3. Photon = bound pair of two spin-½ quanta, not a fundamental spin-1 boson (F69).
4. Gravity = a single impedance-matched lattice dielectric, $K=e^{2GM/rc^2}$ (F64).

See `docs/theory/key-decisions.md` and `findings/` for the full record.
