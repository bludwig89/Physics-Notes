# F210 — Electrical superconductivity on the lattice: the electric S-dual of F86

**Date:** 2026-07-01 - 01:26
**Status:** Confirmed — 16/16 checks PASS. The two coupling-independent BCS universals reproduce to machine precision (2Δ/kT_c → 2π/e^γ, residual 3.8×10⁻¹⁶; ΔC/C_n = 12/(7ζ(3)), residual <10⁻⁹); charge-2e, Φ₀ = h/2e, and the massless-photon reduction are exact; Meissner depth and Josephson frequency are numeric-decisive. The one genuinely open input is the **magnitude** of T_c (needs the emergent-lattice coupling N(0)V from a specific material), exactly as BCS itself leaves it.
**Modules:** `ca-simulation/ca_superconductivity.py` (new)
**Tests:** `tests/findings/test_F210_superconductivity.py` (16/16, pure numpy, <2 s)
**Results:** `test-results/F210_superconductivity.json`
**Cross-references:** [[F86-colour-dielectric-dual-superconductor]] (the *magnetic* dual SC — this is its electric S-dual), [[F117-gap-coupled-dielectric-gluon-propagator]] (gap-coupled dielectric — the over-screening glue face), [[F64-em-connection-gravity]] (the lattice dielectric K — the electron–phonon deformation potential), [[F77-njl-gap-rpa-selfconsistent]] (the self-consistent gap equation reused here), [[F69-paired-spinor-photon]] (the pairing channel + the even-law photon that becomes massive), [[F73-spin0-bound-pair-scalar]] (the neutral spin-0 sibling of the Cooper pair), [[F44-higgs-free-mA-zero-from-rank1-stueckelberg]] / [[F34b-wmu-mass-stueckelberg]] (the Goldstone-eating = Meissner mass), [[F87-charge-coupling-paired-photon]] (U(1) holonomy = flux quantization/Josephson), [[F180-gw-speed]] (c_grav = c_lat, the even-law speed the photon inherits), [[F195-blockspin-element-atom]] (the electron degrees of freedom).

---

## What this closes

Electrical superconductivity did **not** exist in the model. The only prior "superconductor" content was *analogical*: F86's **dual (magnetic)** superconductor for QCD confinement, and the **Cooper-pair** label borrowed for the Higgs/Koide sector (F73/F78). This finding builds the actual condensed-matter phenomenon — electron pairing, an energy gap, zero DC resistance, the Meissner effect, the London depth, flux quantization Φ₀ = h/2e, and the Josephson effect — and shows it is not new physics but the **electric S-dual of F86**, assembled almost entirely from machinery already in the repo.

## The one-paragraph physics

F86 condenses colour-**magnetic** charge; by the dual Meissner effect it expels colour-**electric** flux into a tube (confinement, σ = 2πv²). Ordinary superconductivity is the same construction with electric ↔ magnetic swapped: **electric** charge (paired electrons) condenses and **magnetic** flux is expelled (Meissner) or squeezed into vortices (type II). Every ingredient has a pre-existing home — the gap equation is F77's NJL gap, the Meissner photon mass is F44/F34b's Stueckelberg Goldstone-eating, the flux quantum is F87's U(1) holonomy with pair charge 2e, and the propagating photon is F69's even-law luminal photon (never the excluded birefringent σ-bilinear).

## Task 1 — the pairing glue is derived, and the result is nuanced

On the **bare fundamental lattice** the inter-electron channel is repulsive (Coulomb via the F69 photon), and the only intrinsic bosonic collective mode is the dielectric/graviton wave (F180) whose coupling ∝ G is negligibly small. So the vacuum does **not** superconduct conventionally — a structural statement about the "universe in a bottle."

Superconductivity is therefore an **emergent-lattice** phenomenon: a material crystal of F195 atoms carries acoustic phonons (the coarse elastic mode of the F130–F134 block-spin sector), and these supply the Fröhlich retarded attraction. The model-native content of the electron–phonon vertex is elegant: **the coupling is the electron's sensitivity to a local modulation of the lattice dielectric K** (F64) — a strained cell has a slightly different K, which shifts the confined (E,B) rotation rate = the electron's local energy (F26). Exchanging the propagating strain wave gives

$$V_\text{eff}(q,\omega)=V_c+|g_q|^2\,\frac{2\omega_q}{\omega^2-\omega_q^2},$$

