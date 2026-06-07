# F108 — The global-stability invariant attacked: an exact no-go theorem excludes the entire democratic class flagged in F101-A2, the working geometry is localized to a two-invariant quartic completion (demonstrated globally stable at fixed $W^*$), and the momentum-resolved $E_g$/$A_{1g}$ bubble is built, verified exactly, and honestly negative at one loop

**Date:** 2026-06-06 - 23:05
**Numbering note:** drafted as F107; renumbered **F108** — F107 was taken by the concurrent canonical-SI-ruler finding (`F107-canonical-a-adoption-L4-grb-gate.md`, same day).
**Status:** Partial (one exact theorem + one constructive sufficiency + one localization + sharp negatives) — 11/11 checks PASS. **The headline (exact):** the invariant F101-A2 asked for — "one more democratic-sector invariant (e.g. a quartic $\bar y$ cost)" — **cannot exist at any strength or functional form**. For *every* added invariant $w(\bar y)$, the closed-form refit leaves $\kappa_E$ and the wall-KKT margin invariant and shifts only $\mu$ (T1, machine precision), and the democratic shadow $(\bar y_*,\bar y_*,\bar y_*)$ — which shares $\bar y$ with the lepton point — then cancels $w$ and the refit *identically* in the energy difference. What survives is the lepton point's own splitting cost, giving the exact bound
$$\mathrm{Gap}\;\ge\;\Delta_\infty=\tfrac{\kappa_E}{2}e_*^2+W^*S_3^{*2}+\Big[\textstyle\sum_a g(y^*_a)-3g(\bar y_*)\Big]=+0.0386>0 ,$$
verified by full minimization: the gap falls monotonically toward $\Delta_\infty$ and the ground state converges to the shadow (T2). **Localization:** every *single* quartic invariant also fails (per-axis $v\sum y^4$, $E_g$ $c\,e^4$, cross $\bar y^2e^2$, both signs, refit-consistent; best gap $0.048$, T3). **What works:** the pair $\{v\sum_a y_a^4\ (v<0),\ c\,e^4\ (c>0)\}$ has an open region ($v\approx-0.175$, $c\approx0.22$–$0.30$) at fixed $W^*=1.46$ where the **exact lepton point is the global ground state** with wall KKT and PD constrained Hessian (T4) — the working geometry is a quartic-for-quadratic swap in the $E_g$ sector (which halves the splitting cost at fixed stationarity) plus a per-axis quartic attraction. **The honest tension:** $\sum y^4$ carries $3\bar yA^3\cos3\delta$ (F95-D2), so $v$ feeds the cubic and moves the F95 angle requirement ($W^*\!:1.46\to2.58$ at $v=-0.175$), where the T4 stability is lost; no self-consistent $(W,v,c)$ with $\kappa_E>0$ was found, and with $\kappa_E<0$ allowed (Mexican-hat $E_g$ sector) the gap shrinks to $4\times10^{-3}$ against a *new* one-heavy competitor $(s,0,0)$ without closing (T5). **The bubble (audit C.2 route):** the momentum-resolved sea polarization $\Pi(q;m)$ is constructed on the exact F46/BCC sea and verified against exact diagonalization to $1.8\times10^{-6}$ (G1–G4) — and at one loop the $E_g$ sextic **stays wrong-sign**, positivity is **not** restored ($e\gtrsim0.35$), and the loop is strongly coupled ($\kappa+\Pi\approx0$ over much of the BZ): C.2 and C.3 do **not** close at one loop (M1). See §7.
**Script:** `model-tests/test_F108_democratic_no_go_and_bubble.py` (~20 s; caches `test-results/F108_pitable_L16.npz`)
**Results:** `test-results/F108_democratic_no_go_and_bubble.json`
**Cross-references:** [[F101-one-heavy-branch-fit-W]] (A2 metastability — the target; its flagged candidate is excluded here), [[F95-B-derived-C-localized]] (D2 harmonic content of $\sum y^4$, the localization style this follows; the brake requirement that creates the T5 tension), [[F96-second-shell-Eg-gap-saturation]] (the gap framework), [[F92-per-constituent-phase-consistency]] (the pair-budget structure §6 points to), [[F46-pythagorean-lattice-mass]] (the sea the bubble probes), [[F26-speed-of-light-as-rotation-rate]] (the walk structure $U=u\,I-i\,n\cdot\sigma$ used in the matrix elements).

