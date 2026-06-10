# F118 — The self-consistent $(W,v,c)$ derivation closes on the spontaneous-$E_g$ (Mexican-hat) branch, the $\kappa_E>0$ branch is excluded, and the brake $C$ is localized to the $E_g$ condensate's own clock self-interaction at $O(1)$ strength ($\lambda_6=0.243\approx\tfrac14$, equivalently $W=1.46$) — with the sea loop now ruled out for $C$ by *sign* as well as scaling

**Date:** 2026-06-09 - 12:05
**Status:** Partial-positive (an existence closure on the physical branch + a sign no-go + an $O(1)$ localization; the first-principles value of $\lambda_6$ remains the residual) — 8/8 checks PASS. **The headline:** the $(W,v,c)$ triple that F108-T5 left open *does* have a self-consistent solution — but **only** on the $\kappa_E<0$ (attractive-$E_g$, Mexican-hat) branch, which is precisely the **spontaneous** $E_g$ condensation sign F93 already demands. On that branch the exact PDG lepton spectrum is the **global** ground state to grid resolution (gap $=-2\times10^{-6}$ under a $121^3$ brute search), with wall-KKT $<0$, PD constrained Hessian, and **all completion couplings $O(1)$** ($\kappa_E\approx-2.2,\ c\approx1.1,\ v\approx0.16,\ W=W^*(v)\approx0.44$). The $\kappa_E>0$ (repulsive) branch is **excluded** everywhere on the angle-locked line $W=W^*(v)$ (best global gap $0.066$; the empty $(0,0,0)$ always wins) — F108-T5 is sharpened from one point to the whole $(v,c)$ plane and then *closed* on the correct branch. **For $C$:** the brake is the unique symmetry-allowed $E_g$ "clock" self-interaction $C=\lambda_6\,e^6$ (the $e^6\cos^23\delta$ invariant); the **derived** cubic $B$ (F95) and the data ratio fix $\lambda_6=0.636|B|/e^6=0.243=O(1)$ — strikingly close to $\tfrac14$ — i.e. the equivalent brake $W=6\lambda_6=1.46$ (reproducing F101-B). And the sea loop is now **doubly excluded** as the source of $C$: beyond F95's wrong *scaling* ($C_\text{loop}\sim\bar y^7$ at small amplitude), the clip-free projection at saturation shows the loop's own sextic is **wrong-sign** ($C_\text{loop}=-0.018<0$, an anti-brake). See §6.
**Script:** `tests/findings/test_F118_self_consistent_Wvc_and_C.py` (~10 s)
**Results:** `test-results/F118_self_consistent_Wvc_and_C.json`
**Cross-references:** [[F108-democratic-no-go-global-stability]] (the $\{v\sum y^4,c\,e^4\}$ completion at fixed $W^*$ and the T5 self-consistency tension this closes), [[F109-f92-bridge-construction]] (the spontaneous-$E_g$ flow whose $\kappa_E<0$ sign is the branch that closes here; the $(s,0,0)$ competitor), [[F101-one-heavy-branch-fit-W]] (the wall-pinned closed-form refit and the $W^*=1.46$ two-route convergence reproduced in R1/B2), [[F95-B-derived-C-localized]] (the derived $B$, the per-axis no-go for $C$, the saturation hint — now extended to a *sign* no-go), [[F96-second-shell-Eg-gap-saturation]] (the gap framework), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ condensate is spontaneous — the $\kappa_E<0$ sign), [[F46-pythagorean-lattice-mass]] (the sea the loop probes).

---

## 1. The object and the open problem

The second-shell flavor functional (F96/F101/F108), $y=(y_0,y_1,y_2)\in[0,1]^3$:

$$E(y)=\tfrac{3\kappa_0}{2}\bar y^2+\tfrac{\kappa_E}{2}e^2+\sum_a g(y_a)
+W\Big(\sum_a p_a^3\Big)^2+v\sum_a y_a^4+c\,e^4,$$

with $p_a=y_a-\bar y$, $e^2=\sum_a p_a^2$, $g(y)=f(y^2)=-\langle\Omega_\text{Dirac}\rangle_\text{BZ}$ the exact F46/BCC sea, $\tau$ wall-pinned ($y_\tau=1$, F101-A0), and the closed-form refit $(\kappa_E,\mu)(W,v,c)$ making the exact lepton spectrum stationary (F101-A1). F108 established the $\{v\sum y^4\,(v<0),\,c\,e^4\,(c>0)\}$ completion makes the lepton point **global at fixed $W^*=1.46$** (T4), but flagged the **self-consistency tension** (T5): $v\sum y^4$ feeds the F95 cubic, so the angle requirement moves $W^*$ ($1.46\to2.58$ at $v=-0.175$) to where stability is lost; with $\kappa_E<0$ the gap shrank to $4\times10^{-3}$ but *closure was not established*. The two open items were therefore: **(1)** the self-consistent $(W,v,c)$ triple, and **(2)** a derivation of $C$ (equivalently $W$) from the second-shell condensate's own self-interaction at $O(1)$ strength.

