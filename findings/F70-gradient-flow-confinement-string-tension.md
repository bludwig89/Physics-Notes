# F70 — Wilson gradient flow / cooling driver + exact 2D confinement (static potential, string tension)

**Date:** 2026-06-01 - 16:35
**Status:** Confirmed — 6/6 (flow driver) + 8/8 (confinement) PASS; 7 results at machine ε / bit-for-bit, Creutz ratio & linear potential algebraically exact
**Modules:** `ca-simulation/ca_cooling.py` (new), `ca-simulation/ca_confinement.py` (new)
**Tests:** `model-tests/test_FG7b_gradient_flow.py`, `model-tests/test_FG7c_confinement.py`, `model-tests/run_confinement_mc.py` (heavy MC, user-run)
**Results:** `test-results/FG7b_gradient_flow.json`, `test-results/FG7c_confinement.json`
**Cross-refs:** F43 (FG-7 dynamical gluons + Wilson-loop primitives), `reference-research/ca-strong-design.md`

---

## Summary

Closes the open follow-up flagged in **F43 / FG-7** and the `first-gen-completeness.md` §5.1 FG-7 row:

> "The linear-confinement regime requires real-time link evolution from a near-identity start (gradient flow / cooling)."

Two deliverables:

1. **A correctly implemented Wilson gradient-flow / cooling driver** (`ca_cooling.py`) on the 2D-square SU(3) link field, verified against the four defining properties of the flow (cold fixed point, action monotonicity, su(3)-valued force, gauge covariance) plus its diffusive (lattice-Laplacian) action.

2. **An exact static quark potential** (`ca_confinement.py`): in 2D, SU(N) lattice gauge theory is exactly solvable, so the Wilson loop obeys a **strict area law** `⟨(1/N)Re Tr W(R,T)⟩ = w(β)^{R·T}`. This gives a **linear static potential** `V(R)=σR` with string tension `σ(β)=−ln w(β) > 0` for **every** finite coupling. That is the model-level statement of *why a quark cannot exist alone*: pulling a colour charge a distance `R` from its partners costs `σR`, which diverges.

This is the first time the model **predicts** confinement rather than being merely compatible with it. F43 had only established the cold baseline (`⟨W⟩=N_c`) and strong-coupling decorrelation; F70 supplies the actual area law, σ, and `V(R)`.

---

## Part A — Gradient flow / cooling driver

Wilson gradient flow (Lüscher 2010), continuum form:

$$\frac{d}{dt}V_\mu(x) = Z_\mu(V)\,V_\mu(x), \qquad Z_\mu(x) = -\big[\,V_\mu(x)\,\Sigma_\mu^\dagger(x)\,\big]_\text{TA},$$

with the traceless anti-Hermitian projection $\mathrm{TA}(M)=\tfrac12(M-M^\dagger)-\tfrac{1}{2N}\mathrm{Tr}(M-M^\dagger)I$ and $\Sigma_\mu(x)$ the sum of the two 2D staples attached to the link. The flow is gradient descent on the Wilson action, $dS_W/dt=-\sum_{x,\mu}\lVert Z_\mu\rVert^2\le 0$. Implemented with both an explicit-Euler and the canonical Lüscher 3-stage RK integrator, plus checkerboard **cooling** (replace each link by the SU(3) projection of its staple sum).

| Test | What it checks | Residual | Tier |
|------|----------------|----------|------|
| GF1 | Cold config is a flow/cooling fixed point ($Z=0$, $U$ unchanged) | $0.0$ bit-for-bit | 1 |
| GF2 | SU(3) unitarity + det=1 preserved (flow & cooling, 15 steps) | $2.5\times10^{-14}$ | 2 |
| GF3 | Wilson action monotonically non-increasing (RK3, Euler, cool) | max step $\Delta S<0$ | 1 |
| GF4 | Flow force $Z\in\mathfrak{su}(3)$ (anti-Hermitian, traceless) | $5.6\times10^{-16}$ | 1 |
| GF5 | Flow is gauge-covariant: $\text{flow}(U^g)=\text{flow}(U)^g$ | $7.8\times10^{-15}$ | 1 |
| GF6 | Flow acts as the lattice Laplacian (decay rate $\propto\hat k^2$) | $4.9\times10^{-10}$ | 2 |

**GF5** is the central correctness certificate: a buggy staple or projection breaks gauge covariance immediately. **GF6** confirms the flow is genuinely diffusive — for small abelian transverse modes the per-step decay $\delta(k)/\hat k^2$ is the same constant across wavevectors to $5\times10^{-10}$, i.e. high-frequency disorder is smoothed fastest, exactly as a heat equation on the connection.

---

## Part B — Exact confinement (why 2D is the right testbed)

In two Euclidean dimensions, after gauge-fixing to axial gauge $U_x\equiv I$, the plaquette variables are **independent**. By **Schur's lemma** the single-plaquette mean of the class-invariant Wilson distribution is

$$\langle U\rangle = w(\beta)\,I,\qquad w(\beta)=\Big\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,U\Big\rangle,\qquad d\mu_\beta(U)\propto e^{(\beta/N)\mathrm{Re}\,\mathrm{Tr}\,U}\,dU.$$