**attractive for $|\omega|<\omega_q$** (SC1a, exact sign). With the acoustic deformation-potential coupling $|g_q|^2=D^2q^2/(2\rho\omega_q)$ and $\omega_q=c_s q$, the static small-$q$ limit is the **$q$-independent BCS contact** $V_\text{eff}(q,0)=-D^2/(\rho c_s^2)$ (SC1b, exact — spread <10⁻¹²). The cutoff $\omega_D=c_s\,(\pi/a_\text{mat})$ is tied to the emergent BZ edge, not fit (SC1c). The over-screening dielectric $K(q,\omega)$ (F117) is the same attraction seen as $\mathrm{Re}\,\varepsilon<0$.

## Task 2 — the gap equation is the F77 NJL gap; the universals are exact

The BCS gap equation and the F77 NJL gap are the **same** self-consistent equation $1=(\text{coupling})\times(\text{loop})$. The $T=0$ gap has the closed form

$$\Delta(0)=\frac{\omega_D}{\sinh(1/N(0)V)}\quad\text{(SC2d, solves }1=N(0)V\,\operatorname{arcsinh}(\omega_D/\Delta)\text{ to }10^{-14}).$$

The crown jewels are **coupling- and cutoff-independent**, which is exactly why they are the honest test that this is genuine BCS and not a fit:

| Universal | Value | Residual | Tier |
|---|---|---|---|
| $2\Delta(0)/k_BT_c$ | $2\pi/e^{\gamma}=3.5277539777$ | $3.8\times10^{-16}$ (at $N(0)V=0.05$); $\omega_D$-independence $<10^{-15}$ | machine |
| $\Delta C/C_n$ | $12/(7\zeta(3))=1.4261269$ | $<10^{-9}$ | machine |

The $\Delta^2(T)$ near-$T_c$ slope confirms $\Delta^2(T)\to\frac{8\pi^2}{7\zeta(3)}(k_BT_c)^2(1-T/T_c)$ (SC2c, ratio → 1.0000 as $T\to T_c$: 0.9998 at $1-T/T_c=2\times10^{-4}$), which is the relation behind the jump. The coherence length is $\xi_0=\hbar v_F/\pi\Delta(0)$.

## Task 3 — the Cooper pair is the charged spin-0 singlet of F69/F73

Two electrons, spin-singlet, symmetric $s$-wave, **charge $2e$ exactly** (integer holonomy, F87; SC3a). It is the charged sibling of the neutral F73 bound pair, and by F69 its phase advances as the **sum** of the constituents → **winding number 2** (SC3b). That factor 2 is the origin of $\Phi_0=h/2e$.

## Task 4 — Meissner/London is the F44/F34b Stueckelberg mass

Inside the condensate the F69 even-law photon eats the condensate phase Goldstone and becomes massive (Anderson–Higgs = Meissner), with Proca dispersion $\omega^2=m_\gamma^2+(c_\text{lat}k)^2$ that reduces **exactly** to the luminal even photon at $m_\gamma=0$ (SC4a). The London depth is $\lambda_L=1/m_\gamma$, $\lambda_L^2=m^*/(\mu_0 n_s(2e)^2)$; the finite-difference London BVP recovers $\lambda_L$ from the $B\sim e^{-x/\lambda_L}$ expulsion (SC4b, 1.9×10⁻⁶), and the $(2e)$ vs $(e)$ screening differs by exactly $1/2$ — the pair-charge signature (SC4c, exact).

## Task 5 — flux quantum h/2e and Josephson from the F87 holonomy

Single-valuedness of the charge-$2e$ order parameter forces $\oint\nabla\theta\cdot d\mathbf l=2\pi n$, so trapped flux is $\Phi=n\,h/2e$. **$\Phi_0=h/2e=2.0678\times10^{-15}$ Wb, exactly half the naive $h/e$** (SC5a) — the cleanest signature that the carriers are pairs. $\kappa=\lambda_L/\xi_0$ vs $1/\sqrt2$ sorts type I/II vortices (S-dual of the F86 flux tube; SC5b). The DC ($I=I_c\sin\Delta\theta$) and AC ($\hbar\,\partial_t\Delta\theta=2eV$) Josephson relations hold, with the recovered Josephson frequency $f_J=2eV/h$ matching to 10⁻¹⁰ (SC5c).

## Task 6 — zero DC resistance

