# Finding 22 — QCA Velocity Addition: Exact Deformed Formula from the Arccos Dispersion

> **[PARTIALLY SUPERSEDED 2026-08-04 by F15 — ledger S19-F22-velocity-addition-review-retraction]**
>
> **DEAD:** Claim 1, that the linear SR boost of (omega,k) preserves the arccos mass shell -- false at leading order in v. And claim 3, the 'deformed velocity-addition formula' -- the composition is ordinary Einstein addition in the nonlinear variables, and the headline third-order form misses the real first-order deviation by 10^2-10^3x.
>
> **STILL LIVE:** Claim 2, rho(m) = tan(theta)/theta = 1 - 2 beta_LV, confirmed independently at sympy zero; the corrected statement that on the 2D-square k_y = 0 axis the boost does NOT preserve the shell, with the O(vk) coefficient measured; and the prior art now cited (arXiv:1310.6760, arXiv:1503.01017).
>
> **NOTE:** Retracting claims 1 and 3 from the PUBLIC headline, and rewriting exactness-inventory rows 45/46/47, were escalated by the remediation and are tracked as claim-layer work (D12), not as edits to this finding. The finding is a record of what a session concluded and is not rewritten.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-05-22  
**Status:** Confirmed — Tier 1 algebraic (sympy bit-zero) + Tier 2 machine-precision numerical  
**Reviewed:** 2026-08-04 — **OVERSTATED** ([independent review](../docs/reviews/F22-review-2026-08-04.md))  
**Remediated:** 2026-08-04 — 9 applied · 1 partial · 1 deferred · 2 escalated ([remediation](../docs/reviews/F22-remediation-2026-08-04.md))  
**Source:** `casim.engine.interactions.derive_velocity_addition` (extension of Finding 15). Records: `F22-rho-identity-and-offshell` (gate). Result: `test-results/F22_rho_identity_and_offshell.json`.
**Scope:** 2D-square lattice, $k_y = 0$ axis, $c_\text{lat} = 1/\sqrt2$. **Not** the canonical BCC lattice ($c_\text{lat} = 1/\sqrt3$), where F13 records a $\sim10\times$ larger coefficient and where no analogue of the construction below has been attempted.

---

## Summary

Starting from the exact 2D-square QCA Dirac dispersion

$$\omega(k) = \arccos\!\bigl(\sqrt{1-m^2}\,\cos(k/\sqrt{2})\bigr), \quad c_\text{lat} = 1/\sqrt{2},$$

we derive algebraically that:

1. ~~The **SR Lorentz boost acts exactly on the QCA 4-momentum** $(\omega, k)$.~~
   **FALSE** (review 2026-08-04). The boost fails at first order in $v$:
   $$\frac{\omega' - \omega(k')}{v\,k}\bigg|_{k\to0} = \frac1\rho - 1 = \frac{2\beta_\text{LV}}{1-2\beta_\text{LV}},$$
   measured $-0.0930513$ against a predicted $-0.0931003$ at $m=0.5$ (rel.
   $5.3\times10^{-4}$), and $-0.03105/-0.20732/-0.58071$ at $m=0.3/0.7/0.95$. At a
   finite boost it is a **7.1%** error in $\omega$ at $m=0.7,\ k=1.0,\ v=0.3$.
   Structurally it cannot hold: on the shell $\omega$ is bounded in
   $[\theta,\pi-\theta]$ and periodic in $k$, while boost orbits are unbounded
   hyperbolae. What *is* exact is stated under `## Corrections`.
