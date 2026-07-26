# A Universe in a Bottle — The Eleven-Paper Series

A peer-review-style write-up of the BCC quantum-cellular-automaton (QCA) model of physics. Each paper is self-contained and replication-grade: it states the construction, gives the derivations, quotes the verification residuals, names the underlying findings (`findings/F*.md`) and modules (`ca-simulation/ca_*.py`), and lists external references.

*Issued 2026-06-08. Supersedes the ten-paper draft in `deprecated/papers-v1/` (the matter sector is now split into three papers — fermions, leptons, baryons — and the dielectric black hole has its own paper). Canonical SI cell aligned to Finding F107 throughout: $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.5978\,\ell_P=1.0664\times10^{-34}$ m.*

*Revision (2026-07-01): the horizon-free "dielectric black hole" paper (formerly Paper VIII, F114) is **deprecated** following the adoption of the full-tensor induced Einstein equation (F178; see Paper VII §4.2) — the exact strong-field object is Schwarzschild/Kerr, and the dielectric is its vacuum/weak-field representation. The deprecated paper is retained at `deprecated/Paper-08-Dielectric-Black-Hole.md`. Papers IX–XIII are renumbered consecutively to VIII–XII.*

## Reading order

| # | Paper | What it establishes |
|---|---|---|
| I | [Base Structure](Paper-01-Base-Structure.md) | BCC Weyl QCA substrate; speed of light as a rotation rate ($c_\text{lat}=1/\sqrt3$); Maxwell as a linearised rotation; the spherical-Pythagorean mass shell. |
| II | [The Photon](Paper-02-Photon.md) | The photon as a bound pair of two spin-½ lattice quanta; massless, luminal, transverse, exactly non-birefringent; supersedes the chiral σ-bilinear. |
| III | [Higgs-Free Mass](Paper-03-Higgs-Free-Mass.md) | Chiral-$SU(2)$ complex-mass step (no Higgs); the $SU(2)_L$ Ward identity; the NJL constituent-mass scale; the Koide relation as cubic equipartition. |
| IV | [Electromagnetism](Paper-04-Electromagnetism.md) | Maxwell from the rotation rule; $U(1)$ minimal coupling forces the paired photon; Aharonov–Bohm + sourced curl end-to-end; charge quantisation and anomaly freedom. |
| V | [Strong Force](Paper-05-Strong-Force.md) | Dynamical $SU(3)$ gluons (even propagator, forced); confinement from exact 2D area law → colour-dielectric dual superconductor → gauge Monte-Carlo; centre-phase closure. |
| VI | [Weak Force](Paper-06-Weak-Force.md) | Chiral $SU(2)_L\times U(1)_Y$ without a Higgs; rank-1 Stueckelberg masses; the derived Weinberg angle ($\sin^2\theta_W=\tfrac14$); end-to-end $\beta$-decay. |
| VII | [Gravity](Paper-07-Gravity.md) | Gravity as an impedance-matched lattice dielectric ($K=e^{2GM/rc^2}$, PPN $\beta=\gamma=1$), reclassified as the vacuum/weak-field representation of the canonical induced Einstein equation; the structural Newton constant $G=a^2c^3/(8\pi\sqrt3\,\hbar)$; exact Schwarzschild/Kerr in the strong field. |
| VIII | [Fermion Sector](Paper-08-Fermion-Sector.md) | Weyl/Dirac quanta; chirality–helicity correspondence; exactly three generations from $O_h$ (no fourth); anomaly-free first generation. |
| IX | [Lepton Sector](Paper-09-Lepton-Sector.md) | Higgs-free hypercharge; the Koide $45^\circ$ equipartition as an EM-selected critical point; the Higgs-free see-saw neutrino. |
| X | [Baryon Sector](Paper-10-Baryon-Sector.md) | The colour-singlet proton; centre-phase closure (baryon mass = field energy); the dynamical pion; the deuteron bound by the tensor force; the derived NN repulsive core. |
| XI | [One Currency (Unification)](Paper-11-Unification-Rotation-Currency.md) | Synthesis: mass, energy, light, and gravity are one rotation rate $\Omega$ read four ways; $E=mc^2$ makes the energy-coupled dielectric gravity *forced*, not merely permitted. (Draws on F26/F167/F69/F68/F168/F64/F106.) |
| XII | [The Koide Angle](Paper-12-Koide-Angle.md) | The charged-lepton **phase**: $\delta^{*}=\tfrac29$ as the $E_g$ representation weight $\dim E_g/\dim(T_{1u}\otimes T_{1u})$; unified with the Koide amplitude by the saturation self-duality $3\delta=Q$ (radial half BPS-derived, angular half $=$ the one shared residual); full charged-lepton shape to $\le0.007\%$, zero shape parameters. (Findings F174–F177.) |

## Headline verified numbers

- $c_\text{lat}=1/\sqrt3=0.5773503$ (rotation-rate slope, axis and body diagonal)
- $\sin^2\theta_W=\tfrac14\Rightarrow m_Z/m_W=2/\sqrt3=1.1547$ (zero-parameter; $1.77\%$ from PDG)
- Koide $Q=0.6666605$ ($0.91\sigma$ from $\tfrac23$); $m_\tau^\text{pred}=1776.97$ MeV ($6.1\times10^{-5}$)
- $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$; $G=6.6743\times10^{-11}$ SI ($3\times10^{-8}$, CODATA round-off)
- Strong-field black hole: exact Schwarzschild/Kerr (horizon, shadow $3\sqrt3\,M$); the earlier horizon-free dielectric-metric shadow prediction ($2e/3\sqrt3=1.0463$, +4.63%) is superseded (deprecated, F114→F178→F183)
- Deuteron $E_b=2.224$ MeV, $\kappa=0.2316$ fm$^{-1}$; baryon constituent-mass fraction $0.96\%$ of $m_p$

## Standing design decisions (deviations from the Standard Model)

1. Speed of light = rotation rate, not phase velocity (F26).
2. Mass from chiral-$SU(2)$ complex coupling, not a Higgs field; hypercharge on the same gauge field (F27/F41).
3. Photon = bound pair of two spin-½ quanta, not a fundamental spin-1 boson (F69).
4. Gravity = the induced Einstein equation sourced by the full stress-energy tensor (F178); the single impedance-matched lattice dielectric $K=e^{2GM/rc^2}$ (F64) is its vacuum/weak-field representation.

See `docs/theory/key-decisions.md` and `findings/` for the full record.

## Companion and applied notes

These are not core papers (I–XII); they are focused expansions or engineering applications of a single sector.

| Note | Sector | What it covers |
|---|---|---|
| [Companion Note 1 — The Graviton](Companion-Note-01-The-Graviton.md) | Gravity (Paper VII) | Deep account of the graviton: why it exists (zero-tree-stiffness / induced loop), its characteristics with exactness tiers (massless, spin-2, luminal at $c_\text{lat}=1/\sqrt3$, non-birefringent), its effects (Newtonian/GR limit, GWs, UV dispersion, geon/one-cell remnant), and its measurability. |
| [Applied Note 1 — EHD Ionocraft Efficiency](Applied-Note-01-EHD-Ionocraft-Efficiency.md) | Electromagnetism (Paper IV) | Ionocraft/asymmetric-capacitor thrust in the EM sector; efficiency formulas and the zero-vacuum-thrust prediction. |