---

## 1. The theorem (T1/T2): no democratic invariant can do the job

Add **any** $E_w=w(\bar y)$ to the F101 functional and refit. The light-flavor
stationarity equations are linear in $(\kappa_E,\mu)$ with columns
$(y_a,\bar y)$; the $w$-gradient $w'(\bar y)/3$ is a pure $\bar y$-column
shift, so exactly (machine precision, two unrelated $w$ tested):

$$\kappa_E\ \text{invariant},\qquad \mu\to\mu-\frac{w'(\bar y_*)}{3\bar y_*},\qquad
\text{wall-KKT margin invariant}.$$

Now compare the lepton point $y^*=(1,u,v)$ with its **democratic shadow**
$(\bar y_*,\bar y_*,\bar y_*)$. Both have the same $\bar y$, so $w$ *and* every
refit-induced change cancel identically in the difference, leaving the
$\bar y$-independent splitting cost:

$$E(y^*)-E(\text{shadow})=\underbrace{\tfrac{\kappa_E}{2}e_*^2}_{+0.1739}
+\underbrace{W^*S_3^{*2}}_{+0.0224}
+\underbrace{\textstyle\sum_a g(y^*_a)-3g(\bar y_*)}_{-0.1577}
=\Delta_\infty=+0.0386 .$$

Since the global minimum is $\le E(\text{shadow})$,
$\mathrm{Gap}\ge\Delta_\infty$ for every $w$ and every strength. Verified
nonperturbatively for $w=\lambda\bar y^4$, $\lambda\in[0,30]$: gap
$0.205\to0.045$, monotone, never below $0.0386$; ground state
$\to(0.402,0.402,0.402)\to$ the shadow. **F101-A2's "democratic quartic
$\bar y$ cost" is excluded as a class.** The physical content: the sea's
splitting reward ($-0.158$) does not pay for the contact + brake cost of
splitting ($+0.196$); no amount of democratic bookkeeping changes that
difference. The invariant the model needs must **reduce the splitting cost
itself**.

## 2. Localization (T3): single quartic invariants all fail

Refit-consistent scans at $W^*=1.46$ over $v\sum_a y_a^4$, $c\,e^4$,
$b\,\bar y^2e^2$ (both signs): the lepton point is never global. Best case:
per-axis *attraction* $v\approx-0.18$–$-0.19$ at the $(0,0,0)/(1,1,1)$
crossover, gap $0.048$ — close to the democratic floor but above it. The
$E_g$ quartic alone back-fires: the refit absorbs it into $\kappa_E$
($c=-0.5\Rightarrow\kappa_E=1.72$) and the splitting cost *rises*.

## 3. Sufficiency (T4): the two-invariant completion works at fixed $W^*$

$$E\;+\;v\sum_a y_a^4\;+\;c\,e^4,\qquad v\approx-0.175,\ c\approx0.22\text{–}0.30:$$

the **exact lepton spectrum is the global ground state** (grid-refined global
minimization lands on $(1,\,0.244,\,0.017)$; wall KKT $<0$; constrained
Hessian PD). Mechanism: at fixed stationarity a quartic carries the same
gradient as a quadratic at *half* the energy, so moving $E_g$ stiffness from
$\kappa_E e^2/2$ into $c\,e^4$ cuts the lepton's splitting cost without
touching $(1,1,1)$ or $(0,0,0)$ (both have $e=0$); the per-axis $v<0$ tunes
the $(1,1,1)$/$(0,0,0)$ balance. Note the magnitudes: $v,c=O(0.2)$ — the
$O(1)$-strength second-shell condensate self-interaction scale that F95
already demanded for $C$; and the sea's own per-axis quartic is
$-\tfrac{I_2}{2}=-0.110$, the same order as the required $v$.

## 4. The honest tension (T5): self-consistency with the angle requirement

$\sum_a y_a^4$ contains $3\bar yA^3\cos3\delta$ (F95-D2 exact), so $v$ shifts
the effective cubic: $B_\text{eff}(v=-0.175)=-0.1005$ vs $B_\text{sea}=-0.0569$,
and the F95 requirement $C=0.636|B_\text{eff}|$ moves $W^*$ to $2.58$ — where
the T4 region is no longer globally stable. Scanning the self-consistent line
$W=W^*(v)$: with $\kappa_E>0$ no solution; allowing $\kappa_E<0$
(spontaneous-splitting Mexican hat in $e$, locally admissible — KKT and
constrained Hessian still hold) the gap falls to $4\times10^{-3}$
($v=0.15,c=0.85$) against a **new competitor class $(s,0,0)$** (one heavy,
two empty) without closing in the scanned domain. The completion exists at
fixed $W$; its self-consistent version is the sharply posed remaining
problem — and the $(0,0,0)/(s,0,0)/(1,u,v)/(1,1,1)$ competitor ladder again
invites (but does not establish) the sector reading flagged in F101.

## 5. The momentum-resolved bubble (M1, audit C.2 route): exact machinery, honest negatives

Built from scratch on the exact F46/BCC sea: per branch
$U(k)=e^{i\theta\sigma_1}e^{i\omega(k)\sigma_3}$, $\theta=\arcsin m$, Bloch
vector $n=(\sin\theta\cos\omega,\,-\sin\theta\sin\omega,\,\cos\theta\sin\omega)$;
mass modulation $\delta\theta(x)=2\delta\cos qx$ gives the *exact* sea response

$$\Pi_\theta(q;m)=2\,\Big\langle\;-\tfrac12\,\big|X_{-+}(k{+}q,k)\big|^2
\cot\tfrac{\Omega_k+\Omega_{k+q}}{2}\;\Big\rangle_{k,\text{branches}},\qquad
|X_{-+}|^2=\tfrac{1-\hat n'\!\cdot\tilde n}{2},\ \tilde n=(n_1,-n_2,-n_3),$$

with quasi-energy PT verified on random unitaries ($7\times10^{-8}$), the
trace formula exact, the full assembly vs **exact diagonalization** of the
modulated walk to $1.8\times10^{-6}$, and $\Pi_y(q\to0)=g''(y)$ to $\le1\%$.
(Convention: $k+q$ on the mode-grid torus — the BCC dispersion is
$4\pi$-periodic, so this matches the exact chain construction; flagged as a
scope choice.) Results at the $W^*$-fit couplings:

1. **Wrong sign persists:** the $E_g$ sextic of
   $E_\text{fl}=\tfrac12\langle\ln\det[\kappa+\Pi(q)]\rangle_\text{BZ}$ is
   negative on every PD probe circle ($W_\text{ind}=-135$ to $-566$,
   PD-boundary dominated) — the F101-C static negative is *not* cured by
   momentum resolution.
2. **Positivity not restored:** the operator loses PD at $e\gtrsim0.35$
   (heavy flavor $y\approx0.71$), essentially the static boundary; the
   momentum stiffening $(\theta')^2[\Pi_\theta(q)-\Pi_\theta(0)]>0$ is an
   order of magnitude too small.
3. **Strongly coupled:** $\kappa_E+\Pi_y\approx0$ over much of the BZ at
   physical amplitudes — the one-loop numbers ($a_4=+16.5$ democratic
   quartic, splitting stiffness $dE_\text{fl}/de^2=-3.0$) are not
   Landau-controlled and are reported as directions only. Notably the
   splitting stiffness is *negative* — fluctuations reward splitting,
   the direction $\Delta_\infty$ requires.
4. **New structure:** the softest sea mode is **not** $q=0$ — at small $m$
   the staggered $(\pi,\pi,\pi)$ mass mode is softer by $\approx0.019$
   (worth its own look: a staggered-mass/parity-partner channel).

**Verdict on the audit items:** C.3's flagged invariant is *excluded*
(theorem); the C.2 bubble is built and verified but does not deliver $W$ or
the stability invariant at one loop.

## 6. Where the invariant now lives

Combining the theorem (must reduce splitting cost), the localization (T4
geometry: quartic-for-quadratic in $E_g$ + per-axis quartic), and F95's
no-go for per-axis loops: the global-stability invariant has the same unique
allowed source as $C$ — the **second-shell condensate's own self-interaction
at $O(1)$ strength** — now with a *specific demanded geometry and sign
pattern* $(v<0,\ c>0)$ and the T5 self-consistency condition as its hard
target. Equivalently (F92 §6): a condensate kinematics in which the three
flavor amplitudes draw on a shared pair budget — note the equipartition
identity $e=\sqrt3\,\bar y$ holds *exactly* at the lepton point
($0.7279=\sqrt3\times0.4203$, Koide $\iff$ equipartition) — would remove the
democratic competitors kinematically rather than energetically. The F92
bridge build and this invariant appear to be the same remaining object
(audit items #3 and #4 merge).

## 7. Test summary (`test_F108_democratic_no_go_and_bubble.py`, 2026-06-06 - 23:02)

| Check | Statement | Result | Status |
|---|---|---|---|
| G1 | quasi-energy PT formula on unitaries | $6.8\times10^{-8}$ | PASS |
| G2 | $\lvert\langle s',n'\rvert\sigma_1\lvert s,n\rangle\rvert^2=(1+ss'\,\hat n'\!\cdot\tilde n)/2$ | $<10^{-12}$ | PASS |
| G3 | $\Pi$ assembly vs exact diagonalization | $1.8\times10^{-6}$ | PASS |
| G4 | $\Pi_y(q\to0)=g''(y)$ | $\le1\%$ (L16 vs L24) | PASS |
| T1 | refit identities, any $w(\bar y)$ | machine precision | PASS |
| T2 | no-go: $\mathrm{Gap}\ge\Delta_\infty=+0.0386$, monotone, shadow limit | verified $\lambda\le30$ | PASS |
| T3 | single quartic invariants fail | best gap $0.048$ | PASS |
| T4 | $\{v<0,c>0\}$ completion: lepton point **global** at $W^*{=}1.46$ | gap $0$, KKT, PD | PASS |
| T5 | self-consistency tension: $W^*(v{=}-0.175)=2.58$, stability lost | gap $0.257$ | PASS |
| M1 | bubble honest negatives + soft-mode structure | $W_\text{ind}<0$ all PD circles | PASS |

**Overall 11/11 PASS** (~20 s).

## 8. Provenance

- New content: the democratic no-go theorem and the exact bound
  $\Delta_\infty$; the refit invariance identities; the single-invariant
  failure scan; the two-invariant global-stability existence; the
  $W^*(v)$ self-consistency tension and the $(s,0,0)$ competitor; the
  momentum-resolved $\Pi_\theta(q;m)$ construction with exact-diagonalization
  verification; the staggered soft-mode observation.
- Machinery: `ca_bcc.bcc_dispersion`, F46 map, F101 sea tables and fit
  (reproduced verbatim), quasi-energy PT, pure numpy (no scipy, per
  CLAUDE.md caution; mode-grid torus convention for $k+q$ noted in §5).
- Verification: `model-tests/test_F108_democratic_no_go_and_bubble.py`
  (2026-06-06 - 23:02, 11/11 PASS), results
  `test-results/F108_democratic_no_go_and_bubble.json`, cached bubble table
  `test-results/F108_pitable_L16.npz`.
- Masses: PDG charged leptons.
