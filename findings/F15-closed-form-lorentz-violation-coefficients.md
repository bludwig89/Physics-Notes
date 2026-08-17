# F15 — Closed-form SR-2 Lorentz-violation coefficients: $\beta_\text{LV}$, $\gamma_\text{LV}$, $\delta_\text{LV}$, $\varepsilon_\text{LV}$ as exact functions of the mass, all four strictly negative

**Date:** 2026-05-19 - 23:30
**Amended:** 2026-05-22 - 01:14 — added $\delta_\text{LV}$ (the $\beta^6$ coefficient) and corrected the tabulated $\gamma_\text{LV}$ values, which had been carried over from a superseded expression.
**Promoted:** 2026-08-03 - 10:30 — moved out of the legacy bundle `findings/F01-F15-findings.md` into its own file with a gate-tier registry record, per recommendation 1 of [`docs/reviews/F01-F15-review-2026-08-03.md`](../docs/reviews/F01-F15-review-2026-08-03.md). Four errors found by that review are corrected here and flagged in §7.
**Status:** Confirmed — 6/6 PASS. **Exact algebraic**, zero fitted constants. Independently re-derived by a cold blind agent via a different route (2026-08-03) and confirmed to $8.3\times10^{-17}$.
**Reviewed:** 2026-08-03 — **CONFIRMED** (physics) as part of the `F01-F15` bundle review; the bundle itself graded UNDER-EVIDENCED, and this promotion is the fix.
**Module:** `casim.engine.interactions.derive_beta_LV`
**Test:** `tests/findings/test_F15_closed_form_beta_LV.py` — registry record `F15-closed-form-lv-coefficients` (gate tier, `expect.exactness: exact`)
**Results:** `test-results/F15_closed_form_beta_LV.json`
**Cross-references:** [[F12-sr-time-dilation]] (in the bundle — the SR-2 dispersion identity, and the open item *"does not derive $\beta_\text{LV}$ analytically"* that this closes; **note its parenthetical claim that $\beta_\text{LV}$ is positive is wrong**, see §5), [[F13]] (3D BCC, $\sim10\times$ larger numerical coefficient — the 3D closed form is still open), [[F28-grb-dispersion-test]] (the LIV observational gate, and the source of the correct $n=2$ bound), [[F30-photon-dispersion-order-anisotropy-birefringence]] (records the same float64 cancellation hazard), [[F245]] (the 2D/3D curl coefficients, same implicit-function machinery), [[F232]]/[[F107]] (the adopted lattice→SI identification, which **supersedes** the Finding 10 route this finding originally used).

---

## 1. Setup

The exact-QCA 2D-square Dirac dispersion along the $x$-axis ($k_y=0$) is the implicit relation

$$\cos\omega(k) = n\cos(ka),\qquad n=\sqrt{1-m^2},\qquad a=\frac1{\sqrt2}=c_\text{lat},$$

on the continuous positive-energy branch, with $m\in(0,1)$ **open at both ends** (at $m=0$ the
construction is $0/0$; see §6). Three quantities feed the SR-2 ratio:

- $\omega_\text{static}=\omega(0)=\arccos n=\arcsin m$ (F12, Part A)
- $v_g(k)=\partial\omega/\partial k$
- $\omega_\text{moving}=\omega(k)-k\,v_g(k)$

The lattice's analogue of $1/\gamma$ is $R=\omega_\text{moving}/\omega_\text{static}$, compared with
$1/\gamma_\text{SR}=\sqrt{1-\beta^2}$ at $\beta=v_g/c_\text{lat}$. The Lorentz-violation coefficients
are defined by

$$R(\beta)-\sqrt{1-\beta^2}=\beta_\text{LV}(m)\,\beta^2+\gamma_\text{LV}(m)\,\beta^4+\delta_\text{LV}(m)\,\beta^6+\varepsilon_\text{LV}(m)\,\beta^8+\mathcal O(\beta^{10}).$$

