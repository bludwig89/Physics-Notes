# F95 — B and C from the QCA rule: the Dirac-sea loop derives the cubic invariant completely (form, origin, sign, closed form $B=-3\sqrt2\,I_2\,\bar y^4$) and proves the sextic brake cannot come from any per-axis energy — C is localized to the second-shell condensate's own self-interaction

**Date:** 2026-06-04 - 21:25
**Numbering note:** drafted as F94; renumbered **F95** — F94 was taken by the concurrent lattice-gauge-MC finding (`F94-lattice-gauge-mc-confinement-vs-F86.md`, renumbered from its own F87 draft the same day).
**Status:** Partial (half derived, half a sharp no-go) — 7/7 checks PASS. **Derived from the QCA rule:** (i) the F93 Landau *angular form* itself ($B\cos3\delta+C\cos^23\delta$ — only $\cos3n\delta$ harmonics can occur, a roots-of-unity theorem); (ii) the **origin** of $B$ — it is $A_{1g}\times E_g$ interference, coefficient exactly $3\bar yA^3$, vanishing iff the democratic background vanishes; (iii) its **closed form** $B=-\tfrac{3}{2}I_2\,\bar yA^3=-3\sqrt2\,I_2\,\bar y^4$ with $I_2=\langle\cot\omega_\text{kin}\rangle_\text{BCC}=0.2202$ a pure lattice constant (verified against the full nonperturbative BZ computation to $1.4\times10^{-4}$); (iv) its **sign** — $B<0$, so the loop drives the condensate to the *hierarchical* side ($0\le\delta<30°$), exactly where the data sit ($12.73°$). **The no-go:** the same loop's sextic coefficient scales as $\bar y^{\sim7}$ vs $B\sim\bar y^4$; at the physical lattice amplitudes (F83) the angle is tetragonally locked by **31 decades**, and even at the unitarity cap the lock never opens. Since *any* per-axis energy $\sum_a u(m_a)$ has the same scaling, the brake $C$ **cannot** come from a second loop of this type: it must be a direct $O(1)$-strength function of the $E_g$ invariants — the second-shell condensate's self-interaction at saturation-scale amplitude. The data demand $C=|B|/(2\times0.785874)=0.636\,|B|$. The F93 open problem is now half-closed and half-localized. See §7.
**Script:** `model-tests/test_F95_BC_from_qca_loop.py` (~25 s)
**Results:** `test-results/F95_BC_from_qca_loop.json`
**Cross-references:** [[F96-second-shell-Eg-gap-saturation]] (2026-06-05: the §7 closing computation executed — the quadratic gap theory is excluded by a two-value theorem, making $C$ necessary for a third independent reason; $W(\sum p^3)^2$ shown sufficient; the massless-electron texture algebra gives $\delta=15°$ exactly at Koide), [[F93-orthorhombic-Eg-vacuum]] (the open problem this attacks: $\cos3\delta^*=-B/2C=0.7859$), [[F76-generation-mass-hierarchy-crystal-field]] (C6 parametrization), [[F78-koide-amplitude-from-cooper-pair]] ($m=y^2$), [[F46-pythagorean-lattice-mass]] (the dispersion the sea fills), [[F57-induced-eh-term-from-leg-field-backreaction]]/[[F59-induced-eh-prefactor-and-f10-selection]]/[[F79-structural-newton-constant]] (the same induced/Sakharov logic, applied here to the condensate angle), [[F83-fix-lattice-spacing-from-fermion-mass]] (the physical $m_\text{lat}$ values), [[F92-per-constituent-phase-consistency]] (the saturation scale that reappears in §6).

---

## 1. The setup (every ingredient already in the model)

F93 reduced the orthorhombic vacuum to one number: $\cos3\delta^*=-B/(2C)=0.7859$,
the ratio of the cubic and sextic $E_g$ Landau invariants. This finding computes
the QCA-native candidate for both: the **Dirac-sea induced angular potential** —
the same Sakharov/induced logic the gravity sector uses (F57–F61, F79), applied
to the condensate angle.

The $E_g$ condensate at angle $\delta$ sets the generation amplitudes
(F76-C6 $\equiv$ F93-O4) $y_a=\bar y+A\cos\theta_a$, $\theta_a=\delta+2\pi a/3$,
$A=\sqrt2\,\bar y$ (equipartition, F80/F92); masses $m_a=y_a^2$ (F78); and the
sea energy per generation is

