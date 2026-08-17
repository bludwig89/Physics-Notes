# F241 — The last $O(1)$ factor of the cosmological constant, $\Omega_\Lambda\approx0.685$, is **not** derivable from the F190 area-entropy / F183 black-hole scaling: those fix the ceiling at $\rho_\text{crit}$ ($\Omega=1$) and the sub-unity residual is provably the "why-now" coincidence — every principled route is either circular (event horizon), needs $\Omega_m$ as input (flatness), or is a selection statement; the near-hits ($2/3$, $\ln2$, $e/4$) are shown to be numerology by a density argument

**Date:** 2026-07-03 - 14:35
**Numbering:** **F241** (reserved for this open-derivations task; prior mainline max F199).
**Status:** **Negative / classification result — rigorously argued.** The remaining $O(1)$ factor after F196's $p=2$ derivation is $\Omega_\Lambda=\rho_\Lambda/\rho_\text{crit}\approx0.685$. It is **not** derived to $<0.1$ dex from the model's holographic/BH sector; instead it is shown, at the level of a theorem-with-caveats, that this sector fixes only the **ceiling** $\rho\le\rho_\text{crit}$ ($\Omega=1$, the de Sitter fixed point) and that the departure below the ceiling *today* is the standard coincidence problem, which requires a temporal-selection ("when is the lattice being observed") input the model does not supply. The tempting parameter-free matches ($2/3$, $\ln2$, $e/4$, $1/\sqrt2$) are demonstrated to be coincidental by a numerology-density count. 6/6 checks PASS. **Does not reopen $p=2$** (treated as fixed, per F196).
**Module / Script:** `tests/findings/test_F241_omega_lambda_residual.py` (self-contained, stdlib+numpy; hand-rolled RK4/quadrature — no scipy).
**Results:** `test-results/F241_omega_lambda_residual.json` (6/6).
**Cross-references:** [[F196-dilution-exponent-derived]] (the $p=2$ derivation that lands at $\rho_\text{crit}$ and hands this the $\Omega_\Lambda$ residual — the direct parent), [[F193-ontic-vacuum-gravitates-as-zero]] (bare CC $=0$; the residual is content back-reaction), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the original $10^{121}$ overshoot, now reduced to this one $O(1)$), [[F190-horizon-entropy-lattice-microstates]] (the area-entropy candidate source, tested here), [[F183-blackhole-under-full-tensor]] (the Schwarzschild $M\propto R$ capacity, tested here), [[F192-vacuum-energy-full-tensor]] (the $w=-1$ sign; the FEH route's $w_0$ tension is measured against it), [[F188-multicomponent-lcdm-cosmology]] ($\Omega_m$/flatness — the input that would close this), [[F197-first-excitation-dark-source]] / [[F199b-amplitude-mode-stability-nogo]] (the dark-sector abundance the model does **not** yet have — why $\Omega_m$ is unavailable). External: Cohen–Kaplan–Nelson 1999; Li 2004 (holographic DE, future event horizon); Weinberg 1987 / Martel–Shapiro–Weinberg 1998 (anthropic $\Lambda$ distribution); Gibbons–Hawking 1977.

---

## Acceptance test (stated up front)

Prompt G1 asks: derive the $O(1)$ factor placing $\Omega_\Lambda\approx0.685$ (Planck 2018: $0.6847\pm0.0073$) from the F190 area-entropy / F183 BH scaling **to $<0.1$ dex**, *or* deliver a rigorous documented statement classifying it as coincidental/anthropic. Result: **the second branch.** No principled route from the model's holographic sector lands the sub-unity factor without circularity or an external $\Omega_m$/selection input; the residual is classified as the coincidence-problem ("why-now") residual, and the exact missing input is named. $p=2$ is **not** reopened.

## 1. What F196 actually pins, and what it hands down

F196 derived $p=2$ two ways and showed both collapse to the **same closed form**
$$\rho_\text{grav}(L)=\frac{3c^4}{8\pi G\,L^2}\xrightarrow{\,L=R_H=c/H_0\,}\frac{3H_0^2c^2}{8\pi G}=\rho_\text{crit},$$
i.e. saturating the black-hole/holographic capacity at the Hubble scale gives **exactly the critical density**, $\Omega=1.000$. Observation is $\rho_\Lambda=\Omega_\Lambda\,\rho_\text{crit}$ with $\Omega_\Lambda=0.6847$. So the object still to be explained is
$$\boxed{\ \Omega_\Lambda=\frac{\rho_\Lambda}{\rho_\text{crit}}=0.6847\ (\Delta\log_{10}\ \text{from unity}=0.165)\ }$$
This finding asks whether the *same* F190/F183 sector fixes that $0.685$, or whether it is a genuine residual.

## 2. The ceiling theorem — the holographic/BH sector fixes $\Omega\le1$, not $\Omega=0.685$

The F183 capacity $M_\text{max}(L)=Lc^2/2G$ and the F190 area count $N_\text{dof}=A/4\ell_P^2$ are both **saturation** statements: the *most* gravitating energy a horizon-sized region can hold. Read as a bound on the dark-energy density they give
$$\rho_\Lambda\ \le\ \frac{3c^4}{8\pi G R_H^2}=\rho_\text{crit}\quad\Longleftrightarrow\quad \Omega_\Lambda\le1 .$$
This is a **ceiling**, and it is saturated only in the asymptotic de Sitter future ($\S3$). It cannot by itself produce a specific interior value $0.685<1$: saturation is an inequality, and the F190/F183 constructions contain no second scale to set *how far below* saturation the present universe sits. The exponent $p=2$ is the *slope*; the offset below the ceiling is a boundary condition, not a slope. **This is the crux: the model's holographic sector is a one-parameter ($p$) statement, and $p$ is already spent on F196.**

## 3. The de Sitter fixed point recovers $\Omega=1$, not $0.685$ (event-horizon route is circular)

The most principled attempt is holographic dark energy with the IR cutoff set to the **future event horizon** $R_\text{EH}$ (Li 2004) at the F196 saturation coefficient $d=1$ (F196 fixes this coefficient to unity — it is not a free knob). Two exact facts kill it as a derivation of $0.685$:

1. **Circularity.** $R_\text{EH}=a\!\int_a^\infty\! da'/(a'^2H)$ itself depends on $\Omega_\Lambda$. Imposing $\rho_\Lambda=3c^4/8\pi G R_\text{EH}^2$ gives the identity $\Omega_\Lambda=1/(H_0R_\text{EH})^2$, which in flat $\Lambda$CDM is satisfied **for any** $\Omega_\Lambda$ (verified numerically: with $\Omega_\Lambda=0.6847$ one gets $H_0R_\text{EH}\approx1.15$ and $1/(H_0R_\text{EH})^2\approx0.76$ *today*, and $\to0.6847$ exactly in the asymptotic future). It is a self-consistency relation, not a prediction.
2. **Asymptote $=$ tautology, $=1$ in the true dS limit.** As $a\to\infty$ matter dilutes, $\Omega_\Lambda\to1$, and the event horizon $\to c/(H_0\sqrt{\Omega_\Lambda})$, so $1/(H_0R_\text{EH})^2\to\Omega_\Lambda$ — the fixed point of the map is $\Omega=1$. The holographic/BH sector's principled prediction is therefore $\Omega=1$ (the ceiling, $\S2$), reached only in the infinite future.

