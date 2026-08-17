# F300 — G10: lattice-native thermodynamics — the radiation equation of state is a *theorem* of the derived dispersion, entropy rises only under coarse-graining, and the free sector reaches a GGE rather than a Gibbs state

**Date:** 2026-08-06 - 10:05
**Status:** **Confirmed — 15/15 PASS**, two declared controls verified red. Rubric row **G10** moves `ABSENT → PARTIAL` — the last of the seven `ABSENT` rows the 2026-08-04 completeness report opened with. Four legs are algebraically exact (closed-form dispersion expansion, $\langle A\rangle=1/315$, the three EoS coefficients, the $15/2$ ratio), four are machine-precision (unitarity, conserved charges), three are quantitative (GGE approach, time reversal, capacity), and one is an exact **no-go** against F190's own named next step.
**Module:** `src/casim/engine/interactions/thermodynamics.py`
**Test record:** `F300-lattice-thermodynamics` (gate tier)
**Results:** `test-results/F300_lattice_thermodynamics.json`
**Claim cards:** `docs/claims/CL260-lattice-radiation-eos.md`, `docs/claims/CL261-cell-entropy-not-a-state-count.md`

**Cross-references:** [[F26-speed-of-light-as-rotation-rate]] (the walk and $c_\text{lat}=1/\sqrt3$), [[F67-even-law-photon-vs-bilinear-mutually-exclusive]] / [[F68-minimal-coupling-forces-even-photon]] / [[F69-paired-spinor-photon]] (the dispersion every integral here runs over), [[F107-canonical-a-adoption-L4-grb-gate]] and [[F79-structural-newton-constant]] (the ruler that sets the one temperature scale), [[F297-bbn-light-element-abundances]] (**the input this finding grades**), [[F182-friedmann-pressure-cosmology]] and [[F288-structure-formation-zero-free-functions]] (the cosmology that assumed $w=1/3$), [[F190-horizon-entropy-lattice-microstates]] and [[F183-blackhole-under-full-tensor]] (§5, rubric E9), [[F212-dynamical-entanglement-generation]] / [[F217-field-native-fermion-entanglement]] (the entropy machinery this reuses), [[F110-realtime-link-hamiltonian-confinement]] (the interacting sector §4 hands off to), [[F129-blockspin-free-photon]] / [[F130-blockspin-rg-gauge-gravity]] (coarse-graining), [[F281-measurement-pointer-basis-born-rule-rg-classicality]] (A8, the adjacent row), [[F47-majorana-seesaw-higgs-free]] / [[F279-hypercharge-constraint-attribution]] (the 48-Weyl content used in §5).

---

## 1. What was absent, and what this replaces

G10 read:

> Temperature enters cosmology and superconductivity as an external parameter;
> no lattice-native thermodynamics. 18 findings mention entropy, all of it
> black-hole or information entropy.

Both halves were true. The report's own Amendment 4 then argued the remaining rows should be read as **assembly** problems, and that assembling an absent sector is itself a review instrument, "because it forces every input through an observation that had never been applied to it." That is the right frame here, and it produces the sharpest result in the finding:

> **F297's thermal history — three hours older than this session's claim — assumed the continuum $\rho=(\pi^2/30)g_*T^4$ and $p=\rho/3$. Nothing in the tree had ever checked that the lattice supplies them.** §3 checks it, in closed form, and quantifies the margin.

No new physics is introduced. Every ingredient is a quantity the tree already derived, and the parameter count is **zero**.

---

## 2. Temperature, defined rather than imported

The partition function is built on the model's own object, not on a continuum ansatz. For the paired-spinor photon (F69) the rotation rate per tick is

$$\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2),\qquad \omega^\pm=\arccos u^\pm,$$

so the grand potential is a Brillouin-zone integral of **that** function and no other. Temperature enters as the single dimensionless ratio

$$\Theta \equiv \frac{k_BT\,\tau}{\hbar},\qquad \tau=\frac{a}{\sqrt3\,c},\qquad a=6.5978\,\ell_P\ \text{(F107)},$$

i.e. $T$ measured against the one scale the lattice has. $\Theta=1$ at

