# F207 — The Casimir effect in the BCC Weyl-QCA model: the force is reproduced exactly from the F69 photon as a source/$H_\text{int}$ effect, consistent with F193 (the homogeneous zero-point sum does not gravitate); the Casimir *shift* gravitates as beable binding energy $\Delta m=E_C/c^2$ — degenerate with SEP vacuum-buoyancy, so Archimedes cannot discriminate

**Date:** 2026-06-30 - 21:32
**Numbering:** **F207** (re-checked per CLAUDE.md; F206 was the prior committed max, a concurrent session took F208 — F207 verified free).
**Status:** Confirmed — 6/6 checks PASS. **C2 is exact-algebraic** (closed-form Abel–Plana reduction returning $-\pi^2\hbar c/240L^4$ from the exact IR dispersion); C1 machinery validated to $3.5\times10^{-5}$; C3 directional structure exact (axis-linear $\Rightarrow$ zero correction); G1 exact (Gauss-law) with an **honest non-discrimination** result; D1 exact pair correlation. No new physics introduced.
**Module:** `ca-simulation/ca_casimir.py`
**Test / results:** `tests/findings/test_F207_casimir.py` (6/6) → `test-results/F207_casimir.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the photon and its exact IR dispersion + non-birefringence), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$, the even-law rotation), [[F107-canonical-a-adoption-L4-grb-gate]] (the cell $a$ as UV cutoff), [[F193-ontic-vacuum-gravitates-as-zero]] (beable vs superimposable; the load-bearing consistency partner), [[F178-gravity-full-tensor-adoption]] / [[F106-psi-K-sourcing-derivation]] (the dielectric source $\nabla^2\ln K=-8\pi T^{00}$), [[F30-photon-dispersion-order-anisotropy-birefringence]] (even-channel dispersion correction), [[F204-alcubierre-warp-structural-exclusion]] (precedent: confront a known result with the model's constraints). Research phase: `references/casimir-force-literature-and-model-integration.md`; brief: `docs/design/casimir-effect-build-brief.md`. External: Jaffe 2005 (PRD 72, 021301); Nikolić 2016 (arXiv:1605.04143); Ishikawa et al. 2020 (lattice-fermion Casimir); Calloni et al. 2014 / Avino et al. 2020 (Archimedes); Wilson et al. 2011 (DCE).

---

## The question

The Casimir force is the one measured, room-temperature observable routinely attributed to "zero-point energy." F193 makes the sharp claim that the homogeneous zero-point sum $\sum\tfrac12\hbar\omega$ is a non-gravitating *superimposable*. So: can the model reproduce a real Casimir force without that energy being physical, and is doing so consistent with F193? This finding computes the force in the **source/van der Waals channel** ($H_\text{int}$ = the F69 photon coupled to matter), settles the gravitation question, and evaluates the two model-specific predictions (Archimedes weighing, dynamical-Casimir pair emission).

The computation introduces **no new physics**: the photon (F69), its dispersion (F26), the cell scale (F107), and the beable gravity source (F178/F193) are all already derived.

## What was computed (6/6 PASS)

| # | Check | Method | Result | Tier |
|---|---|---|---|---|
| C1 | 1D mode-sum machinery | sum − bulk integral on a length-$L$ Dirichlet chain | `sin` scalar → $-\pi c/24L$ (rel $3.5\times10^{-5}$); model photon along a cubic axis is **exactly linear** → $E_\text{sub}=$ const $=c\pi/4$ (no Casimir term from a pure axial line) | quantitative + exact |
| C2 | 3D EM reproduction | Abel–Plana reduction of the mode sum with the **exact IR dispersion** $\Omega_\text{pair}\to c\lvert k\rvert$ (F69-PP3) | $F/A=-\pi^2\hbar c/240L^4$, $E/A=-\pi^2\hbar c/720L^3$ — **exactly**, in closed form ($c=1/\sqrt3$) | **exact-algebraic** |
| C3 | Lattice signature | bending coefficient $\beta(\hat k)$ of $\Omega_\text{pair}=c\lvert k\rvert(1+\beta\lvert k\rvert^2+\dots)$ | $\beta_\text{axis}\approx0$ (exact), $\beta_\text{face}\approx-3.4\times10^{-3}$, $\beta_\text{body}\approx-6.6\times10^{-3}$ → correction $\sim\beta\,(a/L)^2$ | directional structure exact; coeff $O((a/L)^2)$ |
| C4 | Source channel (Jaffe) | two $\delta$-mirrors of strength $\lambda$, massless scalar | $E$ runs monotonically $0\to$ Dirichlet as $\lambda:0\to\infty$ ($\lambda=10^{3}$ within $0.4\%$ of $-\pi c/24L$) → **no coupling, no force** | qualitative + limits |
| G1 | Does $E_C$ gravitate? | feed $E_C$ as beable $T^{00}$ into $\nabla^2\ln K=-8\pi T^{00}$ (F106/F178) | $\Delta m=E_C/c^2$ (Gauss-law closure, exact); **equals the SEP vacuum-buoyancy magnitude** → Archimedes **cannot discriminate** | exact + honest non-discrimination |
| D1 | Dynamical Casimir | parametric boundary drive $H=g(a^\dagger b^\dagger+ab)$, Fock evolution from vacuum | strict **pair emission** $n_a=n_b$ (residual $0$), $=\sinh^2(gt)$; two-mode-squeezed vacuum | exact pair correlation + $\sinh^2$ |

## The crux — reproduction is exact, and exactly in the source channel

**C2 (the headline).** The Casimir mode sum is **IR-dominated**: the Abel–Plana reduction of the perfect-plate mode sum collapses to
$$\frac{E}{A}=-\frac{c\,L}{6\pi^2}\int_0^\infty\frac{s^3}{e^{2Ls}-1}\,ds\times(\text{pol}),\qquad \int_0^\infty\frac{s^3}{e^{2Ls}-1}ds=\frac{\pi^4}{240L^4},$$
whose integrand peaks at $s\sim1/L\to0$. There the model photon's dispersion is **exactly** $\Omega_\text{pair}\to c\lvert k\rvert$ (gapless, isotropic, $c=1/\sqrt3$ — proven in F69-PP3), so the textbook result is recovered with no approximation:
$$\boxed{\ \frac{F}{A}=-\frac{\pi^2\hbar c}{240\,L^4},\qquad \frac{E}{A}=-\frac{\pi^2\hbar c}{720\,L^3}\ }$$
(scalar Dirichlet $-\pi^2\hbar c/1440L^3$; the EM photon is exactly $2\times$ because F69 is **non-birefringent** — both transverse polarisations ride the single rate $\Omega_\text{pair}$, so there is no TE/TM splitting to track). The numeric integral confirms the closed form to machine precision; the force coefficient matches to $<10^{-12}$.

**C2 lives entirely in $H_\text{int}$.** The force is the boundary-induced shift of the F69 photon field energy, and the boundary exists only because the plates impose it through the U(1) minimal coupling (F68 identity channel) of the photon to matter currents. C4 makes this operational with Jaffe's own $\delta$-mirror model: as the coupling $\lambda\to0$ the plates become transparent and the energy $\to0$; the force is purely a function of the matter coupling, never of a free-standing vacuum sum. This is exactly the Jaffe (2005) / Nikolić (2016) "source picture," and it is precisely what F193 needs — the model sits on the modern-consensus side, not the fringe.

**C1's directional curiosity.** Along a cubic axis $\Omega_\text{pair}(k\hat x)=\lvert k\rvert/\sqrt3$ is exactly linear (a triangle wave, no zone-edge smoothing), so a hard mode-sum of a *pure axial line* returns only a constant surface energy and no Casimir term — the universal $-\pi c/24L$ requires the dispersion bending that off-axis modes carry. The physical 3D force is recovered because the transverse-momentum integration samples exactly the IR isotropic regime where $\Omega_\text{pair}=c\lvert k\rvert$. (This also explains why the naive hard-BZ-cutoff 3D sum carries cutoff artifacts and is only reliable via Abel–Plana — matching Ishikawa et al.'s lesson that the lattice Casimir energy depends on which dispersion you put in.)

## Consistency with F193 — gravitating $\neq$ exerting a force

There is **no tension**. The homogeneous $\sum\tfrac12\hbar\omega$ is a non-gravitating superimposable (F193 A2/A4): it sources no dielectric and is the same inside and outside the cavity, so it neither gravitates nor exerts a net force. The Casimir force is the *boundary-induced shift* — a beable/$H_\text{int}$ effect (C2/C4). Both statements hold at once.

**G1 — what gravitates, and as what.** The Casimir energy $E_C$ is the van der Waals binding energy stored in the actual field+matter configuration. It is **beable**, so it gravitates. Feeding it as $T^{00}$ into the F106/F178 weak-field source $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$, the Gauss-law closure fixes the enclosed gravitating mass independent of how $E_C$ is distributed:
$$M_\text{grav}=\oint\frac{c^2}{8\pi G}\nabla\ln K\cdot d\mathbf A=\int\frac{T^{00}}{c^2}\,dV=\frac{E_C}{c^2}.$$
Since $E_C<0$, the cavity weighs **less** by $\lvert E_C\rvert/c^2$ — like nuclear binding energy reducing an atom's weight. For a $1\ \mathrm{cm^2}$, $10\ \mathrm{nm}$ cavity, $E_C\approx-4.3\times10^{-8}\ \mathrm J$, $\Delta m\approx-4.8\times10^{-25}\ \mathrm{kg}$ ($\Delta(\text{weight})\approx-4.7\times10^{-24}\ \mathrm N$).

**The honest Archimedes verdict.** Under the strong equivalence principle the vacuum-buoyancy picture (Calloni/Avino) gives the Archimedes force = weight of the Casimir energy $E_C/c^2$ — **the same number**. After the (universal) renormalisation of the absolute vacuum energy, the model's $\Delta m=E_C/c^2$ and the SEP-buoyancy prediction are **numerically degenerate**: Archimedes cannot discriminate them at leading order. The distinction is *interpretational* — the model carries no fine-tuned cosmological-constant baggage (F193) — not a measurable signal. We do **not** claim a "first lab gravity test"; the build brief's make-or-break question is answered in the negative, as computed.

## D1 — dynamical Casimir: pairs, but mind which pair

A parametric boundary drive at frequency $\Omega_d$ produces excitations strictly in **correlated pairs**: $[\,n_a-n_b,\;a^\dagger b^\dagger+ab\,]=0$, so from vacuum $n_a(t)=n_b(t)=\sinh^2(gt)$ exactly (residual $0$ in the Fock evolution) — the standard DCE two-mode-squeezed vacuum (Wilson et al. 2011). **Caveat against over-reading the literature's "resonance":** this is *not* the F69 pairing. F69's pair is the photon's *internal* structure (one photon = a bound pair of two Weyl quanta); the DCE pair is *two photons emitted together*. A DCE event in the model therefore produces two photons = four Weyl quanta in a doubly-paired structure. The two-mode-squeezing correlation is a genuine prediction; the "photon is a pair, DCE makes pairs" coincidence is suggestive but they are distinct pairings and are recorded as such.

## Verdict

The model reproduces the measured Casimir force **exactly** ($-\pi^2\hbar c/240L^4$, closed-form) from the F69 photon as a source/$H_\text{int}$ effect, fully consistent with F193: the force is beable, the homogeneous zero-point sum stays a non-gravitating superimposable. The Casimir energy gravitates as binding energy $\Delta m=E_C/c^2$, but this is **degenerate with SEP vacuum-buoyancy**, so Archimedes is not a model discriminator. The model-specific signatures are an $O((a/L)^2)$ lattice correction (zero for cubic-axis plates; $\sim10^{-56}$ for laboratory $L$ — a clean falsifier only in principle) and the doubly-paired DCE emission.

## What is exact vs computed vs honest-negative

| Piece | Status |
|---|---|
| $F/A=-\pi^2\hbar c/240L^4$, $E/A=-\pi^2\hbar c/720L^3$ from IR dispersion | **Exact-algebraic** (Abel–Plana closed form; force ratio $<10^{-12}$) |
| EM $=2\times$ scalar (non-birefringence) | **Exact** (F69 single-rate $\Omega_\text{pair}$) |
| 1D `sin` machinery $\to-\pi c/24L$ | **Computed** ($3.5\times10^{-5}$) |
| cubic-axis $\Omega_\text{pair}$ exactly linear $\Rightarrow$ zero correction there | **Exact** (triangle-wave dispersion) |
| $\Delta m=E_C/c^2$ (Gauss-law closure of $\nabla^2\ln K=-8\pi T^{00}$) | **Exact** |
| source channel: $E\to0$ as coupling $\to0$ | **Computed** (Jaffe $\delta$-mirror limits) |
| DCE strict pair correlation $n_a=n_b$ | **Exact** (commutator + Fock evolution, residual $0$) |
| Archimedes distinguishability from SEP buoyancy | **Honest negative** — degenerate at leading order, not a discriminator |
| $O((a/L)^2)$ lattice coefficient (full anisotropic value) | **Bounded / order-of-magnitude** ($\beta\sim10^{-2}$; UV-sensitive, unobservable) |

## Caveats (do not overclaim)

- The "Casimir energy gravitates as binding energy" result is now computed (G1), but its **Archimedes distinguishability is negative** — it is not a lab gravity test, contrary to the optimistic framing in the research note §2.
- The exact $O((a/L)^2)$ lattice coefficient is UV-sensitive (the naive hard-cutoff sum carries cutoff artifacts; Abel–Plana fixes only the IR-exact leading term). The correction is $\sim10^{-56}$ for laboratory $L$ — recorded as a falsifier in principle, not a measurement target.
- Real-material corrections (Drude/plasma, temperature, roughness, the graphene puzzle) are QED matter-modelling layered on the same $H_\text{int}$ and are **not** foundational tests; kept out of the core gate.
- D1's pair structure is the standard two-mode squeezing; the apparent "resonance" with F69's internal pairing is explicitly **not** claimed as identity.

## Open / next

- A full lattice dynamical-Casimir simulation on `ca_photon_pair` (moving boundary in real space) to exhibit the doubly-paired Weyl emission directly, rather than via the two-mode parametric proxy.
- Pin the anisotropic $O((a/L)^2)$ coefficient with a proper full-BZ lattice sum (academic; unobservable).

## Files
- Module: `ca-simulation/ca_casimir.py` (`casimir_energy_1d`, `casimir_energy_3d_abelplana`/`_closed`, `casimir_force_3d_abelplana`, `pair_bending_coeff`, `casimir_energy_delta_1d`, `casimir_gravitating_mass`, `dielectric_enclosed_mass_gauss`, `two_mode_squeezing`).
- Test: `tests/findings/test_F207_casimir.py` (6/6).
- Results: `test-results/F207_casimir.json`.