> **$R$ is a definition, not a derivation.** Nothing above establishes that $\omega-k v_g$ *is* the
> rate of a moving clock. It is one of several defensible Legendre-type constructions, and they do
> not agree beyond leading order. The physical reading of $\beta_\text{LV}$ rests on that choice.
> Likewise, expanding in $\beta$ rather than in $ka$ is an $m$-dependent reparametrisation
> ($\beta\simeq(n/m)ka$) and yields entirely different coefficients. Both caveats were raised by the
> 2026-08-03 blind re-derivation and are load-bearing.

## 2. The closed forms

With $\theta=\arcsin m$ and $T=\tan\theta=m/\sqrt{1-m^2}$:

$$\boxed{\;\beta_\text{LV}(m)=\frac12\left(1-\frac{m}{\sqrt{1-m^2}\,\arcsin m}\right)=\frac12\left(1-\frac{T}{\theta}\right)\;}$$

$$\gamma_\text{LV}(m)=\frac18-\frac{m(3-2m^2)}{24(1-m^2)^{3/2}\arcsin m}=\frac18-\frac1\theta\left(\frac{T}{8}+\frac{T^3}{24}\right)$$

$$\delta_\text{LV}(m)=\frac1{16}-\frac{m(8m^4-20m^2+15)}{240(1-m^2)^{5/2}\arcsin m}=\frac1{16}-\frac1\theta\left(\frac{T}{16}+\frac{T^3}{24}+\frac{T^5}{80}\right)$$

$$\varepsilon_\text{LV}(m)=\frac5{128}-\frac{m(35-70m^2+56m^4-16m^6)}{896(1-m^2)^{7/2}\arcsin m}$$

The rational constants $\tfrac12,\tfrac18,\tfrac1{16},\tfrac5{128}$ are the SR Taylor coefficients of
$-\sqrt{1-\beta^2}$; the numerator polynomials are $P_1=m$, $P_2=3m-2m^3$, $P_3=15m-20m^3+8m^5$,
$P_4=35m-70m^3+56m^5-16m^7$. The recursion
$a_{2n}(m)=R_n-P_n(m)/(D_n\,n^{2n-1}\arcsin m)$ continues indefinitely.

**The two forms in each line are the two independent derivations.** The left-hand form comes from
expanding $\arccos(n\cos u)$ in $u$ and reverting $u\to\beta$; the right-hand $T/\theta$ form comes
from the exact change of variable $t=\cos u$, which closes the construction in finite terms (§3).

## 3. The non-perturbative closed form (new, 2026-08-03)

The blind re-derivation found that the whole construction closes without any expansion. Setting
$t=\cos u$ and solving $\beta^2=n^2(1-t^2)/(1-n^2t^2)$ gives $\sin^2\omega=m^2\gamma^2$ and
$\sin^2u=\beta^2m^2/(n^2(1-\beta^2))$, hence **exactly**

$$\omega=\arcsin(m\gamma),\qquad u=\arcsin\!\left(\frac{\beta m\gamma}{n}\right),\qquad \gamma=\frac1{\sqrt{1-\beta^2}},$$

$$\boxed{\;R(\beta)=\frac{\arcsin(m\gamma)-\beta\,\arcsin(\beta\gamma\tan\theta)}{\arcsin m}\;}$$

and the generating identity $\dfrac{dR}{d\beta}=-\dfrac1\theta\arcsin(\beta\gamma\tan\theta)$,
$R(0)=1$, from which every coefficient follows by one termwise integration. Check **W2** confirms
this equals the module's lattice evaluation to $6.7\times10^{-15}$ over 35 $(m,k)$ points.

Two consequences the series form hides:

- **$\beta$ ranges only over $[0,\sqrt{1-m^2})$**, since $\sup_k\beta=n$ exactly. $\beta$ never
  reaches 1.
- **Resummed leading order:** the $O(m^2)$ parts of the four coefficients are
  $-\tfrac{m^2}{6}\{1,\tfrac12,\tfrac38,\tfrac5{16}\}$ — the $\gamma$-series — so

  $$R-\sqrt{1-\beta^2}=-\frac{m^2}{6}\,\frac{\beta^2}{\sqrt{1-\beta^2}}+\mathcal O(m^4)\quad\text{uniformly in }\beta.$$