$$T_\text{lat}=\hbar/(k_B\tau)=\mathbf{3.719\times10^{31}\ K}\qquad(\tau=2.054\times10^{-43}\ \text{s},\ \hbar/\tau=3.205\times10^{18}\ \text{GeV}).$$

$k_B$ is a *ruler for temperature*, exact by SI definition; it is the only new external constant and it carries no physics. (It is not yet a D7 registry symbol — see §7.)

### 2.1 The dispersion in closed form (exact)

Expanding $\Omega_\text{pair}$ to third order gives, with $\hat n=\mathbf k/|\mathbf k|$,

$$\boxed{\ \Omega_\text{pair}(\mathbf k)=c_\text{lat}|\mathbf k|\Bigl[1-A(\hat n)\,|\mathbf k|^2\Bigr]+O(|\mathbf k|^5),\qquad A(\hat n)=\frac{1}{72}\sum_{i<j}\hat n_i^2\hat n_j^2+\frac{1}{24}\bigl(\hat n_x\hat n_y\hat n_z\bigr)^2\ }$$

Two structural facts fall out, and both are checks:

* **$A$ vanishes identically along $\langle100\rangle$.** Along a cubic axis $u^\pm=\cos(k/2\sqrt3)$ exactly, so $\Omega_\text{pair}=c_\text{lat}k$ **at every $|\mathbf k|$**, not merely asymptotically — verified to $6.0\times10^{-14}$ out to $|\mathbf k|=3$ (G10-2). The paired photon has an exactly linear direction.
* **The branch-odd term cancels in the $(+,-)$ sum.** That cancellation *is* F67/F68's non-birefringence, seen from the thermodynamic side: a single-branch photon would carry an $O(|\mathbf k|)$ relative splitting, and the pair carries none.

The angular average is exact:

$$\langle A\rangle=\tfrac{1}{72}\cdot\tfrac{3}{15}+\tfrac{1}{24}\cdot\tfrac{1}{105}=\tfrac{1}{360}+\tfrac{1}{2520}=\boxed{\tfrac{1}{315}}$$

confirmed by quadrature to $7.8\times10^{-15}$ (G10-3a).

---

## 3. The equation of state — closed form, then measured

Pressure is the **momentum-flux** definition, $p=\frac{1}{3V}\sum_\mathbf{k}n_B\,(\mathbf k\!\cdot\!\nabla_\mathbf{k}\Omega)$ — the one that enters $T^{ij}$ and therefore the Einstein equation. On a rigid substrate $-\partial F/\partial V$ is not available: the substrate's volume is not a thermodynamic variable. At leading order $\Omega$ is homogeneous of degree 1, so Euler's theorem gives $\mathbf k\!\cdot\!\nabla\Omega=\Omega$ and $w=1/3$ **exactly** — the continuum radiation EoS is a theorem, not an assumption.

With the two Bose integrals $\int_0^\infty x^3/(e^x-1)=\pi^4/15$ and $\int_0^\infty x^5/(e^x-1)=8\pi^6/63$, the leading lattice corrections are pure numbers times $\Theta^2$:

| Quantity | Closed form | Measured (BZ quadrature) | rel. |
|---|---|---|---|
| $u/u_\text{SB}-1$ | $\dfrac{40\pi^2}{441}\Theta^2=0.8952022\,\Theta^2$ | $0.8955933\,\Theta^2$ | $4.4\times10^{-4}$ |
| $\tfrac13-w$ | $\dfrac{16\pi^2}{1323}\Theta^2=0.1193603\,\Theta^2$ | $0.1194204\,\Theta^2$ | $5.0\times10^{-4}$ |
| $s/s_\text{SB}-1$ | $\dfrac{4\pi^2}{49}\Theta^2=0.8056820\,\Theta^2$ | $0.8060174\,\Theta^2$ | $4.2\times10^{-4}$ |
| $C_u/C_w$ | $\mathbf{15/2}$, parameter-free | $7.499498$ | $6.7\times10^{-5}$ |

The residual is **not** numerical error: it scales as $\Theta^2$ across the fit window ($1.3\times10^{-5}$ at $\Theta=0.002$, $1.3\times10^{-3}$ at $\Theta=0.02$, a clean factor $10^2$ for a factor 10 in $\Theta$), i.e. it is the next term in the series. The sign is physical: a softer band puts more modes below any given energy, so $u$ rises and $w$ falls — **lattice radiation is softer than continuum radiation**, never stiffer.