2. The 4-momentum velocity $u_p = k c_\text{lat}^2/\omega = k/(2\omega)$ satisfies $u_p = \rho(m)\,u_g$ at $k \to 0$, where
$$\rho(m) = \frac{m}{\sqrt{1-m^2}\,\arcsin m} = 1 - 2\beta_\text{LV}(m).$$
   **This survives** and was independently re-derived at sympy zero. It is the one
   genuine result here. Note it is a $k\to0$ **limit**: at finite $k$ it runs
   ($m=0.5$: 1.1027 at $k=0$, 1.1547 at the BZ edge, divergent there), and $u_p$
   itself is **superluminal for $ka>\pi/2$**, so $u_p$ is not a signal velocity.
   Equivalently $\rho = c_\text{lat}^2/(v_\text{ph}v_g)$ — $\rho$ *is* the failure
   of the relativistic identity $v_\text{ph}v_g = c^2$.
3. ~~This yields a **closed-form deformed velocity-addition formula**~~ **MISNOMER**
   (review 2026-08-04). The formula below is retained as the record of what was
   claimed; it does not describe the lattice.
$$u'_\text{QCA} = \frac{u_g + v_g}{1 + 2\rho^2(m)\,u_g v_g}$$
with deviation from SR
$$\delta u' = \frac{2(1-\rho^2)\,u\,v\,(u+v)}{(1+2\rho^2 u v)(1+2uv)} \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v).$$

Since $\beta_\text{LV}(m) < 0$ for all $m \in (0,1)$, the QCA **always predicts less velocity addition than SR at finite mass**, consistent with the time-dilation over-dilation in Finding 15.

---

## Derivation

### Step 1 — The ρ ratio

Expanding $\omega(K)$ with $K = k/\sqrt{2}$ at $K \to 0$:

$$\omega \approx \arcsin m + \frac{\sqrt{1-m^2}}{2m}\,K^2 + O(K^4)$$

The group velocity is $u_g = d\omega/dk = (1/\sqrt{2})\,d\omega/dK$; at $K \to 0$:

$$u_g \approx \frac{\sqrt{1-m^2}}{m}\,k/2 \quad (\text{leading term in }k)$$

The 4-momentum velocity is $u_p = k/(2\omega) \approx k/(2\arcsin m)$ at $k \to 0$.  Therefore

$$\rho \equiv \lim_{k\to 0}\frac{u_p}{u_g} = \frac{m/\arcsin m}{\sqrt{1-m^2}} = \frac{m}{\sqrt{1-m^2}\,\arcsin m}.$$

Confirmed symbolically via sympy with residual = **0** (bit-exact).

### Step 2 — Deformed velocity-addition formula

The SR Lorentz boost $(v_\text{frame})$ maps the 4-momentum as

$$k' = \gamma(k - 2v\,\omega), \quad \omega' = \gamma(\omega - v\,k), \quad \gamma = (1-2v^2)^{-1/2}.$$

Since $u_p = \rho\,u_g$, both $u_p$ and $v_p = \rho\,v_g$ obey SR velocity addition exactly:

$$u'_p = \frac{u_p + v_p}{1 + 2\,u_p\,v_p} = \frac{\rho(u+v)}{1 + 2\rho^2 uv}.$$

Converting back to group velocity via $u'_g = u'_p/\rho$ yields the deformed formula.

### Step 3 — LV deviation

$$\delta u' = u'_\text{QCA} - u'_\text{SR} = \frac{2(1-\rho^2)\,u\,v\,(u+v)}{(1+2\rho^2 uv)(1+2uv)}.$$

Confirmed symbolically (sympy residual = **0**). Leading-order expansion:

$$2(1-\rho^2) = 2(1-\rho)(1+\rho) \approx -4\beta_\text{LV}(m)\cdot 2 = 8\beta_\text{LV}(m) \quad (\rho \approx 1 \text{ at small }m)$$

$$\Rightarrow \delta u' \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v), \quad \beta_\text{LV}(m) \approx -\frac{m^2}{6} \text{ for small }m.$$

---

## Key results