Two facts make the self-consistency a *two-parameter* problem rather than three:
$c\,e^4$ is **$\delta$-blind** ($e^2=P_2$ is the $E_g$ magnitude), so it contributes neither to the cubic nor to the sextic angular harmonic; and the brake $W S_3^2\propto\cos^23\delta$ contributes no $\cos3\delta$. Hence the **angle requirement pins $W$ from $v$ alone**, $W=W^*(v)$, leaving $c$ free for global stability.

## 2. R1 — baselines reproduce F101/F108 exactly

$B_\text{sea}=-5.69\times10^{-2}$, $W^*(v{=}0)=1.460$, refit $r=\kappa_E/\kappa_0=0.986$, and the F108 floor $\Delta_\infty=+0.0386$ — all reproduced to the quoted precision. The machinery is the F108 code path (sea tables L=24, wall-pinned closed-form refit, `Wstar_of_v`), so the new results sit on the verified base.

## 3. A1 — the $\kappa_E>0$ branch is excluded everywhere on $W=W^*(v)$

Exhaustive scan of the angle-locked line: for every $(v,c)$ with $\kappa_E>0$ and wall-KKT $<0$, the lepton point is **never** the global ground state — best global gap $0.0655$, ground state always the empty $(0,0,0)$. The structural squeeze of F108-A2/T5 is confirmed across the *entire* plane: raising $v$ to beat $(1,1,1)$ lowers $W^*(v)$ and lets $(0,0,0)$ win; $c>0$ ($e^4$) *raises* the high-$e$ lepton point relative to the $e=0$ competitors, so it cannot help globally on the repulsive branch.

## 4. A2/A3 — the spontaneous-$E_g$ ($\kappa_E<0$) branch closes it

Allowing the **attractive** $E_g$ sign — the Mexican hat $-\tfrac12|\kappa_E|e^2+c\,e^4$ that *is* spontaneous $E_g$ condensation (F93) — and re-fitting closed-form, a self-consistent solution exists. Representative point ($v=0.16,\ c=1.10,\ W=W^*(v)=0.438$):

$$\kappa_E=-2.156,\quad\mu=2.335,\quad\text{wall-KKT}=-12.76<0,\quad
H^{(2)}_\text{min}=+0.234>0,$$

and a dense $121^3$ brute-force global search over the ordered simplex lands on $(1.000,\,0.242,\,0.017)$ — **the exact lepton spectrum** $(1,\,0.2439,\,0.0170)$ — with gap $=-2\times10^{-6}$ (grid resolution). The completion couplings are all $O(1)$, and the hat is properly bounded ($c>0$). **F108-T5 is closed on the physical branch**: the splitting is spontaneous *and* the lepton vacuum is global, simultaneously, with one self-consistent $(W,v,c)$.

The physical reading: the same Mexican hat that makes the $E_g$ doublet condense at all (F93) is what promotes the lepton point from F101-A2's metastable saddle to the true ground state. The "extra" couplings $(\kappa_E<0,\,c,\,W)$ are not decorations — they are the $E_g$ order parameter's own self-interaction (quadratic-attractive + quartic-bounding + sextic-clock), exactly the "second-shell condensate self-interaction at $O(1)$ strength" F95/F108 §6 localized $C$ to.

## 5. A4 — the per-axis quartic economizes (the completion is robust, not fine-tuned)

The pure-$E_g$ hat ($v=0$) still closes, but only with a larger quartic $c\approx2.4$ and a deeper $\kappa_E\approx-4.4$, beating the F108-T5 $(s,0,0)$ one-heavy competitor (the ground state runs $(0.70,0,0)\to(0.79,0,0)\to(1,0.25,0.01)$ as $c$ grows). A modest per-axis $v\approx0.16$ economizes the solution to $c\approx1.1,\ \kappa_E\approx-2.2$. So the closure is not a knife-edge: it holds over a 2D region $v\in[0.14,0.22]$, $c\in[0.75,1.2]$, $\kappa_E\in[-2.4,-1.6]$, all $O(1)$.

## 6. B1/B2 — $C$ is the $E_g$ clock self-interaction at $O(1)$; the loop is excluded by sign too

**B1 (sign no-go, new).** Projecting the full nonperturbative sea $F(\delta)=\sum_a g(y_a(\delta))$ on the **clip-free** equipartition circle ($A=\sqrt2\,\bar y$, $\bar y\le$ the cap $1/(1+\sqrt2)$) onto $\cos6\delta$ gives the loop's own sextic $C_\text{loop}$. At saturation amplitude it is **negative** ($C_\text{loop}(\text{cap})=-1.82\times10^{-2}$) — an *anti-brake*. (F95's "lock $|B|/2C\approx2.0$ at the cap" was a magnitude; the sign is wrong.) Combined with F95's wrong *scaling* at small amplitude ($C_\text{loop}\sim\bar y^7$, here $-6\times10^{-5}$ at $\bar y=0.30$), the sea loop is **doubly excluded** as the source of the positive brake $C$: it has the wrong magnitude where the masses are tiny and the wrong sign where the amplitude is $O(1)$.