**Boundary control (G10-6b).** The result does not depend on the shape of the paired photon's Brillouin zone, which this finding deliberately does not settle. In the $\Theta\ll1$ regime the occupation at the zone edge is exponentially small, so the radial cut decouples: moving it over $x_\text{max}=45\to75$ (in units of $\Theta/c$) moves $u/u_\text{SB}-1$ by $3.7\times10^{-9}$ relative. The cut is set by the **Bose tail**, not by the zone. Cutting at $x_\text{max}=30$ is *not* converged ($1.9\times10^{-5}$), and that is the honest boundary of the regime.

### 3.1 What this is worth where the tree actually uses it

| Epoch | $\Theta$ | $u/u_\text{SB}-1$ | $\tfrac13-w$ |
|---|---|---|---|
| CMB, 2.7255 K | $7.3\times10^{-32}$ | $4.8\times10^{-63}$ | $6.4\times10^{-64}$ |
| BBN, $T_9=1$ | $2.7\times10^{-23}$ | $6.5\times10^{-46}$ | $8.6\times10^{-47}$ |
| BBN, 1 MeV | $3.1\times10^{-22}$ | $8.7\times10^{-44}$ | $1.2\times10^{-44}$ |
| QCD crossover, $1.7\times10^{12}$ K | $4.6\times10^{-20}$ | $1.9\times10^{-39}$ | $2.5\times10^{-40}$ |
| Electroweak, $1.6\times10^{15}$ K | $4.3\times10^{-17}$ | $1.7\times10^{-33}$ | $2.2\times10^{-34}$ |

**F297's continuum assumption is safe by 44 orders of magnitude at the BBN bottleneck.** The model's radiation EoS is $w=1/3$ to better than 1% for every temperature below $6.2\times10^{30}$ K. That is a *derived margin* replacing an unexamined assumption, and it is the answer to the report's question of what an assembled sector says about its own inputs: in this case, that the input was fine — which is a result, not a null, because until today nobody could have said so.

