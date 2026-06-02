# F50 — Gravity fork from F46: which leg of the spherical triangle carries gravitational redshift

**Date:** 2026-05-28 - 23:55 (updated 2026-05-29 - 00:30 — kinetic leg promoted to the bounded exact-QCA form)
**Status:** Confirmed — 8/8 tests PASS (G1 slope-4 lattice correction; G2–G4, G6 algebraic/machine-ε; G5 exactly norm-conserving prototype stepper; G7 boundedness + slope; G8 bit-for-bit QCA stepper phase match)
**Module:** `ca-simulation/forks/gr_fork_F46_dirac.py` (new); reuses `gr_fork_E_tensor.py` (metric), `ca_dirac.py` (`_mix_eta_chi`), `ca_curved.py` (`CayleyVarcSolver2D`)
**Verification script:** `model-tests/test_F50_gravity_fork_dirac.py`
**Results:** `test-results/F50_gravity_fork_dirac.json`
**Cross-references:** F46 (spherical-Pythagorean Dirac dispersion, §9.3 curved-spacetime follow-up), F16 (GR-3 factor-2 resolution by Forks A/B/C), F26 (speed of light as rotation rate), F27 (chiral SU(2) mass rotation), `gr_fork_E_tensor.py` (Fork E3 "tetrad Dirac" promise), `ca-dirac-gravity-plan.md` Stage D2, `reference-research/physics-notes-complete.md` pp. 16–17, 32–33 (Sachs tetrad spinor formalism)

---

## 1. Question

F46 §9.3 proposed a curved-spacetime extension:

> In a curved tetrad background, $\Omega_\text{kin}$ becomes site-dependent. F46 then predicts that gravitational redshift enters Dirac as a site-dependent renormalisation of the kinetic leg of the spherical triangle.

This finding works out that extension to algebraic exactness and tests it. The headline result is a **correction to the wording of F46 §9.3**: the static gravitational redshift sits on the **rest** leg (via the lapse), not the kinetic leg. The kinetic-leg renormalisation carries deflection and Shapiro delay instead. Both are "site-dependent renormalisations of a leg," which is why the loose wording is half-right — but for a *static clock* the redshift cannot live on the kinetic leg, and the test G4 proves it.

---

## 2. Tetrad derivation

Recall the F46 identity (exact lattice Dirac dispersion):

$$\cos\Omega_\text{Dirac}(\mathbf k, m) = \cos\Omega_\text{rest}(m)\cdot\cos\omega_\text{kin}(\mathbf k),\qquad \Omega_\text{rest}=\arcsin m.$$

Place the field on a static, diagonal background written with lapse $A$ and spatial factor $B$:

$$ds^2 = -A(\mathbf x)\,c_0^2\,dt^2 + B(\mathbf x)\,\delta_{ij}\,dx^i dx^j,\qquad g_{00}=-A,\ g_{ii}=B.$$

The diagonal tetrad is $e^0{}_0=\sqrt A,\ e^k{}_i=\sqrt B\,\delta^k_i$, with inverse $e_0{}^0=1/\sqrt A,\ e_k{}^i=\delta/\sqrt B$. Insert into the chiral curved Dirac equation $i\gamma^a e_a{}^\mu(\partial_\mu+\Omega_\mu)\psi=m\psi$, drop the spin connection $\Omega_\mu$ (it sources geodesic bending / the gravitational force, not the leading frequency shift), and multiply the time component by $\sqrt A\,\gamma^0$:

$$
\boxed{\;i\,\partial_t\psi = \Big[\,c_0\sqrt{A/B}\;\boldsymbol\alpha\cdot\hat{\mathbf p} \;+\; \sqrt A\,m c_0^2\,\beta\,\Big]\psi\;}
$$

So **both legs of the F46 triangle become site-dependent**:

| Leg | Flat | Curved (coordinate frame) | Carries |
|---|---|---|---|
| kinetic | $\omega_\text{kin}(\mathbf k)=\arccos(c_x c_y)$ | $r_\text{kin}(x)\,\arccos(c_x c_y)$, $r_\text{kin}=\sqrt{A/B}$ | deflection (GR-1), Shapiro (GR-2), matter slowing |
| rest | $\arcsin m$ | $\sqrt{A(x)}\,\arcsin m$ | **static gravitational redshift (GR-3)** |

giving the **covariant F46 identity**

$$
\boxed{\;\cos\Omega_\text{Dirac}^\text{coord}(x,\mathbf k,m) \;=\; \cos\!\big(\sqrt{A(x)}\,\arcsin m\big)\cdot\cos\omega_\text{kin}\big(\mathbf k;\,c_\text{eff}(x)\big)\;}
$$

**Bounded exact-QCA kinetic leg (2026-05-29 promotion).** The kinetic leg is the genuine Paper-1 Eq.16 Weyl walk, $\omega_\text{kin}^0(\mathbf k)=\arccos(c_x c_y)$ with $c_i=\cos(k_i/\sqrt2)$ (the F25/F26/F46 leg), gravitationally rate-rescaled by the *dimensionless* factor $r_\text{kin}(x)=\sqrt{A/B}=c_\text{eff}/c_0$:

$$\omega_\text{kin}(\mathbf k;x)=\sqrt{A(x)/B(x)}\;\arccos\!\big(\cos\tfrac{k_x}{\sqrt2}\cos\tfrac{k_y}{\sqrt2}\big).$$

This is bounded in $[0,\pi]$ (in a well $r_\text{kin}<1$, so $\omega_\text{kin}\le r_\text{kin}\pi<\pi$), reduces **bit-for-bit** to the flat F46 leg at $A=B$, carries the true finite-$k$ lattice anisotropy of the QCA, and — for a uniform (or adiabatic) background — is reproduced by the exact-QCA Weyl stepper's per-tick phase to machine precision (G8). The earlier continuum leg $\omega_\text{kin}=c_\text{eff}|\mathbf k|$ is retained as the Euclidean small-$k$ reference (G1).

**Continuum limit** (small legs, $\cos x\approx1-x^2/2$):

$$\Omega^2 \approx \big(\sqrt A\,m c_0^2\big)^2 + \big(c_\text{eff}|\mathbf k|\big)^2 = A\,m^2 c_0^4 + \tfrac{A}{B}\,c_0^2|\mathbf k|^2,$$

which is exactly the dispersion of the curved-tetrad Hamiltonian above. This is the geometric statement that the relativistic dispersion in a static field is the Euclidean shadow of the spherical triangle, with both legs gravitationally renormalised.

---

## 3. Which leg carries redshift (the correction)

**Static clock, $\mathbf k=0$.** The kinetic leg $\omega_\text{kin}=0$, so $\cos\omega_\text{kin}=1$ *regardless of $c_\text{eff}(x)$*. A kinetic-leg-only scheme therefore leaves

$$\Omega_\text{Dirac}^\text{coord}(\mathbf k=0)=\arcsin m\quad\text{at every site} \;\Rightarrow\; \text{no static redshift.}$$

The redshift is carried by the rest leg:

$$\Omega_\text{Dirac}^\text{coord}(\mathbf k=0)=\sqrt{A(x)}\,\arcsin m,$$

so two clocks at $x_1,x_2$ tick in ratio $\sqrt{A_1/A_2}$. For a weak field $A=1+2\phi/c_0^2$ this is $\Delta\nu/\nu = \Delta\phi/c_0^2$ — the correct GR **factor 1**, not the Paper-6 baseline factor 2.

This is the same physics F16 found at the metric level (Forks A/B fix GR-3 by decoupling the clock $\tau=\sqrt A$ from the propagator $c_\text{eff}$); F50 shows it is forced by the *geometry* of the F46 triangle, and discharges the "E3 — tetrad Dirac" promise written in `gr_fork_E_tensor.py` (that the factor-1 redshift "falls out of $\sqrt{-g_{00}}$ automatically and GR-3 needs no separate phase-tick field"). Here $\sqrt{-g_{00}}=\sqrt A$ is precisely the rest-leg renormalisation.