$$f(m)=-\big\langle \Omega_\text{Dirac}(k;m)\big\rangle_\text{BZ},\qquad
\cos\Omega=\sqrt{1-m^2}\,\cos\omega_\text{kin}(k)\ \ (\text{F46, exact}),$$

with $\omega_\text{kin}$ the BCC dispersion (both branches). At fixed
$(\bar y,A)$ the quadratic invariants are $\delta$-blind ($\sum y$ and
$\sum y^2$ exactly constant), so the **angle potential
$F(\delta)=\sum_a f(m_a(\delta))$ is parameter-free** — no coupling constant
enters the argmin.

## 2. D1 (exact) — the Landau angular form is derived

$$\sum_{a=0}^{2}\cos\!\big(k(\delta+\tfrac{2\pi a}{3})\big)=
\begin{cases}3\cos k\delta & 3\mid k\\ 0 & \text{else}\end{cases}$$

(roots-of-unity sum, verified exactly for $k=1..10$). Corollary: for **any**
analytic $f$, $F(\delta)$ contains only $\cos3n\delta$ harmonics — F93's
$B\cos3\delta+C\cos^23\delta$ is the general low-order form, *derived*.

## 3. D2 (exact) — B is $A_{1g}\times E_g$ interference

$$\sum_a y_a^4=\text{const}+\boxed{3\,\bar y A^3}\cos3\delta ,$$

verified symbolically (24-node exact projection; remainder identically zero).
The $\cos3\delta$ coefficient is **linear in the democratic background
$\bar y$**: a pure splitting field ($\bar y=0$) generates no $\cos3\delta$ at
any even power through $y^8$ (verified) — only $\cos6n\delta$. So the cubic
invariant exists *because* the leptons carry both an $A_{1g}$ and an $E_g$
component — the same equipartition structure that fixes $Q=2/3$.

## 4. D3/D4 — the closed form and the nonperturbative check

Expanding $f$ to $O(m^2)$: $f(m)=f(0)-\tfrac{I_2}{2}m^2+\dots$ with the pure
lattice constant

$$I_2=\big\langle\cot\omega_\text{kin}\big\rangle_\text{BCC}=0.2202\quad
(L=16/24/32:\ 0.21569/0.21913/0.22016),$$

giving

$$\boxed{\;B_\text{lead}=-\tfrac{I_2}{2}\cdot3\bar yA^3=-3\sqrt2\,I_2\,\bar y^4\;}
\qquad(A=\sqrt2\,\bar y).$$

The full nonperturbative $F(\delta)$ on the BCC BZ reproduces this to
$1.4\times10^{-4}$ at $\bar y=0.05$, and the measured scaling exponent is
$|B|\sim\bar y^{3.99}$. **B is derived: form (D1), origin (D2), magnitude
(D3), and the closed form survives the exact dispersion (D4).**

## 5. D5/D6 — the sign is right; the loop alone is falsified

$B<0$ at every amplitude: the sea **lowers its energy by hierarchy** (mass on
fewer generations ⇒ larger $\sum m_a^2$ ⇒ more negative sea energy), driving
$\cos3\delta\to+1$. Two consequences:

1. **Derived sign prediction:** the condensate sits on the hierarchical side,
   $0\le\delta<30°$ — the data's $12.73°$ obeys it. (Had the data sat at
   $\delta\in(30°,60°)$, $\cos3\delta<0$, the loop sign would be wrong — this
   was falsifiable.)
2. **Loop-only falsified:** at $\delta^*=0$ exactly, two masses are exactly
   degenerate — $m_e=m_\mu$. The observed $e$–$\mu$ splitting falsifies the
   loop-only theory and *proves* a brake $C$ of comparable size must exist.

## 6. D5/D7 — the no-go: C cannot come from any per-axis energy

