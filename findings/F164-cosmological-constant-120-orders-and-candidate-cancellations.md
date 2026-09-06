# F164 — The cosmological constant: the model's $\Lambda^4$ vacuum integral made quantitative (a definite, finite $\approx10^{121}$ overshoot), and the candidate cancellation channels it admits

**Date:** 2026-06-29 - 16:20
**Status:** **Problem statement made quantitative + honest scope.** The bare lattice vacuum-energy density is *computed* (not estimated) at the F107 canonical cell: $\rho_\text{vac}\approx3.5\times10^{111}\ \mathrm{J/m^3}$, vs the observed $\rho_\Lambda\approx6\times10^{-10}\ \mathrm{J/m^3}$ — a ratio $\approx5.8\times10^{120}$ ($\log_{10}=120.8$). The model **inherits the standard cosmological-constant problem** and, because its UV cutoff is the *physical* Brillouin-zone edge (not a regulator), it inherits it as a **definite finite number with no regularisation freedom** — the problem is *sharpened*, not softened. Three candidate cancellation channels are identified and assessed; none is yet derived. This finding closes audit omission #10 (2026-06-29 physics audit) at the requested level: "identify the cancellation mechanism, or acknowledge the 120-order problem explicitly."
**Module:** `ca-simulation/forks/gr_fork_F164_cosmological_constant.py` (self-contained; mirrors the `ca_bcc` F26 dispersion, real arithmetic only).
**Tests / results:** `test-results/F164_cosmological_constant.json`.
**Test record:** record `F319-uv-completion` (tier gate) — leg `U8-reproduces-F164` asserts `abs(log10_overshoot − 120.76) < 0.02`, i.e. this finding's headline number, at gate tier; the same record excludes F164's own leading cancellation channel. It already named F164 on its side of the join. `F172-residual-algebraic-or-computed` also names F164. Declared 2026-08-19.
**Cross-references:** [[F59-induced-eh-prefactor-and-f10-selection]] (identifies the $\Lambda^4=\int\omega/2$ CC sector, distinct from the $\Lambda^2$ Newton sector — this finding evaluates it), [[F107-canonical-a-adoption-L4-grb-gate]] (the canonical cell $a$ used for the absolute scale), [[F64-em-connection-gravity]] (the dielectric that the vacuum energy would gravitate through), [[F119-kg-scale-three-routes]] (the related hierarchy/scale problem $N$), references `t-hooft-2015-cai-summary.md` (the CA-native vacuum argument).

## The question

F59 separated the two Sakharov sectors by their cutoff scaling: the Newton sector $1/G\propto\int d^3k/(2\omega)\sim\Lambda^2$, and the **cosmological-constant sector**

$$\rho_\text{vac}\ \sim\ \int_\text{BZ}\frac{d^3k}{(2\pi)^3}\,\frac{\omega(k)}{2}\ \sim\ \Lambda^4 .$$

F59 identified this integral but did not evaluate it or confront its magnitude. No finding had computed the model's cosmological constant or said where it sits relative to observation. This finding does both.

## Part A — the bare lattice vacuum energy is a *definite* number

The lattice has no continuum UV divergence: the momentum integral runs over the finite Brillouin zone, and the rotation angle per tick is bounded, $\omega=\arccos(u)\in[0,\pi]$. The zero-point energy density of the $g_*$ fundamental Weyl branches is therefore finite and computable:

$$\rho_\text{vac}=g_*\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\,\frac{1}{2}\,\frac{\hbar\,\omega(k)}{\tau}
= g_*\,\frac{\hbar}{\tau\,a^{3}}\,I_\text{CC}
= g_*\sqrt3\,I_\text{CC}\,\frac{\hbar c}{a^{4}},
\qquad
I_\text{CC}\equiv\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{\omega(k)}{2},$$

using $\tau=a/(c\sqrt3)$ (F107). The dimensionless integral over the BCC $+$-branch dispersion $\omega=\arccos(c_xc_yc_z+s_xs_ys_z)$ (variable $q=k/\sqrt3$, period cube $q\in[-\pi,\pi]^3$) evaluates to

$$I_\text{CC}=4.081,\qquad \langle\omega\rangle_\text{BZ}=\tfrac{\pi}{2}\ \text{(exact)} .$$