**Photon limit, $m=0$.** Rest leg vanishes, $\Omega=\omega_\text{kin}(\mathbf k;c_\text{eff})$ with $c_\text{eff}=c_0\sqrt{A/B}$ — identical to Fork-B / Fork-E $c_\gamma$ (verified bit-for-bit, G3).

---

## 4. Implementation — the gravity fork

`gr_fork_F46_dirac.py` exposes the standard GR-harness interface so it drops into `gr3_fork_harness.py`:

- `metric(phi,c_0) -> (A,B)` — reuses Fork E's exact isotropic-Schwarzschild metric (all PN orders, one static source), default mode `exact_isotropic`.
- `c_photon = c_matter = c_eff = c_0\sqrt{A/B}` — the kinetic leg.
- `tau_rate = \sqrt A` — the rest-leg renormalisation factor.

Plus the F46-specific predictions `rest_leg`, `kinetic_leg`, `dirac_omega_coord` (exact triangle), and `dirac_omega_continuum` (Euclidean reference).

**Prototype propagator.** `gravity_dirac_step_2d` realises the identity at the propagator level by Strang splitting one coordinate tick:

$$\text{Mix}_\text{rest}\!\big(\sqrt A\,m,\tfrac{dt}{2}\big)\;\circ\;\text{Kinetic}\big(c_\text{eff},dt\big)\;\circ\;\text{Mix}_\text{rest}\!\big(\sqrt A\,m,\tfrac{dt}{2}\big)$$

- Rest mix: the existing `ca_dirac._mix_eta_chi` with site-dependent angle $\theta(x)=\sqrt{A(x)}\,m\,dt$.
- Kinetic: the existing `ca_curved.CayleyVarcSolver2D` (Cayley/Crank–Nicolson, exactly unitary) applied independently to $\eta$ and $\chi$ with the shared $c_\text{eff}(x)$ field.

Each sub-operator is exactly unitary, so total norm is conserved to the linear-solver floor; Strang error is $O(dt^2\,|\nabla A|,\,dt^2\,|\nabla c_\text{eff}|)$. (The first attempt used `weyl_step_2d_varc_strang` for the kinetic leg and drifted $\sim 3.8\%$ over 12 steps — that stepper is only approximately unitary, per its own docstring; switching to the Cayley solver fixed the drift to exactly $0$.)

---

## 5. Test results (`test_F50_gravity_fork_dirac.py`, 2026-05-28 - 23:55)

| # | Test | Result | Target | Status |
|---|---|---|---|---|
| G1 | Continuum reduction: log-log slope of $|\Omega^2_\text{sph}-\Omega^2_\text{cont}|$ vs leg scale | slope $=4.0008$ | $4.0\pm0.1$ | **PASS** |
| G2 | Static redshift on rest leg: $\Omega(\mathbf k{=}0)=\sqrt A\arcsin m$; near/far clock ratio | rest residual $1.7\times10^{-16}$; ratio$_\text{GR}=0.9970\pm8\times10^{-4}$ (baseline 2.0) | residual $<10^{-13}$, ratio $\to1$ | **PASS** |
| G3 | Photon limit $m=0$: $c_\text{eff}=$ Fork-E $c_\gamma$, and $\Omega=\omega_\text{kin}$ | $|\Delta c_\text{eff}|=0$; $|\Omega-\omega_\text{kin}|=1.7\times10^{-16}$ | $<10^{-13}$ | **PASS** |
| G4 | Negative control: kinetic-leg-only $\Rightarrow$ position-independent $\Omega(\mathbf k{=}0)$ | spread $=0$; value $=\arcsin m$ to $10^{-16}$ | spread $\approx0$ | **PASS** |
| G5 | Prototype Strang stepper (Cayley kinetic) norm conservation, 12 steps, $L=48$ | relative drift $=0.0$ | $<10^{-10}$ | **PASS** |
| G6 | Bounded exact-QCA leg reduces to flat F46 $\cos\Omega=\sqrt{1-m^2}c_x c_y$ at $A=B$, 200 random $(\mathbf k,m)$ | residual $4.4\times10^{-16}$ | $<10^{-14}$ | **PASS** |
| G7 | Bounded leg stays in $[0,\pi]$ over 400 random $\mathbf k$; small-$k$ slope $=r_\text{kin}/\sqrt2$ | in-band True; slope err $2.0\times10^{-9}$ | $<10^{-6}$ | **PASS** |
| G8 | Homogeneous exact-QCA stepper per-tick phase $=r_\text{kin}\arccos(c_x c_y)$, 20 ticks | abs err $=0.0$ (bit-for-bit) | $<10^{-12}$ | **PASS** |