London eq. 1, $\partial_t\mathbf J_s=(n_s(2e)^2/m^*)\mathbf E$, with $\mathbf E=0$ gives $\partial_t\mathbf J_s=0$: the supercurrent is a constant of motion — persistent, exactly (SC6, drift = 0.0), while a Drude ($T>T_c$, gapless) control decays. The gap forbids single-particle backscattering (no final state within $\Delta$ of the Fermi surface) and the condensate momentum is a rigid collective coordinate (F118/F130 rigidity).

## Test battery (16/16)

| ID | Statement | Tier | Residual |
|----|-----------|------|----------|
| SC1a | phonon exchange attractive for $\|\omega\|<\omega_q$, repulsive above | exact | 0 |
| SC1b | small-$q$ attraction is $q$-independent constant $-V$ (BCS contact) | exact | <10⁻¹² |
| SC1c | Debye cutoff $=c_s\cdot$ BZ edge (lattice quantity) | exact | <10⁻¹⁵ |
| SC2a | $2\Delta(0)/k_BT_c=2\pi/e^\gamma$, coupling & cutoff independent | machine | 3.8×10⁻¹⁶ |
| SC2b | $\Delta C/C_n=12/(7\zeta(3))=1.4261$ | machine | <10⁻⁹ |
| SC2c | $\Delta^2(T)$ near-$T_c$ slope $=8\pi^2/(7\zeta(3))(k_BT_c)^2$ | numeric | 2×10⁻⁴ |
| SC2d | $T{=}0$ gap solves the F77-form gap equation | machine | <10⁻¹⁴ |
| SC3a | Cooper-pair charge $=2e$ exactly | exact | 0 |
| SC3b | pair winds 2× (F69 sum) + spin-0 $s$-wave singlet boson | exact | 0 |
| SC4a | massive photon $m{=}0$ reduces to luminal even photon | exact | <10⁻¹⁵ |
| SC4b | Meissner $B$-expulsion decay length $=\lambda_L$ | numeric | 1.9×10⁻⁶ |
| SC4c | $\lambda_L(2e)/\lambda_L(e)=1/2$ exactly (pair signature) | exact | <10⁻¹² |
| SC5a | $\Phi_0=h/2e$ (= half $h/e$; carriers are pairs) | exact | <10⁻³⁰ |
| SC5b | $\kappa=\lambda_L/\xi_0$ sorts type I/II | exact | 0 |
| SC5c | Josephson DC $I{=}I_c\sin\Delta\theta$ & AC $f_J{=}2eV/h$ | machine | <10⁻¹⁰ |
| SC6 | persistent supercurrent $\partial_t J_s{=}0$; normal control decays | exact | 0 |

## New information

1. **Superconductivity is the electric S-dual of confinement.** F86 (magnetic condensate → electric-flux tube) and F210 (electric condensate → magnetic-flux expulsion) are one construction under electric↔magnetic exchange. The model did not need a new mechanism for either.
2. **The two BCS universals are model outputs, not inputs.** $2\Delta/k_BT_c=3.528$ and $\Delta C/C_n=1.426$ fall out of the reused F77 gap equation to machine precision, independent of the (material-specific) coupling — a genuine reproduction of measured superconductor phenomenology.
3. **The glue is the dielectric K.** The electron–phonon coupling is the electron's sensitivity to a strain-modulated lattice dielectric (F64) — the *same* field that carries gravity — unifying the pairing glue with the model's existing EM/gravity treatment.
4. **A sharp structural statement:** the bare fundamental lattice does not superconduct (repulsive channel + graviton-only glue); conventional superconductivity is strictly an **emergent-lattice** phenomenon requiring a material crystal of F195 atoms.

## Open / next

- The **magnitude** of $T_c$ needs a specific material's $N(0)V$ (the emergent-lattice deformation potential $D$, density $\rho$, sound speed $c_s$) — BCS leaves this open too; deriving $D$ from the F64 dielectric strain response for a named crystal would make $T_c$ absolute.
- Unconventional (d-wave) pairing from BCC anisotropy if the s-wave channel is ever found net-repulsive for a given material.
- A live CASIM condensate slab + Josephson junction as engine scenarios (here done as reduced BVP/ODE demonstrations); wiring the massive F69 even-law photon into a full 3-D `casim` run.
- The retarded Coulomb pseudopotential $\mu^*=\mu/(1+\mu\ln(E_F/\omega_D))$ (Anderson–Morel) from the F64 dielectric, to quantify the net attraction margin.
