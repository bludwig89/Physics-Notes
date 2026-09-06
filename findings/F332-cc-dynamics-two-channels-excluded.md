# F332 — Is the F164 zero-point sum dynamically driven to respect the F183/F190 capacity ceiling, or is it not? Two concrete channels tested and both **closed**: F164 channel (ii) (AB≡1 sequestering) has no hook into a homogeneous source at all, and a literal F130 block-spin coarse-graining of the F59/F164 heat-kernel moments is excluded by 35+ orders beyond the CODATA $G$ budget — worse than F319 U8's own exclusion, because $a_0$ falls while $a_1$ simultaneously rises. The surviving F193§B/F196/F241 ceiling route is shown to be the model's own Friedmann-I law, not an import, and is left untouched and still undynamicised

**Date:** 2026-08-28 - 19:10
**Numbering:** **F332**, taken as `NEXT FREE NUMBER` (max was F331).
**Status:** **Negative / classification result on two named channels, plus one clarifying structural identity.** 5/5 checks PASS, 2/2 declared controls verified red-and-only-there. K1 is **exact** (algebraic identity, residual $0.0$) plus a **machine**-precision self-consistent solve; K2 is **exact** (Fredholm/DC-mode argument, residual $0.0$ vs $1.0$) plus a **structural** citation of F178's already-adopted scope restriction; K3 is **machine** (fitted exponents $-0.999989/+0.999991$ against $-1/+1$); K4 is **quantitative** (a computed excess of $35.15$ orders of magnitude). Does **not** derive $\Omega_\Lambda$, does **not** exhibit F319 U8's required $\ge1.27\times10^{116}$ order-selective mechanism, and does **not** reopen $p=2$ (F196) or CL275 (F311/F319's uniform-$\lambda$ exclusion).
**Checked:** 2026-08-28 - 19:00 -- 10 PASS / 4 WEAKENS / 0 FAIL / 0 NOT RUN -- **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/interactions/cosmology_lambda_dynamics.py`
**Registry record:** `F332-cc-dynamics` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, 2 controls verified)
**Results:** `test-results/F332_cc_dynamics.json`
**Claim:** none — internal-mechanism check, not an extension/contradiction of QM/SM/GR/SR (`docs/claims/README.md` "standing rule"). K1's ceiling=Friedmann-I identity and K2/K3/K4's channel exclusions are all internal to the model's own construction, not a tested claim against external physics; the residual this leaves (F193§B/F196/F241's ceiling, still undynamicised) is already carried by CL212 (F241), which this finding leaves unmoved.
**Addresses:** rubric row **K9**, ledger **G1** (completeness-2026-08-18 Amendment 4's own named next step: *"show that the F164 zero-point sum is made to respect the F183 capacity bound, or show that it is not"*). Also touches rubric **A11** and parameter **#28** (same residual).
**Cross-references:** [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the bare sum and its channel (ii)), [[F193-ontic-vacuum-gravitates-as-zero]] (Part A excluded per CL275; Part B is the surviving ceiling route and its brief note on channel (ii), sharpened here), [[F196-dilution-exponent-derived]] (the ceiling formula, reinterpreted here as Friedmann-I), [[F241-omega-lambda-o1-residual-anthropic]] (the residual this leaves untouched), [[F311-gap5-three-numbers-adjudicated]] (leg C3, withdrawn — not re-opened), [[F319-uv-sector-reconciled-physical-cutoff-and-counterterms]] (U8's 2×2 solve and the $1.27\times10^{116}$ selectivity requirement, used verbatim), [[F178-gravity-full-tensor-adoption]] (the decision restricting $AB\equiv1$ to vacuum regions — the load-bearing citation for K2), [[F182-friedmann-pressure-cosmology]] (Friedmann-I, F182's own equation, shown identical to F196's ceiling), [[F130-blockspin-rg-gauge-gravity]] (the proven blocking transform $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$ this reuses, and T3b's correct — different — treatment of the gravity sector), [[F79-structural-newton-constant]] / [[F59-induced-eh-prefactor-and-f10-selection]] ($G=a^2c^3/(8\pi\sqrt3\hbar)$ and the two Sakharov moments $I_\text{cc}, I_g$). External: Weinberg, *Rev. Mod. Phys.* **61**, 1 (1989) (the adjustment-mechanism no-go theorem); Padilla, "Lectures on the Cosmological Constant Problem", arXiv:1502.05296 (review); Kaloper & Padilla, *Phys. Rev. D* **90**, 103523 (2014) (vacuum-energy sequestering — the literature's own non-local/global evasion of the theorem, cited by analogy, not used).

Raised by the open-derivations G1 ledger's own next step, restated by completeness-2026-08-18 Amendment 4 (2026-08-18 - 17:15): *"show that the F164 zero-point sum is made to respect the F183 capacity bound, or show that it is not — a physics session, in the sector F196 and F241 already built."*

---

## 1. What Amendment 4 left open, precisely

Amendment 4 adjudicated a five-day-old disagreement (F311 vs F319) without running new physics: F193 Part A (bare CC $=0$, "the beable vacuum has zero energy") is **excluded** — CL275 applies to it verbatim, because its "delete the $\tfrac12$-per-mode $c$-number" step is *uniform*: F59 Part C builds $1/16\pi G$ out of the same $\tfrac12$, so the deletion takes $G$ down with it. F311 leg C3 ("$1/G$ *is* the mode sum, so it can't also be a CC source") is **withdrawn** — it proves too much, since $a_0$ (the $\rho_\text{vac}$ moment) and $a_1$ (the $1/G$ moment) are different coefficients of one heat-kernel expansion, not one thing double-counted. F319 §6's "channel (ii) is the sole survivor" is **narrowed** — it enumerated only F164's three original channels and missed F193 Part B/F196/F241's capacity ceiling.

What that leaves standing: **two** candidate channels of the right *shape*, neither closed.

| route | what it needs to do to $a_0$ | what it needs to do to $a_1$ | status before this finding |
|---|---|---|---|
| F164 channel (ii) — $AB\equiv1$ sequestering | remove the constant piece of the source | leave untouched | order-selective *by construction* — **no number** |
| F193 §B/F196/F241 — capacity ceiling | cap at $\rho_\text{crit}(R_H)$ | leave untouched | delivers $120.66$ of the required $120.76$ decades — **the number, no dynamics** |

Amendment 4's own closing line: *"show that the F164 zero-point sum is made to respect the F183 capacity bound, or show that it is not."* This finding runs three concrete, computed checks against exactly these two candidates (plus the ceiling's own origin) and answers: **not, on either of the tested channels** — with the failures themselves informative rather than blank.

## 2. K1 — the ceiling is not an import; the bare source's own self-consistent horizon is sub-lattice-cell

F196 derived $\rho_\text{grav}(L)=3c^4/(8\pi GL^2)$ two ways (Schwarzschild bulk capacity, Bekenstein–Hawking surface count) and both landed on $\rho_\text{crit}$ at $L=R_H$. Neither derivation mentions that this is *also*, trivially, the model's own **Friedmann-I constraint** (F182, the direct FRW reduction of the CLAUDE.md decision-4 induced Einstein equation): $H^2=8\pi G\rho/3c^2$ rearranges to exactly the same formula at $H=c/R_H$. Checked here to the float floor (residual $0.0$) rather than asserted — the "ceiling" the surviving route rests on is the model's own adopted cosmological dynamical law, not an external holographic/BH import bolted on top of it.

That identity licenses a genuine question: solve the *same* Friedmann-I equation self-consistently with F164's **bare** (unsuppressed) zero-point density as the sole source, and ask what horizon it produces. Using $G=a^2c^3/(8\pi\sqrt3\hbar)$ (F79, structural) and $\rho_\text{vac}=g_*\sqrt3\,I_\text{cc}\,\hbar c/a^4$ (F164), the result is a **closed form**:

$$R_H(\rho_\text{vac})=a\sqrt{\frac{3}{g_*I_\text{cc}}}$$

— an exact algebraic identity (both $\rho_\text{vac}$ and $G$ are set by the *same* lattice length $a$, with no other scale in the theory) that a direct numerical Friedmann solve reproduces to machine precision (residual $0.0$). Numerically:

| quantity | value |
|---|---|
| $R_H(\rho_\text{vac,bare})$, closed form | $6.465\times10^{-35}$ m |
| $R_H(\rho_\text{vac,bare})$, direct Friedmann solve | $6.465\times10^{-35}$ m (residual $0.0$) |
| $R_H/a$ | $\mathbf{0.6063}$ |
| $R_{H,0}$ (observed, $H_0=67$ km/s/Mpc) | $1.381\times10^{26}$ m |
| $\log_{10}(R_{H,0}/a)$ | $60.11$ |

**The bare zero-point sum is self-consistently confined to sub-lattice-cell scale by the model's own dynamics.** This is a sharp, model-native, closed-form restatement of the cosmological-constant problem (the bare density, taken seriously as a source, cannot even support a coherent patch as large as the theory's own resolution) — but it is a *diagnosis*, not a suppression: it says the bare sum cannot be a smooth macroscopic source, and it says nothing about why the *observed* universe instead sits at $R_H\sim60$ decades larger with some small residual content. K1 is reported honestly as clarifying, not as new suppression physics.

## 3. K2 — F164 channel (ii) is closed, not merely unevidenced

F164's channel (ii) needs the $F64$ dielectric ($A=1/K,\ B=K,\ AB\equiv1$) to "sequester" a constant vacuum energy from sourcing curvature. Two independent facts, taken together, close it.

**K2a — the static equation is exactly Fredholm-blind to a homogeneous source.** F193's brief note already flagged this qualitatively ("a spatially constant $T^{00}_\text{vac}$ has no normalisable static-dielectric solution"); this finding makes it a computed fact. On a periodic domain, F106's static law $\nabla^2u=-S$ has a $k=0$ Fourier mode with **zero freedom**: for *any* candidate $u$, $\widehat{\nabla^2u}(0)=0$ identically, so the equation's own DC balance is $0=-\widehat S(0)$ — solvable only if the source mean is zero. Solved via FFT on a $48^3$ periodic grid:

| source | DC residual $/\,S_0$ |
|---|---|
| uniform $S=S_0$ (the vacuum-energy case) | $\mathbf{1.000000}$ (fully unabsorbed) |
| the same source with its mean subtracted first (control) | $0.0$ (fully absorbed) |

The homogeneous piece isn't merely unaddressed by this equation — there is *nowhere in the equation* for it to go. This is a completely general fact about the Laplacian on a periodic domain (the Fredholm alternative), not a special property of this lattice; what is new here is confirming it holds for the model's own field equation and connecting it explicitly to channel (ii).

**K2b — and F178 (already adopted) restricts $AB\equiv1$ to exactly the regime that fact excludes.** Decision 4 (CLAUDE.md) and F178 state plainly: *"In vacuum ($T_{\mu\nu}=0$) the impedance lock $AB\equiv1$ ... survive[s] as the weak-field representation ... [i]t is not the field equation inside matter: a single scalar forces anisotropic stress (F173)."* A homogeneous cosmological vacuum-energy density is, by definition, $T_{\mu\nu}\ne0$ *everywhere* — it is always the "interior" case F178 already hands to the full two-function tensor treatment (no $AB\equiv1$ lock at all), never the vacuum case the dielectric represents. So the representation channel (ii) needs is definitionally not in play for a homogeneous source, independent of K2a.

**Verdict: channel (ii) is excluded, for two independent and already-derivable reasons — not "unevidenced," closed.** No new physics is invoked for K2b; it is F178's own scope statement, not previously connected to K9.

## 4. K3/K4 — a literal F130 block-spin reading of the two Sakharov moments, and why it fails

F193's own text named a tool for this class of question: *"a block-spin / F130-style RG statement of how far the excitation back-reaction propagates."* F130 proved the blocking transform $\Omega_\text{coarse}(\kappa)=\Omega(\kappa/b)$ exact (T1, the $c_\text{lat}$ fixed point) and gate-verified it. This section **reuses that tool**, not F193's specific question — F193 asked for a derivation of its own dilution exponent $p=2$ (the $\rho_\text{vac}(a/R_H)^p$ law), and this construction's natural density scaling is $b^{-4}$ (§4 below), not $b^{-2}$, so it could not have produced F193's target even in principle. What it *does* ask, with the same tool, is F319 U8's order-selectivity question — the closer and, since Amendment 4, the currently live one. Applying it to F59/F164's two Sakharov moments — recomputing $I_\text{cc}(b)=\int_{\kappa\in\text{BZ}}\Omega_\text{coarse}(\kappa)/2$ and $I_g(b)=\int_{\kappa\in\text{BZ}}1/(2\Omega_\text{coarse}(\kappa))$ over the *same*-sized coarse Brillouin zone, i.e. treating the coarse description as accessing only the reduced momentum range it corresponds to — gives, fit directly (not extrapolated) over $b\in[100,10000]$:

$$I_\text{cc}(b)\sim C_\text{cc}\,b^{p_\text{cc}},\quad p_\text{cc}=-0.999989\ (\to-1)\ ;\qquad
I_g(b)\sim C_g\,b^{p_g},\quad p_g=+0.999991\ (\to+1),$$

machine-exact fits (the coarse dispersion becomes purely linear across the whole coarse BZ as $b\to\infty$, since $\kappa/b\to0$ for every fixed $\kappa\in(-\pi,\pi]$ — this is just T1's fixed point read at every point of the zone at once). Converting to physical densities (dividing by the coarse cell volume $a_\text{coarse}^3=(ba)^3$, and by $a_\text{coarse}^2$ for $1/G$) gives $a_0(b)\propto b^{-4}$ and $1/G(b)\propto b^{-1}$, i.e. **$G(b)\propto b$ — it *grows***.

Closing F319 U8's own $120.76$-decade requirement on $a_0$ through this channel needs

$$b^\star=10^{120.76/4}=1.55\times10^{30},$$

at which point

$$\frac{\Delta G}{G}=\left|\frac{G(b^\star)}{G(1)}-1\right|=3.12\times10^{30}$$

— **$35.15$ orders of magnitude beyond CODATA's $2.2\times10^{-5}$ budget on $G$**. This is a *worse* failure mode than F319 U8's uniform-$\lambda$ exclusion (there, $a_1$ moved by an $O(1)$-scaled "enhancement" at the value needed for $a_0$; here $a_1$ diverges as $b$ grows while $a_0$ is falling, so no choice of $b$ helps both — the two requirements pull in opposite directions from the start, structurally, not just numerically). **This channel is excluded.**

**Why, and what it sharpens.** F130 T3b already computed the *correct* way gravity's sector behaves under legitimate coarse-graining: real-space block-averaging of the log-variable $u$ on an *existing field configuration*, which leaves the source law IR-form-invariant to $O(b^{-2})$ — i.e. $G$ effectively does **not** run this way. The check in this section is a different (and, given T3b, provably wrong) operation: recomputing a coupling from a truncated Brillouin-zone integral, which discards short-distance modes' contribution outright rather than properly matching them onto the coarse theory (the correct Wilsonian procedure). That the naive version fails by 35 decades is not a surprise once T3b is recalled — but it had not been tried and quantified against K9's specific requirement before, and doing so **rules out the single most obvious way of reusing F130's tool for K9**, closing off a wrong turn with a computed number rather than leaving it as an unattempted possibility.

## 5. Context: why both tested channels were local, and why that predicts their failure

Weinberg's 1989 no-go theorem (surveyed in Padilla, arXiv:1502.05296 §3) shows, under fairly general assumptions, that essentially any **local, Lorentz-invariant** dynamical adjustment mechanism cannot relax a large bare cosmological constant to a small value without reintroducing the same order of fine-tuning it was meant to remove. Both channels this finding tests are local constructions in exactly that sense: K1's self-consistent Friedmann back-reaction treats $\rho_\text{vac}$ as an ordinary local source of the field equations (no non-local input beyond the horizon scale it itself would generate), and K4's block-spin coarse-graining is a purely local (real-space, finite-range) transform of the microscopic theory. Their failure is therefore the *expected* outcome under the theorem, not a defect special to this model.

The one channel of the right *type* to evade the theorem is a **non-local/global** one — tied to a quantity (like the Hubble horizon $R_H$) that is not fixed by local physics alone. This is exactly what the *surviving* F193§B/F196/F241 ceiling route already is: it is stated in terms of $R_H$, a global cosmological quantity, not a local field value. The literature's own analogous move is Kaloper & Padilla's vacuum-energy sequestering (*Phys. Rev. D* **90**, 103523 (2014)), which evades the theorem with a spacetime-volume-averaged global constraint rather than a local field. This finding does **not** attempt to build such a mechanism for this model — it records the connection as context for why the surviving route is the one still worth pursuing, and why the two channels closed here were never going to be the answer.

## 6. What is derived vs computed vs classified

| Piece | Status |
|---|---|
| F196's ceiling $=$ F182's Friedmann-I constraint at $L=R_H$ | **exact** (residual $0.0$) |
| $R_H(\rho_\text{vac,bare})=a\sqrt{3/(g_*I_\text{cc})}=0.606\,a$ | **exact-algebraic**, matched to a direct numeric Friedmann solve (residual $0.0$) |
| homogeneous source: DC residual $/S_0=1.000$ (no static-dielectric solution) | **exact** (Fredholm alternative, machine-confirmed) |
| $AB\equiv1$ restricted to $T_{\mu\nu}=0$ (F178) $\Rightarrow$ inapplicable to a homogeneous energy density | **structural** (citation of an already-adopted decision) |
| channel (ii) **excluded** | **derived**, from the two rows above |
| blockspin exponents $p_\text{cc}=-1$, $p_g=+1$ | **machine** ($<1.1\times10^{-5}$) |
| closing $a_0$ via this channel needs $b^\star=1.55\times10^{30}$, giving $\Delta G/G=3.1\times10^{30}$ | **quantitative** (computed) |
| excess over CODATA's $2.2\times10^{-5}$ budget: $35.15$ decades | **quantitative** |
| naive-blockspin channel **excluded** | **derived**, from the two rows above; diagnosed against F130 T3b |
| $\Omega_\Lambda\approx0.685$; the surviving ceiling route's own dynamics | **untouched**, exactly where F241/Amendment 4 left them |

## 7. Falsifiers

1. **A demonstration that F182's Friedmann-I and F196's ceiling are *not* algebraically identical formulas.** K1's residual is $0.0$ by direct sympy-level substitution; a genuine discrepancy would mean one of the two derivations carries a hidden extra assumption this finding missed.
2. **A normalisable static solution of $\nabla^2u=-S$ on a periodic domain for nonzero constant $S$.** K2a's DC-mode argument is a general fact about the Laplacian (Fredholm alternative); an exhibited counterexample would break it.
3. **A demonstration that F178's $AB\equiv1$ scope restriction does not, in fact, exclude homogeneous energy-density sources** — e.g. a reading of F178 under which the "interior" case does not include the cosmological FRW fluid. This is the single most attackable premise in §3, being a citation rather than a new computation.
4. **A recomputed block-spin exponent pair differing from $(-1,+1)$.** T1 (F130) already forces this in the $b\to\infty$ limit for *any* dispersion with a linear IR fixed point; a genuine deviation would mean the F26/BCC dispersion is not linear at small $q$, contradicting F26 itself.
5. **A demonstration that the naive truncated-BZ recomputation of $1/G$ IS the correct Wilsonian matching procedure**, rather than the wrong tool F130 T3b's own (different, correct) treatment already supersedes. Would require showing T3b's $O(b^{-2})$ form-invariance is itself flawed.
6. **A genuinely non-local/global mechanism that dynamically enforces the F183/F190 ceiling.** Would close K9 outright and is the outcome this finding's §5 flags as the remaining, untried shape.

## 8. Honest scope

This finding **eliminates two candidate channels with computed content**, not by re-reading an existing result (Amendment 4's own caveat about itself) but by running the model's own Friedmann equation, its own field-equation scope restriction, and its own proven block-spin transform against two concrete, previously-unattempted questions. It does **not** supply a positive mechanism: the F193§B/F196/F241 ceiling route is untouched, still a consistency requirement rather than a demonstrated dynamical outcome, and remains the sole surviving candidate of the right shape. K1's Friedmann-identity observation is largely definitional (the "ceiling" formula is, after all, just the textbook critical-density formula, and F196's two elaborate derivations — Schwarzschild capacity, Bekenstein–Hawking entropy — were bound to reproduce it for that reason) and is reported as clarifying rather than as new suppression physics; it is included because it corrects an implicit overclaim risk (reading the ceiling as importing extra structure from black-hole/holographic physics that a plain FRW argument does not already supply). K2's structural half (citing F178) is the most attackable single step in this finding — it rests on reading F178's "interior vs vacuum" split as applying to the *homogeneous cosmological* case, which the decision's own text supports but does not spell out in those words. §5's Weinberg-theorem framing is context, explicitly not a proof that no local mechanism could ever work — it explains *why* the two failures found here were the expected outcome, and narrows what a genuine future attempt would need to look like (non-local, tied to a global/horizon quantity), which is exactly the shape the surviving ceiling route already has.

## Reviewed & corrected

**2026-08-28 - 19:20** -- attack pass: **CONFIRMED-NARROWER** (cold `general-purpose` subagent,
13/13 attacks run, including the perturbation sweep and a robustness sweep over grid resolution,
fit window, and the K4 extrapolation). Found: no FAIL. Four WEAKENS -- (3) the registry's
`expect.tol` is not read by the runner for `kind: assertion` records (repo-wide convention, not a
defect specific to this record -- e.g. F319 carries the same decorative `tol`); (7) `casim test
--param n=...` only stressed K1, silently leaving K3/K4 untested by that lever; (10) Sec.4's
framing overstated fidelity to F193's own named next step (F193 asked for its dilution exponent
$p=2$; this construction's natural density scaling is $b^{-4}$, not $b^{-2}$, so it could not have
produced F193's target -- it reuses F193's *tool* against F319 U8's *question* instead); (12) the
module's `blockspin_moment` silently underflows to a spurious exact $(0.0,0.0)$ past $b\sim3\times10^8$
with no warning -- not on the path used for K4's reported numbers (which use the closed-form fit),
but a landmine for a future direct sanity check, as the attack itself found. Fixed: `run()` now
threads its `n` parameter through to `blockspin_asymptotics`/`blockspin_selectivity` (re-verified:
`excess_orders_of_magnitude` moves by $<0.01$ between $n{=}30$ and $n{=}200$, confirming the
robustness the attack already measured by hand); `blockspin_moment` now raises with a clear message
above $b=10^6$ instead of returning silent zeros; Sec.4 and the module docstring reworded to say
"reuses F130's tool, benchmarked against F319 U8's requirement" rather than "the literal reading of
F193's own named next step". Rejected: none. Deferred: none -- both fixes were small and landed in
this same session. Both declared controls and the K1--K4 numbers re-verified unchanged after the
fixes (`casim test --id F332-cc-dynamics`, `casim test --control --id F332-cc-dynamics`).

## 9. Files

- Module: `src/casim/engine/interactions/cosmology_lambda_dynamics.py`
- Registry record: `F332-cc-dynamics` in `tests/registry/interactions.yaml` (tier gate, 2 controls verified)
- Results: `test-results/F332_cc_dynamics.json`
- Registered: `src/casim/engine/registry.py` (`interactions.cosmology_lambda_dynamics`)