**Falsifier.** Any observation of a Planck-spectrum distortion of *lattice-discreteness* type — $\delta I_\nu/I_\nu\propto(\nu\tau)^2$ with the derived coefficient — at $\nu$ far below $1/\tau$ kills the F107 ruler, since the coefficient is fixed once $a$ is. FIRAS-class sensitivity ($10^{-5}$) corresponds to $\Theta\approx3.3\times10^{-3}$, i.e. $T\approx1.2\times10^{29}$ K: **the prediction is unobservable, and saying so is the point** — a falsifier that cannot fire must be labelled, not published (completeness gap #2).

---

## 4. The second law, and what does not happen

The walk is quadratic, so the many-body state is Gaussian and is carried **exactly** by the one-particle correlation matrix — no truncation, no Trotter error, exact evolution of a $2L^3$-mode Fock space. $L=8$: 1024 modes.

| # | Statement | Measured |
|---|---|---|
| G10-7 | Fine-grained von Neumann entropy is conserved by the model's own walk. Measured on a **mixed** state ($S_0=591.27$ nats), so this is not the trivial $S=0$ of a pure state | drift $\le1.1\times10^{-12}$ over $t=1,17,101$ |
| G10-8 | The branch occupations $n_\pm(\mathbf k)$ are **exactly** conserved — $2N$ conserved charges | $\le5.4\times10^{-14}$ |
| G10-9 | Coarse-grained entropy rises from zero to a plateau | $S_A(0)=4.3\times10^{-11}$; plateau $79.96\pm0.46$ nats at subsystem fraction $1/8$ |
| G10-11 | **Time reversal**: $S_A(-t)$ rises exactly as $S_A(+t)$ does | $79.943$ vs $79.957$, $1.8\times10^{-4}$ relative |

G10-11 is the honest lattice-native statement of the second law, and it is worth stating plainly rather than burying: **the arrow of time is not in the dynamics.** It is in the initial condition together with the choice of coarse-graining. Entropy grows toward the past exactly as it grows toward the future. Any later claim in this tree that the CA "derives" the second law must mean this and nothing stronger.

**Control (declared, verified red).** Inserting a mode decimation into the propagator — a non-invertible coarse-graining — turns G10-7 red along with G10-9 and G10-10. Fine-grained entropy is conserved by unitarity and by nothing else; the check can fail, and it does.

### 4.1 The free sector cannot thermalise (a bounded negative result)

G10-8 is not a curiosity — it is a **no-go**. $2N$ conserved charges mean the stationary ensemble is a generalised Gibbs ensemble fixed by the initial $n_\pm(\mathbf k)$, not a Gibbs state at any temperature. Measured, the coarse-grained plateau approaches the GGE prediction as the subsystem shrinks — which is exactly the sense in which a GGE is ever true:

| subsystem fraction | modes | plateau | GGE | ratio |
|---|---|---|---|---|
| $1/2$ | 512 | 196.56 | 354.88 | 0.5539 |
| $1/8$ | 128 | 79.96 | 88.72 | 0.9012 |
| $1/64$ | 16 | 10.95 | 11.09 | 0.9872 |
| $1/512$ | 2 | 1.3832 | 1.3862 | 0.9978 |

So: **local observables equilibrate; the system does not thermalise.** Getting a Gibbs state requires breaking the $2N$ charges, i.e. interactions — and the tree already has the instrument, F110's real-time link Hamiltonian, whose deferred SU($N$) ladder F294 independently named as its next step. That is the named next step here too, and it is the same one.

This also bounds what §3 claims: the equation of state is an *equilibrium* statement about the Gibbs measure on the derived dispersion. This finding does **not** show the lattice dynamically reaches that measure. Those are two different claims and only the first is made.

---

## 5. The cell constant: F190's open step is impossible as written (rubric E9)

F190 posits $s_\text{cell}=2\pi\sqrt3=10.8828$ nats and names its open step verbatim: *"show a boundary cell carries $e^{2\pi\sqrt3}$ states from the BCC/Weyl content."* Two things follow immediately, and neither had been said.

**D1 — an exact no-go (G10-12).** A dimension count of any finite Hilbert space is $\ln W$ with $W$ a positive integer; a count of binary modes is $n\ln2$ with $n$ an integer. Neither is available:

$$e^{2\pi\sqrt3}=53252.295\ \ (\text{distance to the nearest integer } 0.295),\qquad \frac{2\pi\sqrt3}{\ln2}=15.7006\ \ (0.299).$$

The nearest integer mode count, $n=16$ — tempting, since the model has 16 Weyl fields per generation — gives $16\ln2=11.0904$ nats and **overshoots by 1.91%**. So the step cannot be discharged as written, whatever the BCC/Weyl content turns out to be. The object F190 needs is an **entanglement** entropy, whose spectrum is continuous and carries no integrality constraint — and §4 is precisely the machinery that computes one.

**D2 — a necessary condition, passed (G10-13).** Counting can still answer whether the lattice has *room*. The model's fermionic content is 48 Weyl fields (3 generations × 16 including $\nu_R$; F47/F279), each two-component, so 96 fermionic modes per site: capacity $96\ln2=66.542$ nats against a requirement of 10.883. **Capacity exceeds requirement by $6.11\times$**; the horizon would use 16.4% of it. F190 is therefore not excluded by room — it is *under-determined* by it, which is a more useful statement than "open", because it says what the missing ingredient is: the **constraint** that selects $2\pi\sqrt3$, not the count that permits it.

Net effect on E9: the grade does not move, and this finding should not be read as moving it. What moves is the target — from "count the microstates" (now proved impossible) to "compute the boundary entanglement entropy under the constraint" (now the only surviving route, with the machinery in hand).

**A flagged coincidence, deliberately not claimed.** In the same lattice units the BCC reciprocal (fcc) conventional cube side is $4\pi/(2/\sqrt3)=2\pi\sqrt3$ — numerically identical to F190's per-cell entropy in nats. Both trace to $a^2=8\pi\sqrt3\,\ell_P^2$, but one is a reciprocal length and the other is an entropy, and **no derivation connects them**. Recorded in `reciprocal_cube_coincidence()` so a later session finds it already noticed and already not claimed (D7's `kind="coincidence"` discipline).

---

## 6. Checks