## 4. Sign: all four coefficients are strictly negative — the open item is closed

$\theta=\arcsin m$ maps $(0,1)$ onto $(0,\tfrac\pi2)$. Let $h(\theta)=\tan\theta-\theta$; then
$h(0)=0$ and $h'=\sec^2\theta-1=\tan^2\theta>0$, so $\tan\theta>\theta$ and $T/\theta>1$ throughout.
Therefore $\beta_\text{LV}=\tfrac12(1-T/\theta)<0$, and since $T/\theta>1$ makes **every term** of
$\gamma_\text{LV}$, $\delta_\text{LV}$ and $\varepsilon_\text{LV}$ negative,

$$\beta_\text{LV},\ \gamma_\text{LV},\ \delta_\text{LV},\ \varepsilon_\text{LV}\ <\ 0\quad\text{for all }m\in(0,1).$$

**This closes the item the pre-promotion version of this finding left open** — *"whether
$\gamma_\text{LV}$ ever flips sign as $m\to1$"*. It does not: $\gamma_\text{LV}(0.999)=-306$,
$\delta_\text{LV}(0.999)=-4.6\times10^4$. The lattice clock runs *slower* than SR at every order:
$R<\sqrt{1-\beta^2}$ for all $\beta\in(0,n)$.

$\beta_\text{LV}$ is also **strictly decreasing in $m$**, since $\theta\mapsto\tan\theta/\theta$ is
increasing on $(0,\tfrac\pi2)$.

## 5. Small-$m$ expansion, and the Finding 12 sign correction

$$\beta_\text{LV}(m)=-\frac{m^2}{6}-\frac{11m^4}{90}-\frac{191m^6}{1890}-\frac{2497m^8}{28350}+\mathcal O(m^{10})$$

$$\gamma_\text{LV}=-\frac{m^2}{12}-\frac{31m^4}{360}+\dots,\qquad \delta_\text{LV}=-\frac{m^2}{16}-\frac{m^4}{12}+\dots,\qquad \varepsilon_\text{LV}=-\frac{5m^2}{96}+\dots$$

The entire LV tower vanishes as $m\to0$: **the Weyl sector is exactly Lorentz-invariant at this
order**, and only the Dirac sector picks up the deformation, suppressed by $m^2$.

**This contradicts Finding 12's parenthetical claim that $\beta_\text{LV}$ is positive** — the
magnitudes there are right; the sign was misread from an unsigned $|\Delta|$ column. Finding 12's
text in the bundle still carries the wrong sign and has not been corrected in place.

**As $m\to1$ the coefficient diverges**, $\beta_\text{LV}\sim-m/(\pi\sqrt{1-m^2})\to-\infty$, but the
accessible velocity range collapses with it ($\beta<n\to0$), so the largest achievable shift
$|\beta_\text{LV}|\beta_{\max}^2\to\sqrt{1-m^2}/\pi\to0$. **The physical Lorentz violation vanishes at
$m\to1$ even as the coefficient blows up.** Quoting the coefficient alone near $m=1$ is misleading.

## 6. Domain, and what the lattice spacing does (nothing)

- **$m=0$ must be excised.** At $m=0$, $n=1$ and $\arccos$ has a branch point at argument 1;
  $\omega=a|k|$ is non-analytic at $k=0$ and $\omega_\text{static}=0$, so $R=0/0$. Real-analyticity
  of $\omega$ in $k$, which the series reversion needs, holds only for $m>0$. The limit at fixed
  $\beta$ exists and equals $\sqrt{1-\beta^2}$ exactly.
- **$a=1/\sqrt2$ is decorative.** $\omega$ depends on $k$ only through $u=ka$, and $c_\text{lat}=a$,
  so $\beta=v_g/c_\text{lat}=d\omega/du$ and $\omega_\text{moving}=\omega-u\,d\omega/du$ are functions
  of $u$ alone: **$a$ cancels identically, before any expansion**, at every order. Check **W5**
  measures the spread across $a\in\{1/\sqrt2,1,0.25,3\}$ at 50 dps: $1.3\times10^{-54}$, i.e. zero.
  This matters because $a$ is listed in the setup as though it enters the answer. It does not. (It
  would, had $c_\text{lat}$ been anything other than the lattice spacing.)
