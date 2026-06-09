# F117 — The gap-coupled colour-dielectric gluon propagator (the condensate wired into time evolution)

**Date:** 2026-06-08 - 16:05
**Status:** Confirmed — 6/6 PASS; GD1/GD4 bit-for-bit + machine-ε, GD2 machine-ε unitary, GD3 exact hand-off identities, GD5/GD6 quantitative.
**Modules:** `ca-simulation/ca_colour_dielectric.py` (new **Part D**)
**Tests:** `model-tests/test_FG7f_gluon_dielectric_gap.py` (new)
**Results:** `test-results/FG7f_gluon_dielectric_gap.json`
**Cross-refs:** F86 (dual-superconductor flux tube — Parts A/C), F88 (colour-magnetic condensate *derived*, the gap source), F91 (gluon propagator is the **even** law), F64 (gravity dielectric — the structural template), F43/FG-7 (dynamical gluon sector), F26 (c = rotation rate).

---

## What this closes

Parts B/C of `ca_colour_dielectric.py` (F86) were **static**: a single-tick uniform-`eps_c` step, and analytic London/BPS constructions for the flux tube. The condensate that sets `eps_c` (F88) lived in a *separate* module and was never fed into a propagating gluon. F117 wires the two together inside the **time-evolved** propagator, so that the model's confinement mechanism is now a dynamical statement, not a static energetics one.

The thesis, made operational: **one measured number — the condensate VEV $v$ — simultaneously fixes**

1. the colour-dielectric $\varepsilon_c(x)=1-f(x)^2$ that renormalises the $(\mathbf E,\mathbf B)$ rotation rate (hence $c$),
2. the dual-Meissner gluon mass $m_V = e v = m_D$ the colour field acquires in the vacuum,
3. the screening length $\lambda = 1/m_V$ and the F86 tension $\sigma = 2\pi v^2$.

These are not three inputs; they are three faces of the one gap.

## Part D — what was built

**D-i — uniform dielectric on the BCC even-law propagator.** `gluon_dielectric_rotation_step_bcc` rescales the even dispersion $\Omega_\text{even}(k)\to\Omega_\text{even}(k)\sqrt{\varepsilon_c}$ (refractive slow-down $n_c=\varepsilon_c^{-1/2}$, exactly the F64 form). This is the BCC twin of the existing 2D step and respects F91: the gluon propagates on the **even** law, not the chiral one.

**D-ii — gap coupling.** `condensate_vev` / `condensate_vev_from_mc` run the F88 monopole-density chain $\rho\to z\to m_D\to v=m_D/e$ on an equilibrated 3D compact-U(1) configuration and hand back $\{v,\,m_V,\,\sigma_{F86}\}$ — the VEV is **measured**, never assumed.

**D-iii — gap-massive gluon step.** `gluon_gap_massive_step_bcc` evolves $(\mathbf E,\mathbf B)$ with the condensate-induced mass via the Proca even law, $\omega_\text{eff}=\sqrt{m_V^2+\Omega_\text{even}^2}$.

**D-iv — spatially-varying $\varepsilon_c(x)$ evolution.** `gluon_dielectric_evolve_{2d,bcc}` integrate a colour-electric packet through a condensate field with a split-step that locally rescales the free rotation increment by $s(x)=\sqrt{\varepsilon_c(x)}$. In the condensed vacuum $\varepsilon_c\to0\Rightarrow s\to0$: the field is **frozen** — colour-electric flux cannot rotate (propagate) into it. This is the dual Meissner expulsion realised in time evolution.

## Results (6/6 PASS)

| ID | Statement | Class | Residual |
|----|-----------|-------|----------|
| GD1 | BCC dielectric step $=$ free even step at $\varepsilon_c=1$ | bit-for-bit | $0.0$ |
| GD2 | Uniform dielectric unitary over 200 ticks; $c_\text{eff}=c_\text{lat}\sqrt{\varepsilon_c}$ | machine-ε | $4.1\times10^{-14}$ (drift); $c_\text{eff}$ res $0$ |
| GD3 | $v,m_V>0$ from MC; $\sigma_{F86}=2\pi v^2$; $v=m_D\sqrt\beta$ | exact identities | $0.0$ |
| GD4 | Gap-massive dispersion $\omega^2=m_V^2+\Omega_\text{even}^2$; $m_V{=}0$ reduces to free | machine-ε + bit-for-bit | $1.2\times10^{-13}$; $0.0$ |
| GD5 | Same measured $m_V$ gives screening $\lambda=1/m_V$ | quantitative | $2.2\%$ |
| GD6 | Packet expelled from condensed vacuum; $\varepsilon_c{=}1$ control transmits | quantitative + bit-for-bit | $1.4\%$ in-vacuum vs $52\%$ control ($\sim38\times$); free-step $0.0$ |

A representative MC run ($L=6,\beta=1.8$) measures $\rho\approx0.024\Rightarrow v\approx0.975,\ m_V\approx0.727,\ \sigma_{F86}\approx5.97$.

## New information

1. **The confinement scale is one number, propagated.** Before F117 the dielectric ($\varepsilon_c$), the screening length ($\lambda$), the tension ($\sigma$) and the propagator mass were established in separate static computations. GD3–GD5 show they collapse onto the **single measured** $m_V=ev=m_D$: the *same* number that sets the time-evolved gluon mass gap (GD4, machine-ε) also sets the static screening length (GD5) and, through $\sigma=2\pi v^2$, the string tension. The gap is the only free quantity in the colour propagator, and it is measured from the monopole density, not fitted.

2. **Confinement as kinematic freezing.** GD6 demonstrates that, in the model's own rotation-rate language (F26), confinement is the $\varepsilon_c\to0$ limit where the $(\mathbf E,\mathbf B)$ rotation rate $\to0$: flux does not get reflected, it simply *cannot rotate* into the condensed region. This is the dynamical complement to F86's static BPS/London picture and is the colour mirror of F64's gravitational dielectric — same renormalised rotation rule, opposite impedance regime (F64 matches, $AB=1$, transparent; confinement breaks impedance, $\varepsilon_c\to0$, opaque).

3. **Exact F91 coherence.** Wiring the dielectric into the even-law BCC step (D-i) and the gap mass into the even-law Proca step (D-iii) keeps the gluon entirely on the even propagator. The $m_V=0$ / $\varepsilon_c=1$ reductions are bit-for-bit (GD1, GD4), so the gap-coupled propagator is a *renormalisation* of the F91 free step with zero drift in the trivial limit — no new propagator was introduced, only a $v$-sourced coefficient on the existing one.

## Honest scope

- **Uniform** $\varepsilon_c$ and the gap mass are exact/machine-ε (spectral, orthogonal). The **spatially-varying** evolution (D-iv) is a 2nd-order split-step: it is bit-for-bit the free step at $\varepsilon_c\equiv1$ and demonstrates expulsion robustly ($\sim38\times$), but it is not claimed to be exactly energy-conserving away from the uniform limit — a variable-speed wave problem does not admit a cheap exactly-orthogonal one-FFT map. The rigorous exactness lives in the uniform step (GD1/GD2) and the analytic Parts A/C (F86).
- The MC VEV inherits F88's quantitative status (finite $L$, dilute-gas chain); GD3's *identities* ($\sigma=2\pi v^2$, $v=m_D\sqrt\beta$) are exact, the *value* of $v$ is measured to MC precision.
- $e$ is fixed by $e^2=1/\beta$ in 3D lattice units, so $m_V=m_D$ directly; mapping to physical units rides the F86/F88 calibration, untouched here.