**B2 (localization, $O(1)$-pinned).** The brake must therefore be the unique symmetry-allowed $E_g$ clock invariant — for a doublet $\Phi=e\,e^{i\delta}$ under the trigonal point group, $\mathrm{Re}(\Phi^3)^2=e^6\cos^23\delta$ — i.e. $C=\lambda_6\,e^6$. The derived cubic $B=-0.0569$ (F95) and the data ratio $\cos3\delta_*=0.785874$ fix

$$C_\text{req}=0.636\,|B|=+3.62\times10^{-2}>0,\qquad
\boxed{\;\lambda_6=\frac{C_\text{req}}{e^6}=0.243\;}\ \ (\approx\tfrac14),
\qquad W=6\lambda_6=1.46 .$$

(The identity $W S_3^2=(W/6)e^6\cos^23\delta$ gives $C=W e^6/6$, hence $W=6\lambda_6$ and the F101-B value $1.46$ reappears.) So $C$ is **localized, sign-fixed, and pinned to $O(1)$**: it is an $E_g$ self-interaction of coupling $\lambda_6=0.243$, having to *overcome* the wrong-sign loop ($C_\text{self}=C_\text{req}-C_\text{loop}=+5.4\times10^{-2}$). The proximity to $\tfrac14$ is flagged (not claimed): $\tfrac14$ is the rotor value $g_s^2\chi=\tfrac14$ of F115, and a derivation of $\lambda_6$ from the pair/saturation normalization (F92/F109) is the natural next target.

## 7. What this settles, and the residual

**Settled.** (i) The self-consistent $(W,v,c)$ triple **exists** — on the $\kappa_E<0$ branch, which is the *physically required* spontaneous-$E_g$ sign (A2/A3); the $\kappa_E>0$ branch is **excluded** (A1). F108-T5's "closure not established" is now closed on the correct branch. (ii) The completion couplings are all $O(1)$ and live in a 2D region, not a point (A4) — robust. (iii) $C$ is the $E_g$ clock self-interaction, $O(1)$, $\lambda_6=0.243$; the sea loop is excluded by sign *and* scaling (B1/B2).

**Residual (sharp).** A first-principles value of $\lambda_6$ ($\approx\tfrac14$?) and of $(v,c)$ from the bound-pair / saturation kinematics (F92/F109) — i.e. computing the $E_g$ order parameter's quartic and sextic self-couplings from the constituent contact at the unit-budget amplitude — is the one structural number still fitted rather than derived. The **existence** and the **$O(1)$ self-interaction character** are now established; the **magnitude** is localized to a single dimensionless clock coupling.

## 8. Test summary (`test_F118_self_consistent_Wvc_and_C.py`, 2026-06-09 - 12:04)

| Check | Statement | Result | Status |
|---|---|---|---|
| R1 | baselines reproduce F101/F108 | $B{=}{-}0.0569$, $W^*{=}1.46$, $r{=}0.986$, $\Delta_\infty{=}0.0386$ | PASS |
| A1 | $\kappa_E>0$ branch never global on $W{=}W^*(v)$ | best gap $0.066$, ground $(0,0,0)$ | PASS |
| A2 | $\kappa_E<0$ branch: lepton point **global** (self-consistent) | gap $-2\times10^{-6}$, KKT, PD | PASS |
| A3 | bounded Mexican hat; $O(1)$ couplings | $\kappa_E{=}{-}2.16,c{=}1.1,v{=}0.16,W{=}0.44$ | PASS |
| A4 | per-axis $v$ economizes; closure robust | $v{=}0$ needs $c{\ge}2.4$; region exists | PASS |
| B1 | sea-loop sextic **wrong-sign** at saturation | $C_\text{loop}(\text{cap}){=}{-}0.018$ | PASS |
| B2 | $C=\lambda_6 e^6$, $\lambda_6{=}0.243{=}O(1)$, $W{=}1.46$ | $\approx\tfrac14$ | PASS |
| V | verdict recorded | — | PASS |

**Overall 8/8 PASS** (~10 s).

## 9. Provenance

- New content: the full $(v,c)$ self-consistency scan along $W=W^*(v)$; the $\kappa_E>0$ exclusion and the $\kappa_E<0$ (spontaneous-$E_g$) closure with dense brute-force global verification; the economization result; the clip-free **wrong-sign** sea-loop sextic at saturation; the $E_g$ clock-invariant matching giving $\lambda_6=0.243=O(1)$.
- Machinery: F108 sea tables and wall-pinned closed-form refit reproduced verbatim (`ca_bcc.bcc_dispersion`, F46 map), pure numpy (no scipy, per CLAUDE.md), brute-force simplex global search.
- Verification: `tests/findings/test_F118_self_consistent_Wvc_and_C.py` (2026-06-09 - 12:04, 8/8 PASS), results `test-results/F118_self_consistent_Wvc_and_C.json`.
- Masses: PDG charged leptons.
