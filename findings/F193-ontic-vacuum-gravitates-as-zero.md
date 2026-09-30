# F193 — The CA-native ontic vacuum gravitates as **exactly zero**: candidate (i) of F164 turned from a position into a derivation (bare CC = 0, fixing magnitude **and** sign), with the residual $\rho_\Lambda$ as a holographic IR back-reaction (reproduced to 0.54 dex; the dilution exponent is the named obstruction)

> **[PARTIALLY SUPERSEDED 2026-09-27 by F319, F408 — ledger S25-F193-partA-excluded-and-secB-sign-reading]**
>
> **DEAD:** PART A in full (A1-A4, 'bare CC = 0 in the ontology', removing magnitude and sign) -- excluded, CL275. SECTION B read as 'the observed rho_Lambda is the IR-diluted zero-point energy', its 0.54 dex agreement (a g* content mismatch), and the line-88 sentence that the vacuum sign is settled by F192's w=-1 argument. 'F193 section B + F196 is one route' (K9, G1, CL021) is withdrawn with it.
>
> **STILL LIVE:** Section B's STRUCTURAL observation that |a0| a^2 and a1 are the same kind of object (hbar c / a^2), which F408 S2 sharpens to the exact ratio 24 sqrt3 pi. The named p=2 obstruction as history (closed by F196). Section E's DE/DM remark stays speculative/open as before.
>
> **NOTE:** Cite F408 for the sign of the surviving route and F319/CL275 for Part A. The live K9/G1 statement is F408 section 7: a0 removal (sign-blind; F367 sequestering, contingent) + the positive a1 horizon term (the scale, not a source) + Omega_Lambda.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*