- **Only even powers of $\beta$ appear**, because $\omega$ is even in $k$. Verified, not assumed.

## 7. Numerical verification, and the floor

| $m$ | $\beta_\text{LV}$ | $\gamma_\text{LV}$ | $\delta_\text{LV}$ |
|---|---|---|---|
| 0.01 | $-1.6668\times10^{-5}$ | $-8.3342\times10^{-6}$ | $-6.2508\times10^{-6}$ |
| 0.05 | $-4.1743\times10^{-4}$ | $-2.0887\times10^{-4}$ | $-1.5677\times10^{-4}$ |
| 0.10 | $-1.6790\times10^{-3}$ | $-8.4204\times10^{-4}$ | $-6.3344\times10^{-4}$ |
| 0.20 | $-6.8689\times10^{-3}$ | $-3.4772\times10^{-3}$ | $-2.6406\times10^{-3}$ |
| 0.50 | $-5.1329\times10^{-2}$ | $-2.8147\times10^{-2}$ | $-2.3262\times10^{-2}$ |

> **CORRECTION (2026-08-03).** The pre-promotion text attributed its numerical floor to *"the
> FFT/round-off floor ($\sim10^{-8}$)"* and claimed the analytic prediction is *"correct to nine
> significant figures"*. **Both are wrong, and in the finding's own disfavour.** There is no FFT
> anywhere in `derive_beta_LV.py` — the table is pure float64 arithmetic. The observed error tracks
> $\varepsilon/(|\beta_\text{LV}|\beta^2)$: **subtractive cancellation** in $R-\sqrt{1-\beta^2}$, a
> difference of two numbers near 1. It *diverges* as $k\to0$ rather than sitting at a floor, with an
> optimum at $\beta_*=(K\varepsilon/|\gamma_\text{LV}|)^{1/4}$ and a best achievable 6–9 significant
> digits in double precision. Re-run at 50 dps, the series is correct to $5\times10^{-16}$ at the
> same grid points — **six digits better than the finding claimed for itself**. Check **W6** asserts
> both halves: the high-precision agreement, and that the float64 error is predicted by the
> cancellation estimate to within an order of magnitude. The same misattribution was propagated into
> four rows of `docs/status/exactness-inventory.md` and is corrected there.
>
> A second, smaller instance: even the closed form $\tfrac12(1-m/(n\arcsin m))$ cancels in float64 at
> small $m$ (three digits lost at $m=0.05$), which is why checks W4–W6 run in `mpmath`.

## 8. Checks (`tests/findings/test_F15_closed_form_beta_LV.py`, 2026-08-03 - 10:24, 6/6 PASS)

| # | Statement | Tier | Result |
|---|---|---|---|
| W1 | All four coefficients reproduced by the **independent** $t=\cos u$ route at exact rational $m$ | exact | worst residual $8.3\times10^{-17}$; all odd orders identically 0 |
| W2 | Non-perturbative $R(\beta)$ equals the module's lattice `ratio_qca(k,m)` | machine | max $\lvert\Delta\rvert=6.7\times10^{-15}$ over 35 points |
| W3 | **Sign theorem**: all four coefficients $<0$ on $(0,1)$; $\tan\theta>\theta$ mechanism | exact | 999 grid points, no flip; derivative identity confirmed |
| W4 | Small-$m$: $m^6$ residual converges to the third coefficient $-191/1890$ | exact | dev $7.8\times10^{-6}$ (mpmath, 50 dps) |
| W5 | Lattice spacing $a$ is decorative | machine | spread over 4 values of $a$: $1.3\times10^{-54}$ |
| W6 | Floor is cancellation, not FFT | machine | 2-term rel. err $5.7\times10^{-14}$ at 50 dps; float64 err matches $\varepsilon/(\lvert\beta_\text{LV}\rvert\beta^2)$ to within $13\times$ |

