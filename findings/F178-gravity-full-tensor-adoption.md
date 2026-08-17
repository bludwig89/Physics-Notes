# F178 — Decision: gravity is sourced by the full stress-energy tensor (induced Einstein equation canonical); the single-scalar dielectric is demoted to the vacuum/weak-field representation

**Date:** 2026-06-29 - 20:55
**Numbering:** F177 was taken by a concurrent session; this is **F178** (re-checked per CLAUDE.md).
**Status:** Decision / reclassification (no new test — it changes the canonical status of the gravity sector and records the supersession map). Cross-checked against the exact results it rests on: F173 (single scalar ⇒ anisotropic stress, sympy-exact), F174 (energy-only ⇒ no maximum mass, 5/5), F176 (covariant recovery, 5/5).
**Decision note:** `docs/theory/key-decisions.md` (2026-06-29 entry).
**Cross-references:** [[F64-em-connection-gravity]], [[F106-psi-K-sourcing-derivation]], [[F173-pressure-tolman-discriminator]], [[F174-stellar-structure-overlay]], [[F176b-covariant-dielectric-tov-recovery]], [[F114-dielectric-black-hole]], [[F79-structural-newton-constant]], [[F107-canonical-a-adoption-L4-grb-gate]]; papers `Paper-07-Gravity.md`, `Paper-12-Unification-Rotation-Currency.md`; brief `FC09`.

---

## The decision

The fundamental gravitational law of the model is now the **induced Einstein equation**

$$G_{\mu\nu} = \frac{8\pi G}{c^4}\,T_{\mu\nu}\qquad(\text{canonical}),$$

with the structural/induced coupling $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79/F107). The energy-only dielectric sourcing $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ (F106) is **reclassified as its static weak-field reduction in a preferred frame** — a representation valid where $T_{\mu\nu}\to0$ (vacuum) or $p\ll\rho c^2$ (Newtonian), not the fundamental dynamical law.

## Why (three independent reasons)

1. **Lorentz covariance.** A source built from $T^{00}$ alone is not a tensor equation: $T^{00}$ is the energy density in one frame and mixes with momentum density and stress under a boost. Only coupling to the full $T_{\mu\nu}$ is frame-independent. The energy-only law can therefore only ever be a static, preferred-frame approximation.
2. **The model already names the parent.** F106 derived $\nabla^2\ln K=-8\pi T^{00}$ explicitly as "the static weak-field reduction of the induced Einstein equation $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$." This decision promotes that parent from "the thing we reduce" to "the law."
3. **Neutron stars.** The literal energy-only law has no maximum mass and predicts $R\approx20$ km at $2\,M_\odot$ — excluded by PSR J0740+6620 (F174). Covariantising with the full source recovers TOV-like structure (F176).

## What it entails (the structural change)

By F173 (exact), the impedance-locked single scalar ($A=1/K,\ B=K$, $AB\equiv1$) forces an *anisotropic* effective stress ($p_r=-p_t$) and cannot satisfy all components of $G_{\mu\nu}=8\pi T_{\mu\nu}$ for an isotropic perfect fluid. Therefore:

- **Inside matter** the metric must carry its second independent function; the dynamics are **general relativity (TOV)**. The single scalar is no longer the field equation there.
- **In vacuum** ($T_{\mu\nu}=0$) the impedance lock $AB\equiv1$ and the dielectric/rotation-rate picture survive as the weak-field representation — but the **exact** vacuum solution is **Schwarzschild**, not the exponential $K=e^{2u}$ (which agrees only to PPN order, differing at $O(u^2)$).

## Supersession map

