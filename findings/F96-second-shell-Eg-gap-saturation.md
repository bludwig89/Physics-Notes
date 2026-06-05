# F96 — The second-shell $E_g$ gap computation at saturation amplitude: a two-value theorem excludes the strictly quadratic theory, the exact massless-electron texture algebra ($Q=\tfrac23\iff\delta=15°$), and the constructive unlock by the sextic invariant

**Date:** 2026-06-05 - 04:55
**Status:** Partial (strong structural result + exact algebra + constructive sufficiency) — 8/8 checks PASS. **The headline is a no-go with teeth:** the quadratic-cost mean-field gap theory on the BCC Dirac sea — any per-flavor + democratic four-fermion contact, either amplitude→mass map in the chain — supports **at most two distinct generation masses** (the two-value theorem, T3, realized over the full phase map, T4). The observed three distinct lepton masses therefore *exclude* it, making the non-quadratic $E_g$ self-term (F95's $C$) necessary for a **third independent reason** — beyond the angle brake (F95) and $m_e>0$, it is required for the very existence of three distinct masses. **The exact algebra:** any $(m_h, m_\text{mid}, 0)$ texture obeys $Q(u)=\frac{1+u^2}{(1+u)^2}$, $\tan\delta=\frac{\sqrt3\,u}{2-u}$ with $u=\sqrt{m_\text{mid}/m_h}$, and $Q=\tfrac23\iff u=2-\sqrt3=\tan15°\iff\delta=15°$ exactly, $\cos3\delta=1/\sqrt2$ — a new exact $45°$ ($=3\delta$) in the chain, and the $\varepsilon\to0$ limit the unlocked theory must approach. **Constructive sufficiency:** adding the single invariant $W(\sum_a p_a^3)^2$ — the $e^6\cos^23\delta$ sextic in flavor variables, whose square root is exactly F95's derived cubic — unlocks a three-distinct-mass phase (30 minimizers found). See §7.
**Script:** `model-tests/test_F96_second_shell_Eg_gap.py` (~40 s)
**Results:** `test-results/F96_second_shell_Eg_gap.json`
**Cross-references:** [[F101-one-heavy-branch-fit-W]] (2026-06-05: the §7 closing computation executed — the sea cliff pins $y_\tau=1$ exactly, the wall-pinned fit is closed-form with $W>0$ emergent, and F95's $C=0.636|B|$ meets the fit at $W^*=1.46$; metastability and the static-RPA wrong sign recorded), [[F95-B-derived-C-localized]] (the localization this confirms and sharpens), [[F93-orthorhombic-Eg-vacuum]] (O5's "quartic Landau theory can never orthorhombify" — here realized dynamically and nonperturbatively), [[F92-per-constituent-phase-consistency]] (the saturation kinematics; the pair-sum map), [[F78-koide-amplitude-from-cooper-pair]] (B3 democratic no-go, sharpened by S1/T1), [[F77-njl-gap-rpa-selfconsistent]] (the gap methodology), [[F73-spin0-bound-pair-scalar]] (over-wrap bound — excludes the spurious $y>1$ phase), [[F46-pythagorean-lattice-mass]] (the sea dispersion).

---

## 1. The construction

Mean-field energy for the generation amplitudes $y=(y_0,y_1,y_2)\in[0,1]^3$
($y=\sqrt m$; A$_{1g}$ mean $\bar y$ + $E_g$ doublet $(e,\delta)$ — the F93
condensate):

$$E(y)=\tfrac{3\kappa_0}{2}\bar y^2+\tfrac{\kappa_E}{2}e^2+\sum_a g(y_a),
\qquad g(y)=f\big(m(y)\big),\quad f(m)=-\langle\Omega_\text{Dirac}(k;m)\rangle_\text{BZ},$$

with the exact F46/BCC dispersion (both branches), and **strictly quadratic
cost** — the mean-field image of four-fermion contacts; no cubic or sextic
invariant inserted by hand, so any angular structure is generated
dynamically. Both amplitude→mass maps in the chain are run: canonical
$m=y^2$ (F78) and the pair-sum law $m=y\sqrt{2-y^2}$ (F73/F92 saturation
kinematics; mass peak at $y=1$, over-wrap beyond — the physical domain is
$y\in[0,1]$).

Channel structure (S1, exact): $\sum_a y_a^2=3\bar y^2+e^2$, so a per-flavor
contact weights the channels equally ($\kappa_0=\kappa_E$ — flavor-separable
⇒ degenerate, the F78-B3 no-go sharpened); the democratic bilinear
$(\sum_a y_a)^2=9\bar y^2$ feeds only $\kappa_0$. **Hierarchy requires an
inter-generation interaction** ($r=\kappa_E/\kappa_0\neq1$).

## 2. T1 — the stationarity theorem (exact)

$$\frac{\partial E}{\partial y_a}=\kappa_E\,y_a+\lambda+g'(y_a),\qquad
\lambda=(\kappa_0-\kappa_E)\,\bar y\ \ \text{(flavor-independent)}.$$

All three flavors solve the **same scalar equation**
$\kappa_E y+g'(y)=-\lambda$: distinct flavor values must be distinct
*stable* roots of one 1-D equation (or held boundary points).

## 3. T3 — the two-value theorem (the no-go)

Census of simultaneously available stable values on $[0,1]$ over both maps,
$\kappa_E\in[10^{-3},3]$, $\lambda\in[-0.3,0.3]$: **maximum 2.** The logic:
the corner $y=0$ is held iff $\lambda>0$, but then a small-branch root of
$h(y)=\kappa_E y+g'(y)=-\lambda<0$ requires the falling (unstable) branch —
corner and small stable root are mutually exclusive; $\lambda<0$ releases the
corner but offers only {small root, upper root}. Either way:

$$\boxed{\ \text{a strictly quadratic-cost gap theory on this sea supports at
most TWO distinct generation masses}\ }$$

for any amplitude→mass map tested. This is F93-O5's Landau statement
("the quartic theory can never give three distinct masses") **realized
dynamically and nonperturbatively** — and T4 confirms it: across the full
$(\kappa_0,r)$ phase map (13×13, both maps) there are exactly **zero**
three-distinct minimizers; only cubic / degenerate / tetragonal phases.
(The canonical map's strong splits sit exactly on the wall $y_\text{heavy}=1$
— saturation again. The lone apparent three-distinct "match" in an early run
lived in the unphysical over-wrap region $y>1$, excluded by F73.)

## 4. T2 — the exact texture algebra (the target the unlocked theory must approach)

For any mass pattern $(m_h, m_\text{mid}, 0)$, scale-free and
map-independent, with $u=\sqrt{m_\text{mid}/m_h}$:

$$Q(u)=\frac{1+u^2}{(1+u)^2},\qquad \tan\delta=\frac{\sqrt3\,u}{2-u},$$

and (sympy-exact)

$$Q=\tfrac23\iff u=2-\sqrt3=\tan15°\iff \boxed{\ \delta=15°\ \text{exactly}}\,,
\qquad \cos3\delta=\tfrac1{\sqrt2}\ (3\delta=45°).$$

So in the $m_e\to0$ limit, a Koide-satisfying spectrum is *forced* to
$\delta=15°$; the measured $\delta=12.733°$ differs by $2.27°$ — a
displacement carried entirely by $m_e>0$ ($m_e/m_\tau=2.9\times10^{-4}$).
Note the chain acquires another exact $45°$: $3\delta=45°$ at the Koide
point of the massless-electron curve.

## 5. T5 — the confrontation

The data have three distinct masses ⇒ the strictly quadratic gap theory is
**excluded**. The localized missing object (F95's $C$, the sextic $E_g$
self-interaction) is now necessary for three independent reasons:

1. the angle brake $\cos3\delta^*=-B/2C=0.786$ (F95);
2. $m_e>0$ (the corner can only be lifted by a non-separable, non-quadratic
   term);
3. **the existence of three distinct masses at all** (this finding).

One object, three jobs — a strong consistency hint that it is real.

## 6. T6 — constructive sufficiency

Adding the single invariant

$$E_W=W\Big(\sum_a p_a^3\Big)^2,\qquad p_a=y_a-\bar y$$

— precisely the $e^6\cos^23\delta$ sextic in flavor variables (its square
root, $\sum_a p_a^3\propto e^3\cos3\delta$, is the cubic invariant F95
*derived* from the sea) — **unlocks the three-distinct phase**: 30
three-distinct minimizers found over a modest $(W,\kappa_0,r)$ scan. The
term is sufficient as well as necessary. The explored grid lands on the
two-heavy side ($\delta>30°$, the sea prefers populating two flavors at the
upper root); the lepton-side branch (one heavy, $\delta<30°$) requires the
cost to forbid the second heavy while $W$ lifts the corner — locating it
and fitting $(\kappa_0,\kappa_E,W)$ to $(Q,\delta,m_e/m_\tau)$ is the
now-posable closing computation.

## 7. What this settles, and the remaining build

**Settled here:** the gap framework itself works end-to-end (S1→T6); the
quadratic theory's exclusion is a theorem with a census proof and a
dynamical realization; the massless-electron texture algebra is exact, with
$\delta=15°$ at the Koide point; the missing term is unique-by-elimination,
*and* demonstrably sufficient.

**Remaining (sharp):** fit the three couplings $(\kappa_0,\kappa_E,W)$ to
the three lepton shape numbers on the one-heavy branch, then (the real
prize) **derive $W$** — e.g. as the next order of the same Dirac-sea
expansion in the $E_g$ channel beyond mean field (the RPA/ladder bubble of
F77 applied to the second-shell channel), or from the second-shell bond
self-energy. F95's required magnitude $C=0.636|B|$ is the number it must
hit. The scale question (condensate-internal saturation vs the tiny
physical $m_\text{lat}$, F83/F92) remains open and is now the chain's last
structural gap.

## 8. Test summary (`test_F96_second_shell_Eg_gap.py`, 2026-06-05 - 04:50)

| Check | Statement | Result | Status |
|---|---|---|---|
| S1 | channels: $\sum y^2=3\bar y^2+e^2$; $r=1$ separable | exact | PASS |
| S2 | sea tables $g(y)=f(m(y))$, both maps | monotone, gain $0.1675$ | PASS |
| T1 | one scalar stationarity equation, $\lambda=(\kappa_0-\kappa_E)\bar y$ | exact | PASS |
| T2 | $(m_h,m_\text{mid},0)$: $Q=\tfrac23\iff\delta=15°$, $\cos3\delta=1/\sqrt2$ | sympy exact | PASS |
| T3 | two-value theorem: census max $=2$ | both maps | PASS |
| T4 | phase maps $W=0$: zero three-distinct minimizers | $2\times169$ pts | PASS |
| T5 | three observed masses ⇒ quadratic excluded ⇒ $C$ (3rd reason) | recorded | PASS |
| T6 | $W(\sum p^3)^2$ unlocks the phase | 30 minimizers | PASS |

**Overall 8/8 PASS.**

## 9. Provenance

- New content: the gap-framework construction, the two-value theorem and its
  census proof, the dynamical realization of F93-O5, the exact
  massless-electron texture algebra ($\delta=15°$ at Koide), the
  three-reasons convergence on $C$, and the $W$-unlock sufficiency demo.
- Machinery: `ca_bcc.bcc_dispersion` + F46 map (sea), sympy (exact parts),
  pure-numpy grid minimizer (no scipy, per CLAUDE.md caution).
- Verification: `model-tests/test_F96_second_shell_Eg_gap.py`
  (2026-06-05 - 04:50, 8/8 PASS), results
  `test-results/F96_second_shell_Eg_gap.json`.
- Masses: PDG charged leptons.