**Failure mode (deliberate).** `lead_denom`, `next_num`, `next_denom` are the small-m rational
constants and are registry `params`. Verified 2026-08-03: `--param lead_denom=7`, `next_num=12` and
`next_denom=91` each drive the record to 5/6 FAIL. The record can fail.

## 9. Observational status — corrected

| Quantity | Value | Source |
|---|---|---|
| LIV energy scale, **$n=2$** (the order this mechanism produces) | $E_\text{QG,2}>1.3\times10^{11}$ GeV | Vasileiou et al. 2013, PRD 87 122001 (Fermi GRB 090510); cf. F28 |
| Muon **time-dilation** test | confirmed to $2\times10^{-3}$ (95% CL); $(0.8\pm0.7)\times10^{-3}$ at $\gamma\approx29.3$ | Bailey et al., Nature 268 (1977) 301; 1979 final report |

> **CORRECTION (2026-08-03).** The pre-promotion text quoted $E_\text{LV}\gtrsim10^{19}$ GeV — the
> **linear ($n=1$)** bound — for a mechanism it identifies one line later as $\mathcal O(k^4)$, i.e.
> $n=2$. Eight orders, and F28's table *in the same bundle file* already carried the correct value.
> It also quoted "CERN g−2 precision ($\sim10^{-7}$)", which is the precision on $a_\mu$, not on time
> dilation; the relevant bound is ~4 orders weaker. And it converted lattice→SI *"via Finding 10's
> $\sqrt d$ identification"*, which the project replaced: F232 adopted the lightcone $a/\tau=c\sqrt d$
> and F107 pins $a=\sqrt{8\pi}\,3^{1/4}\ell_P$.

For photon-like modes the relevant limit is $m\to0$, where the whole tower vanishes; the LIV
signature there is the $\mathcal O(k^4)$ dispersion correction (F28/F30), **not** the SR-2 ratio. For
a massive probe the deformation is a $\beta_\text{LV}(m)(v/c)^2$ multiplicative correction to time
dilation, with $m$ the *dimensionless lattice* mass $m a/\hbar c\lll1$ at any accessible scale.

**Falsifiability, stated honestly:** there is **no named experiment with a reachable threshold**. The
effect is unobservably small by construction ($\propto m^2$, vanishing in the massless limit), and
this claim appears in no entry of `papers/Claims-and-Falsifiers-Summary.md`. That is a statement
about the claim's status, not a strength. This is an **exact algebraic result about the model**, and
it should be cited as one.

## 10. Still open

- **3D BCC analog.** The derivation is for the 2D-square dispersion. Since BCC is the canonical
  lattice (D1) and the square lattice is explicitly a *reference implementation, not canonical*,
  **the currently derived result applies to a non-canonical geometry.** The BCC form uses
  $\omega=\arccos(n(c_xc_yc_z\pm s_xs_ys_z))$; the same implicit-function method applies, only
  $\omega''(0)$ changes and it acquires a $\hat k$-dependent piece. Finding 13's $\sim10\times$ larger
  numerical coefficient already indicates the difference. This is the clean, high-value follow-up —
  and it is the only route by which this result becomes falsifiable.
- **Uniformity in $m$.** The $\mathcal O(\beta^{10})$ remainder is not uniform: $\varepsilon_\text{LV}$
  runs from $-1.3\times10^{-4}$ at $m=0.05$ to $-1.92$ at $m=0.9$, so a fixed-$\beta$ truncation
  degrades sharply toward $m\to1$.
- **Prior art unresolved.** The dispersion is the standard Bisio–D'Ariano–Perinotti–Tosini Dirac QCA
  one and its distorted-Lorentz phenomenology is published; whether *this closed form* is already in
  the literature was not established (arXiv fetches timed out during the 2026-08-03 review). No
  novelty is claimed here — but two reference summaries do claim priority against t'Hooft and against
  the SR literature, and those should be checked before either is used externally.
- **Whether $R$ is the right observable at all** (§1). A derivation that $\omega-kv_g$ is the rate of
  a moving clock — rather than one defensible choice among several — would upgrade this from an
  identity about a definition to a statement about lattice physics.