**The mean rotation angle is exactly a quarter turn.** This is an exact algebraic fact, not a numerical coincidence: under $q_x\to q_x+\pi$ the symbol flips sign, $u\to-u$ (machine-residual $2.2\times10^{-16}$), so $\omega(q)+\omega(q+\pi\hat x)=\arccos(u)+\arccos(-u)=\pi$; pairing the BZ with its $\pi$-shift gives $\langle\omega\rangle=\pi/2$ identically. The vacuum's average zero-point rotation is half its kinematic maximum.

## Part B — the number, and the 120-order problem in the model's own units

At the F107 canonical cell $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=1.066\times10^{-34}\ \mathrm m$, with the minimal $g_*=2$:

| quantity | value |
|---|---|
| bare lattice $\rho_\text{vac}$ | $3.46\times10^{111}\ \mathrm{J/m^3}$ |
| reference $\hbar c/a^4$ | $2.44\times10^{110}\ \mathrm{J/m^3}$ |
| observed $\rho_\Lambda=\Omega_\Lambda\rho_\text{crit}$ | $6.0\times10^{-10}\ \mathrm{J/m^3}$ |
| ratio $\rho_\text{vac}/\rho_\Lambda$ | $5.8\times10^{120}\ \ (\log_{10}=120.8)$ |
| $\rho_\text{vac}^{1/4}$ | $3.6\times10^{27}\ \mathrm{eV}$ |
| $\rho_\Lambda^{1/4}$ | $2.3\times10^{-3}\ \mathrm{eV}$ |
| energy-scale ratio $\big(\rho_\text{vac}/\rho_\Lambda\big)^{1/4}$ | $1.5\times10^{30}$ |

So the model reproduces the canonical statement of the cosmological-constant problem — a vacuum energy $\approx10^{121}$ times too large, equivalently a vacuum energy *scale* $\approx10^{30}$ too high (Planck-ish vs milli-eV). Two points make this the model's *own* statement rather than a borrowed slogan:

1. **No cutoff ambiguity.** In continuum QFT the $\Lambda^4$ is whatever you choose for the regulator; the "$120$ orders" is conventionally quoted against $M_\text{Pl}^4$. Here the cutoff is *physical* — the BZ edge $\lvert k\rvert\le\pi\sqrt3$ — so $\rho_\text{vac}$ is a definite prediction of the bare theory, $\approx10^{121}\rho_\Lambda$. The model **sharpens** the problem: there is nothing to renormalise away.

2. **The bare sign is fixed and *wrong*.** The model has **no fundamental bosons** — every gauge boson is composite (the paired-spinor photon F67–F69; the $\sigma$-bilinear W/Z/gluon). The only fundamental quanta are the Weyl branches, whose zero-point sum is $-\tfrac12\sum\hbar\omega$ — **negative**. The bare $\rho_\text{vac}$ above is a *magnitude*; its sign is $-1$, opposite the observed $+\rho_\Lambda$ of dark energy. There is therefore **no automatic SUSY-style boson/fermion cancellation available** (no independent bosonic $+\tfrac12\hbar\omega$ tower to cancel against), and the leading bare term has the wrong sign as well as the wrong size. Any viable resolution must both cancel $\sim121$ orders *and* flip the residual sign.

## Part C — candidate cancellation channels the model admits

Three mechanisms are consistent with the model's structure. None is derived here; each is stated with what it would take to close it.

**(i) CA-native trivial vacuum — the leading candidate (elegant-design preferred).**
The $\tfrac12\hbar\omega$ per mode is the *canonical-quantisation* prescription for a continuum field. The underlying object here is a **deterministic, unitary cellular automaton**, and its vacuum is a single ontological configuration: the empty lattice. Applying the rotation rule to the zero configuration rotates nothing and costs nothing, so the **CA ground-state energy is exactly zero by construction** — there is no zero-point motion of an ontic state. This is precisely 't Hooft's cellular-automaton-interpretation stance (`t-hooft-2015-cai-summary.md`, §9.2/9.4): zero-point energy is a property of the quantised continuum *description*, not of the discrete beable dynamics, and the project's automata are already "positive-Hamiltonian, unitary by design." On this reading the bare $\Lambda^4$ of Part B is a description artefact, the true bare CC is $0$, and the **observed** small $\rho_\Lambda$ is not a residual of a huge cancellation but the back-reaction of the actual (non-vacuum) field content — a separately small, in-principle-computable quantity. *To close:* show that the CA Hamiltonian's ontic ground state carries zero gravitating energy in the F64 dielectric, and that the leading non-vacuum back-reaction lands near $\rho_\Lambda$. This is the most model-consistent route (it makes the CC small *and* removes the sign problem, because there is no negative tower to begin with) but is currently a position, not a calculation.