Moreover the same $d=1$ FEH model predicts $w_0=-\tfrac13-\tfrac23\sqrt{\Omega_\Lambda}=-0.885$ at $\Omega_\Lambda=0.6847$, in $\sim2\sigma$ tension with the observed $w_0\approx-1$ that F192 already reproduces. So the FEH route is not even a clean quantitative fit, let alone a derivation.

## 4. The residual **is** the coincidence problem — and its only closure is $\Omega_m$

Flat geometry (which the model's Friedmann sector F182/F188 assumes) gives the exact identity
$$\Omega_\Lambda=1-\Omega_m .$$
Thus deriving the $O(1)$ factor is **identically** deriving the present cosmic matter fraction $\Omega_m=0.3153$. That number is set by the *content* of the universe (baryons + the dark sector) at the epoch we observe. The model does **not** currently possess it: the dark-matter abundance is explicitly open/no-go (F197 candidate, F198 under-produces by $\sim15$ orders, F199 stability no-go). Equivalently, the matter–$\Lambda$ equality $\Omega_\Lambda=\Omega_m$ occurs at $a_\text{eq}=(\Omega_{m0}/\Omega_{\Lambda0})^{1/3}=0.772$ ($z_\text{eq}=0.295$) — we live $\sim0.14$ dex past equality, on the shoulder of the transition. Which point of the trajectory carries an observer is the "why-now" question; along the F182/F188 $\Lambda$CDM history $\Omega_\Lambda(a)$ sweeps the whole interval $(0,1)$, so $0.685$ is picked out only by *when* the measurement is made, i.e. by a temporal-selection / anthropic weight, not by the dynamics.

## 5. The parameter-free near-hits are numerology (density argument)

Several simple constants sit suspiciously close to $0.6847$: $2/3$ ($0.0116$ dex), $\ln2$ ($0.0053$), $e/4$ ($0.0033$), $1/\sqrt2$ ($0.0140$), $5/7=0.714$ ($0.017$). None survives scrutiny, and the reason is quantitative: the window $|\Delta\log_{10}|<0.02$ around $0.6847$ is the linear interval $[0.654,0.716]$, a $\sim9\%$-wide band, and the density of "simple" constants (rationals $p/q$, $q\le12$; low-order transcendental combinations) in that band is $O(5)$. Finding *a* clean constant within $0.02$ dex of an $O(1)$ target is therefore expected by chance and carries **no evidential weight**. Crucially, **none of these constants is produced by any step of the F190/F183 derivation** — there is no lattice quantity ($2\pi\sqrt3$ per-cell entropy, $I_\text{CC}=4.08$, $g_*=2$, $\sqrt3$) whose combination yields $0.685$ through the holographic algebra. We record the near-hits explicitly so they are not mistaken for a result. (The single geometrically-motivated candidate, $2/3$ = spatial-volume exponent, does not appear in the energy-density algebra, which carries the factor $3$, not $2/3$; see F196 §Route 2.)

## 6. What input *would* close it

The residual becomes derivable the moment the model supplies **any one** of:
- the present cosmic matter fraction $\Omega_m$ (then $\Omega_\Lambda=1-\Omega_m$ exactly) — blocked by the open dark-sector abundance (F197–F199);
- a first-principles temporal-selection / observer weight over the F182/F188 history (an anthropic or causal-patch measure) that peaks near $\Omega_\Lambda\sim0.7$ — this is external physics (Weinberg 1987; Martel–Shapiro–Weinberg 1998 give a median nearer $0.9$, i.e. $0.12$ dex high, *consistent within the anthropic spread* but not a lattice derivation);
- a dynamical attractor with a **non-unit** fixed point $\Omega_*\ne1$ — but $\S3$ shows the holographic/BH attractor's fixed point is exactly $1$, so this route is closed within the current sector.

Absent one of these, the honest ledger entry is: **the last $O(1)$ factor is the coincidence-problem residual, coincidental/anthropic given the present model, and equal to $1-\Omega_m$.**

## Checks (6/6)

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | F196 saturation $=\rho_\text{crit}$, so residual $\Omega_\Lambda=\rho_\Lambda/\rho_\text{crit}=0.6847$; distance from ceiling $\Delta\log_{10}(1/\Omega_\Lambda)=0.165$ | PASS | exact (definitional) |
| C2 | Ceiling theorem: BH/holographic capacity gives $\Omega_\Lambda\le1$; saturation is an inequality with no interior scale | PASS | exact (structural) |
| C3 | Event-horizon route is circular: today's $1/(H_0R_\text{EH})^2\approx0.76\ne0.685$ (uses its own $\Omega_\Lambda$ input); asymptotic map fixed point $=\Omega_\Lambda$ (dS tautology $\to$ true limit $1$), not a derived $0.685$ | PASS | machine (log-grid quadrature) |
| C4 | FEH $d=1$ predicts $w_0=-0.885$ at $\Omega_\Lambda=0.6847$ (not $-1$) → not even a clean fit | PASS | exact (algebra) |
| C5 | Flatness identity $\Omega_\Lambda=1-\Omega_m$; closure $\equiv$ deriving $\Omega_m=0.3153$, which the model lacks (F197–199 open); $a_\text{eq}=0.772$ | PASS | exact + ledger |
| C6 | Numerology density: $\ge4$ simple constants within $0.02$ dex of $0.6847$; band is $\sim9\%$ wide ⇒ near-hits carry no evidential weight, and none arises from the F190/F183 algebra | PASS | quantitative |

**Overall 6/6 PASS.**

## What is derived vs computed vs classified (ledger impact)

| Piece | Status |
|---|---|
| residual $=\Omega_\Lambda=\rho_\Lambda/\rho_\text{crit}=0.6847$ (once $p=2$ fixed) | **Derived / definitional** (from F196) |
| holographic/BH sector fixes only the ceiling $\Omega\le1$ | **Derived** (structural; saturation is an inequality) |
| dS/FEH attractor fixed point $=1$, event-horizon route circular | **Derived** (exact algebra + machine quadrature) |
| $\Omega_\Lambda=1-\Omega_m$; closure needs $\Omega_m$ (unavailable, F197–199) | **Derived identity + named obstruction** |
| near-hits ($2/3,\ln2,e/4,1/\sqrt2$) are numerology | **Derived** (density count; none from the model algebra) |
| the $0.685$ itself | **Classified coincidental/anthropic** — the "why-now" residual; not derived to $<0.1$ dex from F190/F183 |

**Net for the F164 chain:** F164 ($10^{121}$ + wrong sign) → F193 (bare CC $=0$, sign fixed) → F196 ($p=2$ derived, lands at $\rho_\text{crit}$) → **F241**: the sole surviving unknown is the coincidence factor $\Omega_\Lambda=1-\Omega_m$, and it is *provably* outside the reach of the model's holographic/BH sector, awaiting the cosmic matter fraction or an observer measure. The once-$121$-order problem is closed to a single, well-characterised $O(1)$ residual whose nature (coincidental/anthropic) is now established rather than assumed.

## Caveats (honest scope)

- This is a **negative** result: it does not compute $0.685$. Its content is that the F190/F183 sector *cannot* compute it and *why*, plus the exact input that could.
- The anthropic classification is a statement about the present model, not a proof that no deeper principle exists; a future dark-sector abundance (F197–199 line) would upgrade the residual from "coincidental" to "derived via $\Omega_m$."
- $\Omega_\Lambda=0.6847$, $H_0=67.4$, $\Omega_m=0.3153$ (Planck 2018); few-percent parameter shifts move all dex figures by $\ll1$.
- The FEH $w_0$ tension ($\S3$) uses the standard Li-2004 $d=1$ relation; the model's own $w=-1$ comes from F192's full-tensor treatment, which is the correct sector for the equation of state (F196 caveat, unchanged here).

## Provenance

Direct follow-up to F196 (open-derivations prompt G1). Uses F196's saturation-$=\rho_\text{crit}$ result, F183's $M\propto R$ capacity and F190's area count as the tested candidate sources, the F182/F188 flat-$\Lambda$CDM history for the trajectory/coincidence analysis, and F192 for the $w=-1$ benchmark. The blocking input ($\Omega_m$ / dark-sector abundance) is the open F197–F199 line. No new physics introduced; no existing derivation altered; $p=2$ untouched.