Total: **8/8 PASS** (`OVERALL: PASS`).

G1 confirms the spherical→Euclidean reduction has the F46-characteristic 4th-order lattice correction even with both legs gravitationally renormalised. G2 is the physics headline (factor-1 redshift on the rest leg). G3 ties the photon sector to the existing Fork-E/B metric. G4 is the explicit disproof of the literal F46 §9.3 wording. G5 shows a concrete unitary propagator exists. G6–G8 validate the bounded exact-QCA kinetic leg: it collapses to flat F46 at $A=B$, never leaves the Brillouin zone, and is reproduced bit-for-bit by the QCA stepper in a uniform background.

---

## 6. Where this sits among the forks

- It is **Fork E3** (`gr_fork_E_tensor.py` named it but left it "tracked separately"): couple matter through the tetrad so redshift comes from $\sqrt{-g_{00}}$.
- It is **observationally degenerate with Forks A and B** on GR-1…GR-4 (it reuses their $c_\gamma$ and $\tau=\sqrt A$). It does not by itself select among A/B/E — the F16 discriminator (a photon-vs-matter metric-split observable) is still open.
- Its added value is conceptual closure: it derives the clock/propagator split that F16 had to *impose by hand* directly from the F46 triangle + the tetrad, with no free parameters.

---

## 7. Open follow-ups (not blocking)

1. **Spin connection $\Omega_\mu$.** Dropped here (leading frequency shift only). Restoring it adds the gravitational force / geodesic bending at the propagator level — needed to reproduce GR-1/GR-2 from the *stepper* rather than from the metric line integral. (`ca-dirac-gravity-plan.md` Stage D2, Rindler/Schwarzschild geodesic tests.)
2. **Exact-QCA kinetic leg — DONE (2026-05-29).** The kinetic leg is now the bounded Paper-1 Eq.16 form $r_\text{kin}\arccos(c_x c_y)$ (G6–G8): bit-for-bit flat-F46 reduction, boundedness, and a machine-precision phase match against the exact-QCA Weyl stepper for a uniform background. **Remaining sub-item:** the *inhomogeneous* exact-QCA stepper. The QCA Weyl walk is Fourier-diagonal (a single global $c$), so a site-dependent $r_\text{kin}(x)$ cannot be applied locally in the spectral walk; the inhomogeneous propagator currently uses the centered-difference Cayley stepper (whose band is *not* the QCA $\arccos$). Closing this needs either a position-space exact-QCA walk or an adiabatic/WKB patching of local QCA rates — the genuine open piece.
3. **Zitterbewegung redshift.** The prediction $\Omega_Z^\text{coord}(x)=2\sqrt{A(x)}\,\arcsin m$ at $\mathbf k=0$ is directly measurable from chirality-population oscillations in the prototype stepper (cf. `measure_zitterbewegung_freq_2d`) — a clean dynamical test of rest-leg redshift.

---

## 8. Provenance

- Hypothesis source: F46 §9.3 (2026-05-28) + `gr_fork_E_tensor.py` E3 note + `ca-dirac-gravity-plan.md` Stage D2.
- Tetrad reduction: §2 above, from the Sachs spinor formalism (`physics-notes-complete.md` pp. 16–17, 32–33).
- Numerical verification: `model-tests/test_F50_gravity_fork_dirac.py` (5/5 PASS).
- Filed `test-results/F50_gravity_fork_dirac.json`.