| Result | Status |
|---|---|
| $\rho(m) = m/(\sqrt{1-m^2}\arcsin m) = 1-2\beta_\text{LV}(m)$ — sympy zero | **Tier 1 exact** |
| $\delta u'$ closed form — sympy zero residual | **Tier 1 exact** |
| Massless limit $m\to 0$ ($\rho\to 1$): $\delta u' = 0$ — SR recovered | **Tier 1 exact** |
| $\rho$ formula vs numerical $u_p/u_g$ at $k=10^{-6}$, max residual $3.4\times 10^{-14}$ across $m \in [0.05,0.90]$ | **Tier 2 machine precision** |
| $8\beta_\text{LV} \approx -4m^2/3$ (leading small-$m$ approximation) | **Tier 1 exact (symbolic)** |

---

## Numerical summary

**Step 2 — Deformed formula scan (algebraic):**

| $m$ | $u$ | $v$ | $u'_\text{QCA}$ | $u'_\text{SR}$ | $\delta u'$ | rel(lead) |
|---|---|---|---|---|---|---|
| 0.10 | 0.01 | 0.01 | 0.0199960 | 0.0199960 | $-2.69\times 10^{-8}$ | 1.3e-3 |
| 0.10 | 0.10 | 0.05 | 0.1485050 | 0.1485149 | $-9.89\times 10^{-6}$ | 1.8e-2 |
| 0.50 | 0.10 | 0.10 | 0.1952520 | 0.1960784 | $-8.26\times 10^{-4}$ | 6.2e-3 |

**Step 3 — Continuum-limit ρ check:**

| $m$ | $\rho_\text{analytic}$ | $u_p/u_g$ (num.) | residual |
|---|---|---|---|
| 0.05 | 1.0008348643 | 1.0008348643 | 2.2e-16 |
| 0.50 | 1.1026577908 | 1.1026577908 | 6.6e-15 |
| 0.90 | 1.8438987463 | 1.8438987463 | 3.4e-14 |

**Step 4 — Group-velocity boost structure at finite k:**

At fixed $v_2 = 0.001$ and $m = 0.10$, the total deviation of the lattice QCA boost from SR is:

$$d_\text{qca} = v_g^\text{boost} - u'_\text{SR} \approx v_2\!\left(1 - \frac{1}{\rho(m)}\right) \approx v_2\cdot(-2\beta_\text{LV}) = 3.35\times 10^{-6}$$

This is **k-independent at small k** — it is not a finite-k effect but the fundamental LV mismatch between the lattice group velocity and the SR-transformed group velocity. The correct SR-compatible kinematic observable is the 4-momentum velocity $u_p$, not the group velocity $u_g$.

---

## Physical interpretation

The group velocity $u_g = d\omega/dk$ does not transform as a relativistic velocity under Lorentz boosts of the 4-momentum. The lattice 4-momentum velocity $u_p = k c_\text{lat}^2/\omega$ does. Their ratio $\rho(m) \ne 1$ for $m > 0$ is the same coefficient that produces the SR-2 time-dilation LV term (Finding 15).

This is not a failure of the QCA's Lorentz structure — it is a consequence of the massive dispersion being nonlinear. In the massless limit ($m \to 0$, $\rho \to 1$) SR is recovered exactly. At finite mass, the deformed formula $u'_\text{QCA} = (u+v)/(1+2\rho^2 uv)$ is the lattice-exact analogue of SR velocity addition for group velocities.

---

## Connections

- **Finding 15**: $\beta_\text{LV}(m) = \tfrac12(1-\rho(m))$ — same coefficient appears in SR-2 time-dilation gap and here in velocity addition.
- **Small-$m$ expansion**: $8\beta_\text{LV} \approx -4m^2/3$; velocity-addition LV coefficient $= -4m^2/3$ to leading order.
- **Script**: `ca-simulation/derive_velocity_addition.py` — Steps 1–5 all pass, run in < 30 s.

---

## Prior art

Added 2026-08-04 (review attack 11). The structure in this finding is published for
the Dirac QCA and was not cited:

- A. Bibeau-Delisle, A. Bisio, G. M. D'Ariano, P. Perinotti, A. Tosini,
  *Doubly special relativity from quantum cellular automata*, **EPL 101**, 60005
  (2013) — [arXiv:1310.6760](https://arxiv.org/abs/1310.6760).
- A. Bisio, G. M. D'Ariano, P. Perinotti, *Quantum walks, deformed relativity and
  Hopf algebra symmetries*, **Phil. Trans. R. Soc. A 374** (2016) —
  [arXiv:1503.01017](https://arxiv.org/abs/1503.01017).

"Derived here" survives — the algebra in this file is the session's own. **"Novel"
does not.** The published nonlinear-representation result is moreover precisely the
correct repair of claim 1: the boost is realised nonlinearly, not linearly on
$(\omega,k)$.

## Corrections

**2026-08-04 - 09:10** — per [independent review 2026-08-04](../docs/reviews/F22-review-2026-08-04.md),
verdict **OVERSTATED** (1 PASS · 2 WEAKENS · 10 FAIL).

| Was | Now | Why | Attack |
|---|---|---|---|
| "The SR Lorentz boost acts **exactly** on the QCA 4-momentum $(\omega,k)$" | **False.** Fails at $O(vk)$ with coefficient $1/\rho-1$; measured $-0.0930513$ vs predicted $-0.0931003$ at $m{=}0.5$ | The level set of the arccos dispersion is not preserved by a linear boost. The finding's own Step 4 already reported this as "the fundamental LV mismatch" | 10 |
| "closed-form **deformed** velocity-addition formula" | **Misnomer.** In the variables where the boost is exact, composition is **undeformed** Einstein addition | $E=\sin\omega$, $P=n\sin(ka)/a$ give $E^2-c^2P^2=m^2$ identically and $u_g = c^2P/E$ exactly, so $\eta_3 = \eta_1+\eta_2$ (verified to $5.6\times10^{-17}$) | 10 |
| $\delta u' \approx 8\beta_\text{LV}uv(u+v)$ as the leading deviation | The real leading deviation is **first order in $v$**, $v(1-1/\rho)$ | F22's formula misses the lattice's boost response by $10^2$–$10^3\times$ (103× at $m{=}0.1$, 3251× at $m{=}0.5$, $k{=}0.01$) | 10 |
| "sympy bit-zero" verification of $\rho = 1-2\beta_\text{LV}$ | Rewritten so it can fail, plus an asserted negative control | The old check wrote `beta_LV_sym = (1−rho)/2` then verified `rho − (1−2·beta_LV_sym)` — a tautology. A deliberately wrong $\rho = m/\arcsin m$, and $\rho = 42$, both returned **0** | 1, 4 |
| no test record for the module | `F22-rho-identity-and-offshell`, gate tier, `expect.exactness: exact`; module promoted `dead_candidate → live` in `_SPINE` with `findings=(F15,F22)` | The sole F22-tagged record ran continuum-SR Doppler on a *massless* kernel and was **bit-identical at $m=0.3/0.7/0.95$** | 7, 8 |
| no scope qualifier | "2D-square, $k_y=0$, $c_\text{lat}=1/\sqrt2$" in the header | The canonical lattice is BCC; the module docstring said 2D but the title, summary and `project-status.md` dropped it | 12 |
| no prior art | `## Prior art` | Published as DSR-from-QCA in 2013 and 2016 | 11 |
| $\rho$ presented without domain caveats | $\rho$ runs at finite $k$; $u_p$ superluminal for $ka>\pi/2$; $\rho\to\infty$ as $m\to1$ | All three unstated | 12 |
| `ca-simulation/derive_velocity_addition.py` | `casim.engine.interactions.derive_velocity_addition` | Pre-C9 path | 9 |

**What *is* exact, and is the correct replacement for claim 1.** With
$E \equiv \sin\omega$ and $P \equiv n\sin(ka)/a$,

$$E^2 - c_\text{lat}^2P^2 = m^2 \quad\text{identically},\qquad
u_g \equiv \frac{d\omega}{dk} = \frac{c_\text{lat}^2P}{E}\ \text{exactly at all }k,$$

with $E = m\cosh\eta$, $aP = m\sinh\eta$, $u_g = c_\text{lat}\tanh\eta$. The boost is
exact in **these** variables — a nonlinear, DSR-type realisation. Two caveats that
must travel with it: the action is only **partial** ($\sin\omega\le1$ forces
$m\gamma\le1$, i.e. $\lvert\beta\rvert<n$; beyond that a boost maps onto no lattice
mode), and $\omega\mapsto\sin\omega$ is 2-to-1 across the BZ so the lift back to $k$
is ambiguous. The accessible domain is also **not closed** under composition:
$m=0.4$, $k=1.1$, $v=-0.4$ gives $\lvert u_g'\rvert = 0.6758 > n\,c_\text{lat} = 0.6481$.
And $c_\text{lat}$ is the invariant asymptote but is *not attainable* — the real
ceiling is $\beta_\max = \sqrt{1-m^2}$, which is $m$-dependent and hence not invariant.

**Confirmed unchanged.** $\rho(m) = \tan\theta/\theta = 1-2\beta_\text{LV}$ was
re-derived independently, from F15's *definition* rather than its stated closed
form, at sympy zero — together with $\gamma_\text{LV} = \tfrac18 - \tfrac1\theta(\tfrac T8+\tfrac{T^3}{24})$
as a free cross-check. The free-input count is also correct: **one** ($m$), zero
fitted; $a = c_\text{lat}$ cancels identically because $\omega$ depends on $k$ only
through $u = ka$. Attack 5 passed — $\rho$ is forced by the dispersion, not fitted,
with no look-elsewhere freedom.

**Rejected.** None. Every recommendation was either applied or escalated.

## Falsifiability

Added 2026-08-04 (attack 13 was empty). Thresholds, and an honest statement of why
they are not currently testable:

| Statement | Killed by |
|---|---|
| $\rho(m) = \tan(\arcsin m)/\arcsin m$ | any $m\in(0,1)$ where $\lim_{k\to0}u_p/u_g$ differs from it |
| Off-shell coefficient $=1/\rho-1$ | a measured $\Delta/(vk)\vert_{k\to0}$ differing from it on the 2D-square walk |
| Undeformed Einstein composition in $(E,P)$ | any $(m,k,v)$ inside $\lvert\beta\rvert<n$ where $\eta_3\neq\eta_1+\eta_2$ |

**Experimentally, this sector is currently untestable, and that should be said
plainly.** The effect vanishes for photons ($\rho\to1$ as $m\to0$), so the strong
astrophysical LIV bounds — e.g. Vasileiou et al. 2013, GRB $n=2$ at
$1.3\times10^{11}$ GeV — are structurally inapplicable. In the massive sector, at
$m_\text{lat} = m_e c a/\hbar \approx 2.76\times10^{-22}$, the coefficient
$8\beta_\text{LV} \approx -1.0\times10^{-43}$ sits about $5\times10^{-41}$ of the
sensitivity of muon time dilation (Bailey et al. 1977, $2\times10^{-3}$).

## Status

Claim 2 **live** with a gate record. Claims 1 and 3 **flagged false / misnamed**
above; their formal retraction from the headline is **escalated to Ben**, together
with the disposition of exactness-inventory rows 45–47 (rows 46 and 47 are
identities whose checked expressions never touch the dispersion — row 46's
`free_symbols` is $\{u,v,\rho\}$).

Open: whether any of this survives off the $k_y=0$ axis, or on the canonical BCC
lattice. The BCC form $\omega = \arccos(n(c_xc_yc_z\pm s_xs_ys_z))$ has no obvious
analogue of $\sin^2\omega - n^2\sin^2u = m^2$, and no code path exists.