| # | Check | Result | Class |
|---|---|---|---|
| G10-1 | closed-form $A(\hat n)$ reproduces `pair_dispersion`, residual $O(k^4)$ | $4.4\times10^{-5}$ | exact form / machine |
| G10-2 | $\Omega_\text{pair}$ exactly linear along $\langle100\rangle$ at all $\lvert k\rvert$ | $6.0\times10^{-14}$ | machine |
| G10-3a | $\langle A\rangle=1/315$ | $7.8\times10^{-15}$ | exact |
| G10-3 | $u/u_\text{SB}-1=(40\pi^2/441)\Theta^2$ | $4.4\times10^{-4}$ | exact vs quadrature |
| G10-4 | $\tfrac13-w=(16\pi^2/1323)\Theta^2$ | $5.0\times10^{-4}$ | exact vs quadrature |
| G10-5 | $s/s_\text{SB}-1=(4\pi^2/49)\Theta^2$ | $4.2\times10^{-4}$ | exact vs quadrature |
| G10-6 | $C_u/C_w=15/2$ parameter-free | $6.7\times10^{-5}$ | exact |
| G10-6b | EoS independent of the radial cut | $3.7\times10^{-9}$ | control |
| G10-7 | fine-grained entropy conserved (mixed state) | $1.1\times10^{-12}$ | machine |
| G10-8 | $n_\pm(\mathbf k)$ exactly conserved | $5.4\times10^{-14}$ | machine |
| G10-9 | coarse-grained entropy $0\to$ plateau | $4.3\times10^{-11}\to79.96$ | quantitative |
| G10-10 | plateau $\to$ GGE as fraction falls | $0.554/0.901/0.987/0.998$ | quantitative |
| G10-11 | $S_A(-t)\simeq S_A(+t)$ | $1.8\times10^{-4}$ | quantitative |
| G10-12 | $2\pi\sqrt3$ is neither $\ln(\text{integer})$ nor $n\ln2$ | $0.295$ / $0.299$ | exact no-go |
| G10-13 | per-site capacity $>2\pi\sqrt3$ | $6.11\times$ | quantitative |

**15/15 PASS.** Declared controls, both verified red: `linear_control=True` (dispersion replaced by exactly linear $c\lvert k\rvert$) turns **G10-3, G10-4, G10-5, G10-6** red and nothing else; `nonunitary_control=True` (mode decimation in the propagator) turns **G10-7, G10-9, G10-10** red.

---

## 7. Scope limits, and what is *not* claimed

1. **Equilibrium only.** §3 is the Gibbs measure on the derived dispersion. §4 shows the free sector does not reach it. Do not cite §3 as evidence that the lattice thermalises.
2. **Photon sector only.** The EoS is computed for the paired-spinor photon. A full $g_*(T)$ over the model's 48 Weyl fields needs the fermionic BZ sums with the branch-odd term handled; the machinery is here, the number is not.
3. **The zone shape is not settled.** §3 sidesteps it by measurement (G10-6b), which is legitimate in the $\Theta\ll1$ regime and nowhere else. The paired photon's Brillouin zone — its constituents carry $\mathbf k/2$ — is an open geometric question.
4. **$k_B$ is not in the D7 registry.** It is a module literal here, as it already is in `superconductivity.py`, `horizon_entropy.py`, `blackhole.py` and `qed_casimir_materials.py`. Registering it with all six sites is a clean mechanical follow-up and should be done as one edit, not silently folded into a physics session.
5. **E9 does not move.** §5 sharpens F190's target and kills one route; it derives nothing.
6. **$L=8$.** The §4 ratios are stable in $L$ (the $1/2$ and $1/8$ ratios differ by $<0.3\%$ between $L=6$ and $L=8$) but the statement is a finite-lattice measurement, not a thermodynamic-limit proof.

## 8. Next steps, in order of value

1. **$g_*(T)$ from the model's own content** — the fermionic BZ sums, closing the last continuum assumption in F297's thermal history and giving the cosmology block a derived $g_*$ instead of an SM count.
2. **Thermalisation on F110's link Hamiltonian** — the interacting sector, where Gibbs becomes reachable. Same deferred SU($N$) ladder F294 named; two rows now want it.
3. **Boundary entanglement entropy against $2\pi\sqrt3$** — the only surviving route to E9, using §4's correlation-matrix machinery on the F183 lattice core.
4. **Register $k_B$** (§7.4).