**(ii) Sequestering through the F64 dielectric.**
Gravity in this model is a single impedance-matched dielectric renormalising the $(\mathbf E,\mathbf B)$ rotation rule (F64), with the reciprocal lock $AB\equiv1$. A constant vacuum energy couples to gravity only through this global dielectric. If the dielectric's overall normalisation is fixed by a global (cosmological) constraint rather than by the local vacuum density — the structure of "vacuum-energy sequestering" — the bare $\Lambda^4$ would not source curvature, leaving only fluctuations. *To close:* derive whether the $AB\equiv1$ lock plus a global volume constraint actually removes the constant piece of $T^{00}_\text{vac}$ from the rotation-rule renormalisation. Plausible given the dielectric's global character; not yet attempted.

**(iii) Marginal-binding cancellation of composite bosons.**
The physical photon binds at **exactly zero binding energy** (F69: $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$). A composite whose binding is exactly marginal contributes no vacuum energy beyond its constituents — which are already in the fermionic tower — so composites add nothing new. This *explains why there is no bosonic tower to double-count* (consistent with Part B's all-fermion sign) but on its own does **not** cancel the fermionic tower; it is a consistency statement, not a cancellation. Recorded for completeness and to forestall the mistaken hope that composite bosons supply a cancelling $+\tfrac12\hbar\omega$.

## What is derived vs what remains open

| Piece | Status |
|---|---|
| $I_\text{CC}=\int_\text{BZ}\omega/2=4.08$; $\langle\omega\rangle=\pi/2$ exact | **Derived** (algebraic pairing; residual $2.2\times10^{-16}$) |
| bare $\rho_\text{vac}=3.5\times10^{111}\ \mathrm{J/m^3}$ at canonical $a$ | **Computed** (definite, no cutoff freedom) |
| $\approx10^{121}$ overshoot vs observation | **Quantified** — the problem stated in model units |
| all-fermion vacuum $\Rightarrow$ bare sign negative, no SUSY cancellation | **Structural consequence** of F67–F69 (no fundamental bosons) |
| (i) CA-native zero vacuum ('t Hooft) | **Candidate** — leading; position not yet a calculation |
| (ii) dielectric sequestering | **Candidate** — needs F64 global-constraint derivation |
| (iii) marginal-binding | **Consistency only** — does not cancel the fermion tower |

## Caveats

- $g_*=2$ (minimal, two BCC Weyl branches) is used for the absolute number, as in F59; the full first-generation gravitating-mode count would scale $\rho_\text{vac}$ by an $O(10)$ factor — irrelevant to a $10^{121}$ statement, and it does not change the sign.
- $\rho_\Lambda=6\times10^{-10}\ \mathrm{J/m^3}$ uses $\Omega_\Lambda\approx0.69$, $H_0\approx67\ \mathrm{km/s/Mpc}$; a few-percent shift in cosmological parameters moves $\log_{10}$ by $\ll1$.
- The canonical-cell value of $a$ carries the F107 convention (one ruler, via $\ell_P$); a different $(a,\tau)$ resolution rescales $\rho_\text{vac}\propto a^{-4}$ but cannot bridge $121$ orders.
- Candidate (i) is favoured by the project's elegant-design philosophy *and* uniquely addresses the sign, but it reassigns the burden to computing the non-vacuum back-reaction — itself unproven to land near $\rho_\Lambda$. No claim is made that the small CC is yet explained; only that the model offers a structurally natural place for it to come from.

## Relation to other findings

Evaluates the $\Lambda^4$ sector that **F59** isolated and deliberately left open, using the **F107** canonical cell. The vacuum energy would gravitate through the **F64** dielectric (candidate ii). The all-fermion sign argument rests on the composite-boson findings **F67/F68/F69**. Sits beside **F119**'s hierarchy/scale no-go as the second "large-number" open problem; both point at the same gap — the model fixes ratios and structure cleanly but not the absolute matter/vacuum scale.