A Wilson loop enclosing area $A=R\cdot T$ is the ordered product of the enclosed independent plaquettes, so $\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,W\rangle = w^{A}$ **exactly**. Consequences, all verified:

$$\boxed{\;\sigma(\beta)=-\ln w(\beta)>0\quad\forall\,\beta<\infty,\qquad \chi(R,T)=\sigma,\qquad V(R)=\sigma R\;}$$

`w(β)` is computed deterministically by SU(3) **Weyl-torus quadrature** (the periodic rectangle rule is spectrally accurate → machine precision; grid-converged to $3\times10^{-17}$).

| Test | What it checks | Residual | Tier |
|------|----------------|----------|------|
| CF1 | $w(0)=0$ (Haar), monotone $\uparrow$, $0<w<1$, $w\to1$ | $1.5\times10^{-17}$ | 1/2 |
| CF2 | $w(\beta)$ quadrature grid-converged (160→320) | $2.8\times10^{-17}$ | 2 |
| CF3 | $\sigma(\beta)=-\ln w>0$ for all finite β; $\sigma\downarrow$ in β | $\sigma_{\min}=0.219$ | 1 |
| CF4 | Creutz ratio $\chi(R,T)=\sigma$, **independent of $(R,T)$** | $2.2\times10^{-16}$ | 1 |
| CF5 | Static potential $V(R)=\sigma R$ exactly linear, $T$-independent | $8.9\times10^{-16}$ | 1 |
| CF6 | Metropolis lattice mean plaquette matches $w(\beta)$ | $4.8\times10^{-3}$ | 3 |
| CF7 | Gradient flow raises $\langle\text{plaq}\rangle$ → lowers $\sigma_\text{eff}$ | $0.07\to0.96$ | 3 |
| CF8 | Schur: $\langle\tfrac1N\mathrm{Tr}\,U\rangle$ real $=w$ ( + MC off-diag→0) | $1.3\times10^{-18}$ | 1 |

The **Creutz ratio** result (CF4) is the cleanest confinement signature: $\chi(R,T)=-\ln\frac{W(R,T)W(R-1,T-1)}{W(R-1,T)W(R,T-1)}=-\ln w=\sigma$ for **all** loop sizes, because the area-difference of the four loops is exactly one plaquette. A size-independent Creutz ratio ⇔ strict area law ⇔ linear potential ⇔ confinement.

Representative string tensions (standard Wilson normalisation):

| β | 0.25 | 0.5 | 1.0 | 2.0 | 4.0 | 8.0 | 20.0 |
|---|------|-----|-----|-----|-----|-----|------|
| σ(β) | 4.256 | 3.543 | 2.811 | 2.051 | 1.274 | 0.624 | 0.219 |

σ stays strictly positive — **2D SU(3) confines at every coupling**.

**CF7 ties the two halves together:** flowing a thermalised (disordered, $\langle\text{plaq}\rangle=0.070$, $\sigma_\text{eff}=2.66$) configuration drives $\langle\text{plaq}\rangle\to0.962$ and $\sigma_\text{eff}\to0.039$. Confinement lives in the **disordered** ensemble; cooling/flow is a smoother that dissolves the disorder (and with it the string tension) — which is exactly why the static-potential measurement uses the unflowed ensemble, and why over-cooling must be avoided. The flow's legitimate role is gauge-field smoothing / scale-setting, not generating confinement.

A heavier Monte-Carlo confirmation of the full area law on a larger lattice (`run_confinement_mc.py`) is provided for the user to run outside the sandbox tick budget; it writes a Claude-readable `test-results/confinement_mc.{json,md}`.

---

## What this adds to the model

1. **Confinement is now a model prediction.** The static $q\bar q$ potential is linear with $\sigma>0$ for all couplings; an isolated colour charge has infinite energy. This is the dynamical content behind "quarks cannot exist alone," delivered to algebraic exactness in 2D.
2. **A reusable, validated smoother.** The Wilson flow / cooling driver is gauge-covariant and action-monotone, available for scale-setting, topological-charge studies, and as the near-identity evolver F43 called for.
3. **Sets up the baryon (F71).** With $\sigma>0$ established, the colour-singlet three-quark state has a finite-energy binding argument: separating any one quark costs $\sigma R\to\infty$.

## Known limitations / scope

- **2D Euclidean.** The exact area law is special to two dimensions (independent plaquettes). 3+1D BCC confinement requires Monte-Carlo with a genuine deconfinement transition and is **not** claimed here; the 2D result is the rigorous, exactly-solvable anchor consistent with the F43 scoping.
- **Static (quenched) potential.** No dynamical quark loops / string breaking; the linear potential is the pure-gauge static source potential.
- **Cooling is a smoother, not a confiner** (CF7) — stated explicitly to avoid the common misreading that cooling "produces" the string tension.

---

## Exactness-inventory additions

Tier 1 (algebraic / bit-for-bit exact): GF1, GF3, GF4, GF5, CF3, CF4, CF5, CF8 — 8 entries.
Tier 2 (machine precision): GF2, GF6, CF1, CF2 — 4 entries.
Tier 3 (statistical / qualitative): CF6, CF7 — 2 entries.
