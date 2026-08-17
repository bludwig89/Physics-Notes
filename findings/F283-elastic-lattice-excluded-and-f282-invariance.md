# F283 — An elastic lattice is excluded four ways, and it **cannot** rescue F282: because F79 ties $G$ to $a^2$, the ratio $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$ is **invariant** under any stretch $a\to sa$ ($\partial r/\partial s\equiv0$), so the inflation obstruction $r=\sqrt3=1/c_\text{lat}$ is a scale-free geometric property of the BCC lattice — this **corrects F282 falsifier #5**

**Date:** 2026-08-02 - 14:00
**Status:** **Structural no-go + a correction to F282.** 8/8 checks PASS. The invariance (E1) is **exact-algebraic** (sympy, symbols kept free so the cancellation is exhibited rather than asserted); the varying-$G$ and light-cone bounds (E2, E4) are **quantitative** against LLR/BBN/GW170817; the volume-mode dichotomy (E3) is **structural**, resting on F79/F180/F216.
**Module:** `src/casim/engine/interactions/cosmology_lattice_elasticity.py` (shared with F284)
**Registry record:** `F283-elastic-lattice-excluded` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F283_F284_lattice_elasticity.json`
**Corrects:** [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] §9 falsifier 5. F282 wrote *"a change to $a/\ell_P$ … if $a$ were $\gtrsim20\times$ smaller in Planck units the obstruction would evaporate."* **That is wrong**, and E1 proves it: $a$ cancels. F282's other four falsifiers stand, and its verdict is **strengthened** — the no-go is scale-free, so it cannot be dialled away at all.
**Cross-references:** [[F79-structural-newton-constant]] (the $G\propto a^2$ tie that makes E1 work, and the **zero tree stiffness** that makes E3 work), [[F107-canonical-a-adoption-L4-grb-gate]] (the canonical $a$ — now shown to be *irrelevant* to F282), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$), [[F180-gravitational-wave-speed]] ($c_\text{grav}=c_\text{lat}$ **derived** from the induced loop — E4 bounds what a tree term could add), [[F216-massive-spin2-dark-mode]] (exactly 2 propagating dof — the count E3's branch B would break), [[F178-gravity-full-tensor-adoption]] / [[F106-psi-K-sourcing-derivation]] ($\ln K$ as the sourced conformal mode), [[F284-rigid-lattice-expansion-and-primordial-state]] (the companion: what expansion *is*, given rigidity), [[F130-blockspin-rg-gauge-gravity]] (block-spin rescales the *description*, not the substrate — the contrast that makes "elastic" precise). External: Hofmann & Müller 2018 (CQG **35** 035015, LLR $\dot G/G$); Williams, Turyshev & Boggs 2004; Copi, Davis & Krauss 2004 (BBN bound on $G$); Abbott et al. 2017 (GW170817 + GRB 170817A, $\Delta c/c$); Bertotti, Iess & Tortora 2003 (Cassini $\gamma$); Uzan 2011 (varying constants review).

Raised by Ben, 2026-08-02: *"is it possible for the BCC lattice to be 'elastic' within the model? If we introduce a variable fundamental lattice spacing, what happens?"* — the obvious escape from F282, and worth asking precisely because F282 itself pointed at $a$ as a falsifier.

---

## 1. Why this is the right question, and why F282 got its own falsifier wrong

F282 turns on one number: $\Lambda_\text{UV}=1/a$ sits *below* $M_\text{Pl}$, so $r\equiv M_\text{Pl}^2/\Lambda^2=\sqrt3>1$. The natural response is: **make $a$ smaller.** Push the cutoff above $M_\text{Pl}$ and $r<1$, and slow roll is back on the table. F282 §9 explicitly listed this as falsifier 5.

It does not work, and the reason is the same finding that fixes $a$ in the first place.

## 2. E1 — the obstruction is invariant under any stretch (exact)

Let the lattice be elastic: $a\to s\,a$ for an arbitrary positive stretch $s$ (constant, or $s(t)$ — E1 is algebraic and does not care). **F79 ties Newton's constant to the spacing:**

$$G=\frac{(sa)^2c^3}{8\pi\sqrt3\,\hbar}\qquad\Longrightarrow\qquad M_\text{Pl}=\sqrt{\frac{\hbar c}{8\pi G}}=\frac{3^{1/4}\hbar}{s\,a\,c},\qquad \Lambda_\text{UV}=\frac{\hbar}{s\,a\,c}.$$

**Both scale as $1/s$.** The Planck mass is not an external yardstick the lattice can be measured against — in this model it *is* a lattice quantity, because $G$ is structural. Therefore

$$\boxed{\ \frac{M_\text{Pl}}{\Lambda_\text{UV}}=3^{1/4}\ \ \text{and}\ \ r=\frac{M_\text{Pl}^2}{\Lambda_\text{UV}^2}=\sqrt3=\frac1{c_\text{lat}}\quad\text{for every }s,\qquad \frac{\partial r}{\partial s}\equiv0.\ }$$

$\hbar$, $c$, $a$ and $s$ all cancel identically (checked symbolically with every symbol free, so the cancellation is displayed, not assumed).

**What this means.** $r=\sqrt3$ is not a statement about how big the lattice spacing happens to be. It is a **dimensionless geometric invariant of the BCC lattice** — it is $1/c_\text{lat}$, and $c_\text{lat}=1/\sqrt3$ comes from the $d=3$ eight-neighbour Weyl walk (F26). You cannot dial away a coordination number by stretching the lattice, any more than you can change a crystal's symmetry group by heating it.

**Consequence for F282: the no-go gets stronger, not weaker.** F282 presented its obstruction as flowing from the F107 canonical value of $a$. It does not; F107's value is irrelevant to it. Falsifier 5 is struck. Falsifiers 1–4 (a stiffness $J\ge780$, a non-compact direction, a tree $R^2$, a causal super-horizon mechanism) stand untouched.

## 3. E2 — an elastic lattice has a varying $G$, and that is measured

If $s$ is dynamical, $G\propto s^2$ is dynamical too. Parametrise the stretch against the FRW scale factor, $s\propto a_\text{FRW}^{\,q}$ — $q=0$ is a rigid substrate, $q=1$ is a lattice that comoves with the expansion (the intuitive picture of "space stretching"). Then $\dot G/G=2qH$, and today $2H_0=1.379\times10^{-10}\,\text{yr}^{-1}$.

| Probe | Bound | Implied $q$ | Comment |
|---|---|---|---|
| LLR (Hofmann–Müller 2018, 2σ) | $\lvert\dot G/G\rvert<1.5\times10^{-13}\,\text{yr}^{-1}$ | $q<1.1\times10^{-3}$ | comoving lattice excluded by **919×** |
| LLR (conservative) | $<4\times10^{-13}\,\text{yr}^{-1}$ | $q<2.9\times10^{-3}$ | excluded by 345× |
| BBN, $\lvert\Delta G/G\rvert<0.1$ at $z\simeq4\times10^{8}$ | $2q\ln(1+z)<0.1$ | $q<2.5\times10^{-3}$ | independent of LLR, agrees |
| BBN vs a **fully comoving** lattice | $G_\text{BBN}/G_0=(1+z)^{-2}=6.2\times10^{-18}$ | — | **off by 17.2 decades** |

Two independent probes, 17 orders of magnitude apart in epoch, agree: $q\lesssim10^{-3}$.

> **The lattice is rigid to within ~0.1%.** This is a *prediction the model did not know it was making*: because F79 makes $G$ structural rather than fundamental, every bound on $\dot G/G$ is automatically a bound on lattice elasticity, and the data had already answered the question before it was asked.

## 4. E3 — the volume mode is not a new field; it is $\ln K$

Here is the sharpest point, and it is structural rather than numerical. **A variable fundamental spacing *is* the conformal (volume) deformation of the lattice.** The model already owns that mode, and has already established what it is:

- **F79:** the conformal factor $\tfrac12\ln K$ has **zero tree stiffness** — source-free Maxwell is conformally invariant in 3+1D and the EM stress tensor is traceless, so there is no tree-level elastic energy for the volume mode. The lattice has no bare bulk modulus. This is not an assumption; it is what makes $G$ purely induced, and hence what produces $G=a^2c^3/(8\pi\sqrt3\hbar)$ matching CODATA to $3\times10^{-8}$.
- **F180:** $\ln K$ obeys $(\nabla^2-c_\text{lat}^{-2}\partial_t^2)\ln K=-(8\pi G/c^4)T^{00}$ — a **sourced** equation. It has no potential and no independent vacuum dynamics.
- **F216:** the propagating content in vacuum is exactly **2 dof** (transverse-traceless), protected by the emergent-diff Ward identity $\Pi\propto Q^2$. There is no third, scalar, propagating gravitational mode.

So "make the lattice elastic" resolves into a dichotomy with no third branch:

| Branch | What it means | Outcome |
|---|---|---|
| **A** | The volume mode *is* $\ln K$ | **Nothing is added.** $K$ is constrained, sourced, potential-free and non-propagating in vacuum. The elastic picture is a *re-description* of machinery the model already has — and it is the correct one. What it then says about expansion is [[F284-rigid-lattice-expansion-and-primordial-state]] |
| **B** | A genuinely new, independent scalar dof | Breaks F216's 2-dof count, and couples to $T$ as a PPN scalar. Cassini's $\lvert\gamma-1\rvert<2.3\times10^{-5}$ forces $\alpha<3.4\times10^{-3}$ — the mode of the substrate that *carries* gravity would have to couple to matter **295× more weakly than gravity itself** |

Branch B is not quite a proof (the coupling $\alpha$ of a hypothetical substrate mode is not derived here — see §7), but it is a sharp, quantified tension in a direction the model has no freedom to move.

## 5. E4 — a tree elastic term would give gravity a second light cone

F180 does not *posit* $c_\text{grav}=c_\text{lat}$; it **derives** it, precisely because the graviton's kinetic term is nothing but the induced matter loop, so gravity inherits the matter light cone. Any tree-level elastic stiffness contributes an independent term carrying its own sound speed $c_s$, and that inheritance breaks.

Writing the fractional shift as $\Delta c/c\simeq\tfrac12 f_\text{tree}\,(c_s^2/c_\text{lat}^2-1)$, GW170817 + GRB 170817A ($-3\times10^{-15}<\Delta c/c<7\times10^{-16}$) gives, for an $O(1)$ sound-speed offset,

$$f_\text{tree}\lesssim6\times10^{-15}\qquad\text{(14.2 decades below unity).}$$

This is the same structure that killed the $\sigma$-bilinear photon (F65–F67: a second cone ⇒ birefringence ⇒ excluded by GRB/AGN polarimetry). **The model has now measured, twice and in two sectors, that there is exactly one light cone** — and an elastic substrate is a second one.

## 6. Verdict

> **The BCC lattice cannot usefully be made elastic, and elasticity would not help if it could.** (E1) The F282 obstruction $r=\sqrt3=1/c_\text{lat}$ is **exactly invariant** under any stretch, because F79 makes $M_\text{Pl}$ and $\Lambda_\text{UV}$ scale together — so no choice of fundamental spacing, constant or dynamical, changes the inflation verdict by one part. (E2) A dynamical stretch varies $G$; LLR and BBN independently pin the comoving fraction at $q\lesssim10^{-3}$, and a fully comoving lattice misses BBN by 17 decades. (E3) The volume mode is not a new field — it is $\ln K$, which F79/F180/F216 have already established as sourced, potential-free and non-propagating; the only alternative is a PPN scalar Cassini bounds at $3.4\times10^{-3}$. (E4) A tree elastic stiffness would give gravity its own light cone, bounded at $6\times10^{-15}$ by GW170817.

**The lattice is rigid, and $a$ is a constant of the substrate.** That is now a supported statement rather than a tacit assumption — which is worth more than the assumption was.

## 7. Falsifiers

1. **A measured $\dot G/G$ near $2H_0$.** Would establish $q\approx1$ and falsify rigidity outright. This is the cleanest single test, and it is already 3 orders on the model's side.
2. **A detected scalar polarisation in gravitational waves.** Would be branch B of §4 and would break F216's 2-dof count.
3. **$c_\text{grav}\ne c_\text{EM}$ at $>10^{-15}$.** Would admit a tree elastic term.
4. **A derivation giving a substrate volume mode $\alpha<3.4\times10^{-3}$.** Would rescue branch B from Cassini. §4's tension is quantified but not closed: $\alpha$ for a hypothetical new mode is *argued* to be $O(1)$, not computed.
5. **A tree-level bulk modulus for the lattice.** Would contradict F79's zero tree stiffness — and would also break the $G$ value that matches CODATA to $3\times10^{-8}$, so it is expensive.

## 8. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$ and $r=\sqrt3$ for all $s$; $\partial r/\partial s\equiv0$ | **exact-algebraic** (sympy, all symbols free) |
| $r=1/c_\text{lat}$: the obstruction is the BCC coordination geometry, not a scale | **exact** |
| **Correction to F282 falsifier 5** | **proved** — that falsifier was unsound |
| $\dot G/G=2qH$; $q<1.1\times10^{-3}$ (LLR), $q<2.5\times10^{-3}$ (BBN) | **quantitative** (external bounds) |
| Comoving lattice off BBN by 17.2 decades | **quantitative** |
| Volume mode $=\ln K$: zero tree stiffness, sourced, 2 dof | **structural** (F79/F180/F216) |
| Cassini $\alpha<3.4\times10^{-3}$ for branch B | **quantitative**; the $O(1)$ natural value is **argued, not derived** (falsifier 4) |
| Tree elastic fraction $<6\times10^{-15}$ from GW170817 | **quantitative** (assumes an $O(1)$ $c_s$ offset) |
| A first-principles bulk modulus for the BCC substrate | **open** — E3 argues it must vanish at tree level from F79, but the elastic constants of the lattice have never been computed directly |

## 9. Honest scope

E1 is the load-bearing result and it is airtight: it is one line of algebra whose content is that the model has no free scale to dial, because $G$ is structural. E2 is as strong as the external $\dot G/G$ bounds, which are robust and mutually independent. E3 is the most interesting and the least finished: the *dichotomy* is solid, branch A is well-supported by three existing findings, but branch B's exclusion rests on a natural-coupling argument rather than a computed $\alpha$. E4 assumes an $O(1)$ sound-speed offset; a tuned $c_s=c_\text{lat}$ would evade it, at the cost of a coincidence. None of these touch E1, which is what the question was actually about.

## 10. Files
- Module: `src/casim/engine/interactions/cosmology_lattice_elasticity.py`
- Test: `tests/findings/test_F283_F284_lattice_elasticity.py`
- Results: `test-results/F283_F284_lattice_elasticity.json`