| Item | Status after this decision |
|---|---|
| **Preserved** (vacuum / weak field) | factor-2 light bending, $\beta=\gamma=1$, Mercury $42.98''$/cy, Shapiro, gravitational redshift (F64 D-EM9, FA09); structural/induced $G$ (F79/F107); the emergent-origin picture (gravity = induced renormalisation of the $(\mathbf E,\mathbf B)$ rotation rate) |
| [[F64-em-connection-gravity]] | dielectric demoted to **vacuum/weak-field representation**; exponential $K=e^{2u}$ is the PPN-order approximation, not the exact metric |
| [[F106-psi-K-sourcing-derivation]] | $\nabla^2\ln K=-8\pi T^{00}$ reclassified as the **static weak-field reduction** (as F106 itself stated); not the fundamental law |
| [[F114-dielectric-black-hole]] | **superseded** — exact vacuum is Schwarzschild (horizon present); the horizon-free throat and $+4.6\%$ shadow were consequences of treating the exponential metric as fundamental |
| [[F173-pressure-tolman-discriminator]] | the energy-only $\rho$-vs-$\rho{+}3p$ departure is now understood as a **weak-field-reduction artifact**, not a prediction; the exact tensor analysis it contains stands |
| [[F174-stellar-structure-overlay]] | the no-maximum-mass result is the **diagnosis** that forced this decision, not a model prediction |
| [[F176b-covariant-dielectric-tov-recovery]] | the covariant solve confirms the full-tensor source recovers TOV; the $\sim2$ km $AB\equiv1$ residual exists only if one insists on keeping the single scalar in matter — which this decision does **not** |
| Paper VII / Paper XII | "one field, one source (energy)" weakened to "the rotation field's **full** stress-energy sources gravity"; the $E=mc^2$ "one currency" hinge is retained as the *origin* story, not as "energy is the only source" |

## Net effect

The gravity sector's **dynamics become general relativity**. The model's distinctive gravitational content narrows from "a new theory with novel strong-field predictions (dielectric black hole, neutron-star departure)" to **a derivation of the origin and value of $G$** — gravity as an emergent, induced (Sakharov-type) renormalisation of the rotation substrate whose low-energy dynamics are exactly Einstein's. This is a deliberate trade: Lorentz covariance and automatic consistency with neutron stars and cosmology, in exchange for the dielectric's distinctive strong-field phenomenology.

## Code status

- `ca-simulation/ca_gravity.py` (dielectric) — **canonical in vacuum/weak field** (lensing, PPN, redshift); a status banner now records that it is the weak-field representation, not the strong-field law.
- `ca-simulation/ca_stellar.py` (`theory='gr'`, TOV) — **canonical for the relativistic interior / strong field**.
- **Scoped follow-up:** a full covariant kernel that evolves the two-function metric in matter (replacing the single dynamic dielectric channel of `ca_gravity.py` D-EM8 inside sources). Until built, strong-field work uses the TOV solver and the dielectric is used only where $T_{\mu\nu}\to0$.

## Open / next

All three scoped follow-ups are now closed (2026-06-30):

- ~~Build the covariant interior kernel and re-verify the F62/F64 dynamic battery in the two-function regime.~~ **Done — [[F181-covariant-interior-kernel-battery]]** (`ca_interior_metric.py`, 9/9): two-function ($A,B$ independent, $AB\neq1$) TOV interior + exact-Schwarzschild exterior; sympy-exact that two functions source an isotropic perfect fluid where the single scalar forces $p_r=-p_t$ (F173); GR-TOV reproduced to the integrator floor; the F62/F64 battery (EP, redshift, factor-2 bend, backreaction) passes unchanged on the two-function background.
- ~~Re-issue Paper VII's strong-field section.~~ **Done — `papers/Paper-07-Gravity.md` §4 (Revision 3).** The dielectric $e^{2u}$ is now the vacuum/weak-field representation; the canonical strong-field object is exact Schwarzschild/Kerr from the induced Einstein equation; the horizon-free dielectric black hole (F114/Paper VIII) is reclassified as a PPN-order artifact.
- ~~Confirm cosmology.~~ **Done — [[F182-friedmann-pressure-cosmology]]** (`ca_cosmology.py`, 6/6): the full-tensor source gives $\ddot a/a=-(4\pi G/3)(\rho+3p/c^2)$ (forced by the Bianchi identity); radiation $a\propto t^{1/2}$, matter $a\propto t^{2/3}$; the energy-only law would have mis-weighted the radiation era by exactly a factor 2 ($q=1$ vs $\tfrac12$).

Remaining strong-field build-out: Kerr/frame-dragging ($T_{0i}$) on the two-function kernel; tabulated-EoS TOV for an absolute NICER placement.

## Files
- Decision note: `docs/theory/key-decisions.md` (2026-06-29 entry)
- This finding: `findings/F178-gravity-full-tensor-adoption.md`