**Date:** 2026-06-30 - 17:35
**Numbering:** **F193** (re-checked; prior max F192).
**Status:** **Materially advances candidate (i).** Part A is a *derivation*: the model's own gravity sector (F64/F178) is sourced by the **beable** field-energy density, which on the ontic vacuum (empty BCC lattice) is **identically zero** — so the bare lattice cosmological constant is $0$ in the ontology, removing both the F164 magnitude and its wrong sign. Part B is *computed + honest*: the observed small $\rho_\Lambda$ is the back-reaction of the actual non-vacuum content, and a single factor of $(a/R_H)^2$ (holographic / Cohen–Kaplan–Nelson IR regulation, which the model's own black-hole sector implies) reproduces $\rho_\Lambda$ to within a factor $3.4$ ($\Delta\log_{10}=0.54$). The dilution **exponent** (why $2$, why $R_H$) is not derived — that is the sharpened, named obstruction. 4/4 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F193_ontic_vacuum.py` (self-contained, real arithmetic; mirrors `gr_fork_F164_*`).
**Tests / results:** `tests/findings/test_F193_ontic_vacuum.py` → `test-results/F193_ontic_vacuum_test.json` (4/4); fork dump `test-results/F193_ontic_vacuum.json`.
**Cross-references:** [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the $\Lambda^4$ overshoot and the four candidate channels — this finding closes (i)), [[F192-vacuum-energy-full-tensor]] (the $w=-1$ sign, built on here), [[F64-em-connection-gravity]] (the dielectric sourced by enclosed mass — the load-bearing commitment), [[F178-gravity-full-tensor-adoption]] (the full-tensor source), [[F69-paired-spinor-photon]] (marginal binding → no bosonic tower), [[F191-dark-matter-rotation-curves-bullet]] (the DM tie-in, §E). External: `t-hooft-2015-cai-summary.md` §3.1 (beable/changeable/superimposable); Cohen–Kaplan–Nelson 1999 (holographic UV–IR bound).

---

## The question F164 left open

F164 made the model's cosmological-constant problem quantitative: the bare template zero-point density at the F107 canonical cell is $\rho_\text{vac}=g_*\sqrt3\,I_\text{CC}\,\hbar c/a^4\approx3.46\times10^{111}\ \mathrm{J/m^3}$, overshooting the observed $\rho_\Lambda\approx6\times10^{-10}\ \mathrm{J/m^3}$ by $\log_{10}=120.76$, with the **wrong sign** (all-fermion vacuum). It named candidate (i) — the CA-native trivial ('t Hooft) vacuum — as the elegant-design-preferred lead but recorded it as *a position, not a calculation*: "show that the CA Hamiltonian's ontic ground state carries zero gravitating energy in the F64 dielectric, and that the leading non-vacuum back-reaction lands near $\rho_\Lambda$." This finding does the first part as a derivation and the second as a computed, honestly-bounded estimate.

## Part A — the ontic vacuum gravitates as exactly zero (derivation)

The argument has four steps; the load-bearing one (A3) is a commitment the model's gravity sector **already** makes, so this is a consistency derivation, not new physics.

**A1 — The ontic ground state is the empty BCC lattice $\psi(\mathbf x)\equiv0$.** In a deterministic, unitary CA the vacuum is a single ontological configuration, not a Fock state. The one-step update $U$ is linear and homogeneous, so $U\,0=0$ and the CA energy eigenvalue is $H\,0 = (\hbar/\tau)(-i\log U)\,0 = 0$ **exactly** (residual $0$, structural — not a cancelled sum).

**A2 — The local field-energy density is a *beable*.** It is a diagonal, real, non-negative functional of the **actual** per-cell amplitudes, $e(\mathbf x)=(\hbar/\tau)\,|\psi(\mathbf x)|^2\times(\text{rotation weight})$ — quadratic in the field with **no additive $c$-number** per mode. The $+\tfrac12$-per-mode offset of canonical quantisation is the off-diagonal / normal-ordering piece that lives only in the template (Fock) description. Evaluated on the ontic vacuum $\psi\equiv0$, $e(\mathbf x)\equiv0$ identically:
$$T^{00}_\text{ontic-vac}=0\quad\text{(structural zero, residual }0.0).$$

**A3 — The F64 dielectric is sourced by the *enclosed beable mass*, not by $\langle T^{00}\rangle$.** This is how F64/F178 are actually built: $K=\exp(2GM/rc^2)$ with $M$ the **actual** enclosed mass-energy, and the full-tensor law $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ with $T_{\mu\nu}$ the stress tensor of the **actual** field configuration. On the ontic vacuum $M=T^{00}_\text{ontic-vac}/c^2=0$, so $K=1$ and $G_{\mu\nu}=0$: the empty ontic vacuum **does not curve the lattice**. (Residual $0.0$; the dielectric is flat for any $r$.)

**A4 — Therefore the bare CC is $0$ in the ontology.** The F164 $\rho_\text{vac}=3.46\times10^{111}\ \mathrm{J/m^3}$ is $\sum\tfrac12\hbar\omega = \langle0|\,(\text{off-diagonal part of }{:}\hat\phi^2{:})\,|0\rangle$ — the expectation of a **superimposable** in a template state. Superimposables are not diagonal in the beable basis and **do not source the F64 dielectric**. The quantity that gravitates is the beable $T^{00}$, which is $0$ on the vacuum. This **removes the magnitude *and* the sign**: there is no $-\tfrac12\sum\hbar\omega$ negative tower among the beables to begin with, so the F164 sign problem (Part B of F164) does not arise in the ontology — it was an artefact of pricing the template description.

> **Load-bearing assumption (stated plainly):** gravity couples to the *beable* (actual-configuration) energy density, not to the template expectation value $\langle T^{00}\rangle$ that includes zero-point fluctuations. This is **not** an extra postulate — it is exactly the commitment F64 already makes when it writes $K=\exp(2GM/rc^2)$ with $M=$ enclosed mass. F193's content is recognising that *applying that same rule to the vacuum forces the bare CC to zero.* If one instead insisted the semiclassical source is $\langle T^{00}\rangle$ with un-normal-ordered zero-point pieces, F164's overshoot returns; the model's own gravity construction does not do that.

This is candidate (i) of F164 §C turned from a position into a derivation: *the bare cosmological constant of the BCC Weyl QCA is exactly zero, because the gravitating source is a beable and the ontic vacuum carries zero beable energy.*

## Part B — the residual $\rho_\Lambda$ as a holographic IR back-reaction (computed; obstruction named)

With the bare term gone, the observed $\rho_\Lambda$ is **not** a $121$-order cancellation residual but the back-reaction of the **actual non-vacuum content** of the universe — a separately small, in-principle-computable quantity (F164's framing, now the only term left).

**B1 — Small parameter.** The gravitating vacuum energy is the excitation density *above* the empty state. Its ratio to the bare template density is the **mean lattice excitation fraction**
$$f \equiv \frac{\rho_\Lambda}{\rho_\text{vac}} = 1.74\times10^{-121}.$$
The universe is, to $121$ decimal places, the empty lattice; that near-emptiness *is* the smallness of the CC.

**B2 — One factor of $(a/R_H)^2$ supplies the $121$ orders.** Cohen–Kaplan–Nelson IR regulation — a region of size $L$ cannot pack more field energy than collapses it into a black hole of size $L$, a bound the model's **own** black-hole sector (F114/F178) makes — caps the gravitating density at the IR (Hubble/causal) scale $R_H=c/H_0$:
$$\rho_\text{grav}\ \sim\ \rho_\text{vac}\left(\frac{a}{R_H}\right)^2 .$$
Numerically, with $a=1.066\times10^{-34}\ \mathrm m$ (F107) and $R_H=1.381\times10^{26}\ \mathrm m$ ($H_0=67$ km/s/Mpc):

| quantity | value |
|---|---|
| $R_H/a$ | $1.295\times10^{60}$ |
| $(a/R_H)^2$ | $5.97\times10^{-121}$ |
| $\rho_\text{vac}\,(a/R_H)^2$ | $2.06\times10^{-9}\ \mathrm{J/m^3}$ |
| observed $\rho_\Lambda$ | $6.0\times10^{-10}\ \mathrm{J/m^3}$ |
| ratio (holographic / observed) | $3.44\ \ (\Delta\log_{10}=0.54)$ |
| cross-check $\rho_\text{CKN}=c^4/(8\pi G R_H^2)$ | $2.53\times10^{-10}\ \mathrm{J/m^3}$ ($0.42\times$ observed, $-0.37$ dex) |

The entire $120.76$-decade overshoot of F164 is reproduced — to within a factor of $\sim3$ — by **one** power of $(\text{UV cell}/\text{IR horizon})^2$. The leftover $O(1)$ is absorbable in the choice of IR scale (Hubble radius vs future event horizon vs particle horizon), the CKN coefficient, and $g_*/I_\text{CC}$.

**B3 — The obstruction, now named precisely.** What is *not* derived is the **dilution exponent**: why the gravitating density is $\rho_\text{vac}\,(a/R_H)^{\,p}$ with $p=2$ rather than $p=4$ (which would give zero effect's opposite — a far smaller number) or $p=0$ (the bare overshoot). $p=2$ is the holographic/CKN value, motivated by the model's black-hole sector but **imported, not derived from the CA dynamics**. Closing F193 fully = deriving $p=2$ and the IR scale $=R_H$ from the lattice's own coarse-graining (a block-spin / F130-style RG statement of how far the excitation back-reaction propagates). That is the single remaining unknown, reduced from "$121$ orders and a sign" to "one integer exponent."

## What is derived vs computed vs posited

| Piece | Status |
|---|---|
| ontic vacuum = empty lattice; $H\,0=0$ | **Derived** (linear homogeneous $U$; exact) |
| beable $T^{00}_\text{ontic-vac}=0$ identically | **Derived** (structural zero, residual $0.0$) |
| F64 dielectric flat on vacuum ($K=1$, $G_{\mu\nu}=0$) | **Derived** from F64's own enclosed-mass source |
| bare CC $=0$ in the ontology (magnitude **and** sign removed) | **Derived**, conditional on the (already-made) beable-source assumption |
| $+\tfrac12\hbar\omega$ template sum $=$ F164 number, a superimposable | **Computed** (reproduces $\rho_\text{vac}=3.46\times10^{111}$) |
| residual $\rho_\Lambda$ = back-reaction of actual content; $f=1.7\times10^{-121}$ | **Computed** (definitional, given Part A) |
| $\rho_\text{vac}(a/R_H)^2$ within $0.54$ dex of $\rho_\Lambda$ | **Computed coincidence** (factor $3.4$) |
| dilution exponent $p=2$, IR scale $=R_H$ | **Posited / imported** (CKN) — the named obstruction |

## Candidate (ii) — a brief note (not the focus)

The dielectric-sequestering route (F164 §C-ii) is *subsumed* by Part A in the relevant limit: a spatially constant $T^{00}_\text{vac}$ has **no normalisable static-dielectric solution** ($\nabla^2\ln K=-8\pi\rho_\text{const}$ grows like $r^2$), i.e. the constant mode does not source the *local* weak-field dielectric at all — it only enters the homogeneous Friedmann mode (F182/F188/F192). This is "sequestering" in spirit but is really "the static dielectric is blind to the homogeneous piece"; it does not by itself fix the magnitude. Part A is the cleaner statement: the homogeneous piece is zero in the ontology to begin with.

## E — Dark-energy / dark-matter tie-in (speculative; recorded as open, not a claim)

F191 needs a dark **source** (Bullet-Cluster offset rules out pure dielectric reweighting). F193 sharpens what a unified dark sector would require: a component whose **beable** energy density is (i) essentially zero on the cosmic mean — so it reads as $w\approx-1$ smooth dark energy at the holographic residual scale (Part B) — yet (ii) **clusters** where actual excitation content is present, sourcing $K$ on galactic scales (F191). The model-native candidate is the back-reaction excitation field itself: a gravitating-yet-near-empty condensate (F93 $E_g$ second-neighbour channel, or the F69 marginal-binding channel). Whether *one* field can be both $w\simeq-1$ on large scales and clustering on galactic scales is **not** established here; it is the make-or-break test flagged in F191/F192. Recorded as **open / next**, not as a result.

## Caveats

- Part A's zero is conditional on the beable-source reading of F64; that reading is the one F64/F178 already use, but it *is* a physical commitment and is stated as such.
- Part B's $(a/R_H)^2$ is a coincidence to $0.54$ dex, not a derivation; the exponent is imported from CKN. A different IR scale (event horizon $\sim1.07\,R_H$, or $R_H$ at last scattering) shifts the $O(1)$ but not the exponent.
- $g_*=2$, $H_0=67$, $\Omega_\Lambda=0.69$ as in F164; few-percent cosmological shifts move $\log_{10}$ by $\ll1$.
- The DM/DE unification (§E) is speculative and explicitly not claimed.

## Relation to other findings

Closes candidate (i) of **F164** (the leading channel) and explains *why* the **F164** sign problem and the **F192** sign result are not in tension: there is no negative beable tower, so the only sign that matters is the $w=-1$ Friedmann sign F192 already fixed. Uses **F64/F178**'s enclosed-mass dielectric as the load-bearing source, **F107**'s canonical cell for the absolute scale, **F69**'s marginal binding (no bosonic tower) and the all-fermion structure (F67–F69) — now harmless, because no tower gravitates. The DM tie-in (§E) feeds **F191**. Leaves the hierarchy/scale gap (**F119**) untouched; F193 addresses only the vacuum/$\Lambda^4$ sector.