The same loop's sextic coefficient scales as $C\sim\bar y^{7.2}$ (measured)
vs $B\sim\bar y^4$: the lock ratio $|B|/(2C)$ is $1.4\times10^3$ at
$\bar y=0.2$ and extrapolates to $\sim10^{31}$ at the physical amplitudes
($\bar y_\text{phys}=2.4\times10^{-10}$ from F83's $m_\text{lat}$). An interior
angle needs $|B|/(2C)<1$ — unreachable by **31 decades**. And this is generic:
*any* per-axis energy $\sum_a u(m_a)$ — another fermion species, a bond energy
per axis, any $\Sigma_a$-type loop — has the identical harmonic structure with
$B\sim\text{amp}^3\bar y$, $C\sim\text{amp}^6$, so stacking such terms can
never unlock the angle at small amplitude. Therefore:

$$\boxed{\;C\ \text{must be a direct function of the }E_g\text{ invariants
}(e^6\cos^23\delta)\text{ at }O(1)\text{ strength — the second-shell condensate's
own self-interaction.}\;}$$

The data fix its required size exactly: $C_\text{req}=|B|/(2\times0.785874)=0.636\,|B|$.

**Saturation hint (flagged, not a result):** scanning $\bar y$ up to the
unitarity cap $\bar y(1{+}\sqrt2)=1$, the lock ratio falls monotonically and
reaches $2.03$ at the cap ($\bar y=0.41$) — within a factor $2.6$ of the
required value. The only regime in which the loop's own sextic approaches the
needed strength is **saturation-scale amplitude** — the same $O(1)$ regime
F92 found for the pair (the amplitude filling the unit budget). A condensate
whose *internal* (constituent-level) amplitude is at saturation, while the
*physical* masses are the tiny F83 values, is exactly the structure the
F92 bridge construction would have to formalize. Recorded as the navigation
hint for the remaining build.

## 7. What is derived, what is localized, what remains

**Derived (this finding):** the angular form (D1); $B$'s origin ($A_{1g}\times
E_g$ interference, exact coefficient $3\bar yA^3$, D2); the closed form
$B=-3\sqrt2 I_2\bar y^4$ with $I_2$ a computable lattice constant (D3, checked
nonperturbatively, D4); the sign $B<0$ ⇒ data on the hierarchical side (D6);
the no-go — no per-axis induced potential can supply $C$ at physical
amplitudes (D5/D7).

**Localized (the sharpened residual):** $C$ — equivalently F93's
$\cos3\delta=0.7859$ — now has a *unique allowed source*: an $O(1)$-strength
sextic self-interaction of the second-shell $E_g$ condensate (or equivalently
a saturation-scale internal amplitude, §6). It can no longer hide in fermion
loops, bond energies, or any per-axis sector.

**Not addressed:** inter-generation ($T_{2g}$/off-diagonal) loop responses and
RG-log enhancements were not computed; they share the $\Sigma_a$ scaling
argument only partially and are the one loophole left open. The constructive
next step is unchanged from F92/F93 but now has a target number *and* a target
regime: a second-shell $E_g$ gap computation at saturation amplitude must
produce $C=0.636|B|$, i.e. $\cos3\delta=0.786$.

## 8. Test summary (`test_F95_BC_from_qca_loop.py`, 2026-06-04 - 21:20)

| Check | Statement | Result | Status |
|---|---|---|---|
| D1 | harmonic selection (roots of unity, $k=1..10$) | exact | PASS |
| D2 | $\cos3\delta$ coeff of $\sum y^4$ $=3\bar yA^3$; pure-$E_g$ has none | exact | PASS |
| D3 | $I_2=\langle\cot\omega\rangle=0.2202$, converging, $>0$ | $4.7\times10^{-3}$ (24→32) | PASS |
| D4 | closed form vs full BZ $F(\delta)$; $\delta^*$ scan | rel $1.4\times10^{-4}$; $\delta^*=0$ everywhere | PASS |
| D5 | $|B|\sim\bar y^{3.99}$, $C\sim\bar y^{7.2}$; physical lock | $\sim10^{31}$ | PASS |
| D6 | $B<0$ ⇒ data side; $\delta^*{=}0$ ⇒ $m_e{=}m_\mu$ (falsified) | confirmed | PASS |
| D7 | $C_\text{req}=0.636|B|$; per-axis shortfalls $4.8\times10^4$ / $1.8\times10^3$ / $2.6$ | recorded | PASS |

**Overall 7/7 PASS.**

## 9. Provenance

- New content: D1 selection theorem, the $A_{1g}\times E_g$ interference origin
  and closed form of $B$, the $I_2$ lattice constant, the sign prediction, the
  per-axis no-go for $C$, and the saturation-scale localization.
- Machinery: `ca_bcc.bcc_dispersion` (BCC dispersion, both branches), F46 map,
  F83 physical $m_\text{lat}$, sympy exact projections.
- Verification: `model-tests/test_F95_BC_from_qca_loop.py` (2026-06-04 - 21:20,
  7/7 PASS), results `test-results/F95_BC_from_qca_loop.json`.
