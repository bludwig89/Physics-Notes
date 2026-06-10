# SI Unit Adoption — Options, Constraints, and Relevant Derivations

**Date:** 2026-05-28 - 20:10
**Status:** Decision-support overview (no code change). Consolidates Finding 10 with the rotation-rate (F25/F26), mass-geometry (F46), and Lorentz-violation (F12/F15/F30) results that have landed since F10 was written.
**Cross-references:** [findings.md](findings.md) F10, F12, F13, F15; [findings/F25-real-rotation-exact-discrete-time-maxwell.md](findings/F25-real-rotation-exact-discrete-time-maxwell.md); [findings/F26-speed-of-light-as-rotation-rate.md](findings/F26-speed-of-light-as-rotation-rate.md); [findings/F30-photon-dispersion-order-anisotropy-birefringence.md](findings/F30-photon-dispersion-order-anisotropy-birefringence.md); [findings/F46-pythagorean-lattice-mass.md](findings/F46-pythagorean-lattice-mass.md); [first-gen-completeness.md](first-gen-completeness.md) calibration tier.

---

## 1. The problem in one paragraph

Every result in the model lives in **dimensionless lattice units** — cells per tick, radians per tick, and a dimensionless mass $m \in (0,1)$. Nothing in the dynamics references a metre, a second, or a kilogram. To compare an *absolute* lattice prediction against a measured SI quantity (a deflection angle in arcseconds, a Lorentz-violation energy in GeV, a particle mass in kg) the project must fix a mapping from the three lattice scales — cell spacing $a$, tick $\tau$, and the mass-rotation normalisation — to the three SI base units. **Three independent anchors are required**, and the model currently declares none. Finding 10 showed that the single most natural-looking anchor (Planck-cell identification) is internally inconsistent in any $d>1$; the findings since then add two more anchors we can use instead and one falsifiability bracket that constrains the choice.

---

## 2. What we actually need to fix

SI has three base units relevant here: the metre, the second, the kilogram. The lattice exposes exactly three knobs:

| Lattice knob | Fixes (with the constants below) | Natural anchor candidate |
|---|---|---|
| cell spacing $a$ | the metre | $\ell_P$, or a measured length scale |
| tick $\tau$ | the second | $t_P$, or $a/(c\sqrt d)$ |
| mass normalisation | the kilogram | a measured fermion mass (F46) |

and three fundamental constants that the mapping must reproduce: $c$, $\hbar$, and (if gravity is in scope) $G$. Choosing any **two** of $\{a,\tau\}$ plus **one** mass anchor over-determines the system unless the choices are made mutually consistent — which is exactly the tension Finding 10 surfaced.

---

## 3. Lattice constraints that bound the choice

These are hard, derived facts; any SI mapping has to respect them.

1. **Dimensionless light speed is fixed: $c_\text{lat} = 1/\sqrt d$.** On the 3D BCC lattice the model is built on, $d=3$, so $c_\text{lat} = 1/\sqrt 3$ (Findings 2/7, promoted to the exact-algebraic column). This is the group velocity of the unique Weyl QCA, in cells per tick. It is *not* adjustable.

2. **$a/\tau$ is the lattice lightcone, not the physical $c$.** One cell per tick is the maximum signal speed on the lattice. The physical light speed is the *rotation rate* $c_\text{lat}\cdot(a/\tau)$, not $a/\tau$ itself — this is the substance of **F25/F26**: $c$ is $d\Omega/d|\mathbf k|$, the angular rate at which the real $(\mathbf E,\mathbf B)$ pair rotates, not the speed of a propagating phase crest. Consequence: the physical metre/second pairing is
   $$c \;=\; \frac{a}{\tau}\cdot\frac{1}{\sqrt d}\qquad\Longrightarrow\qquad \frac{a}{\tau} \;=\; c\,\sqrt d \;\approx\; 5.196\times10^{8}\ \text{m/s in 3D.}$$
   This *is* Finding 10's resolution 3, and F26 makes it the physically motivated reading rather than a bookkeeping trick: the lightcone speed and the propagation speed were never supposed to be equal once $c$ is a rotation rate.

3. **Mass is also a rotation rate — a second, independent anchor (F46).** The Dirac dispersion obeys the spherical-Pythagorean identity $\cos\Omega_\text{Dirac} = \cos\Omega_\text{rest}\cos\Omega_\text{kin}$ with $\Omega_\text{rest}(m) = \arcsin(m)$. The dimensionless lattice mass maps to SI as
   $$m_\text{lat} \;=\; \frac{m_\text{phys}\,c\,a}{\hbar}\quad(\text{rest-frame radians per tick}).$$
   So once $a$ is chosen, every fermion mass is pinned, and *conversely a measured fermion mass can be used to fix $a$* without ever invoking the Planck length. At Planck-scale $a$, $m_\text{lat}(e^-)\approx 4\times10^{-23}$ — confirming the "$m\ll1$ at laboratory scales" regime that F12 relies on.

4. **Brillouin-zone UV cutoff.** Physical wavenumbers run only to $|\mathbf k|\sim\pi/a$; the absolute energy/momentum ceiling of any prediction scales as $1/a$. This is what converts the dimensionless Lorentz-violation curve into an SI energy scale (next section).

---

## 4. Derivations that should drive the decision

- **Finding 10 — the $\sqrt d$ mismatch.** Identifying $a=\ell_P$ **and** $\tau=t_P$ simultaneously forces $c_\text{phys}=c/\sqrt d$ — wrong by $\sqrt3\approx1.732$ in 3D. The factor is exact algebraic, same origin as the curl-residual $1/\sqrt{2d}$. So the naive "Planck cell + Planck tick" anchor is ruled out; at most one of the two may be Planck-valued.

- **F12 / F15 — the Lorentz-violation bracket (falsifiability gate).** The lattice carries an intrinsic deformation $\omega_\text{moving}/\omega_\text{static} = 1/\gamma_\text{SR} + \beta_\text{LV}(v/c)^2$, with the closed form $\beta_\text{LV}(m)=\tfrac12\big(1-\tfrac{m}{\sqrt{1-m^2}\arcsin m}\big)$ (negative for all $m$, $\approx -m^2/6$ at small $m$). Converting this to an SI energy via $1/a$ produces a predicted $E_\text{LV}$ that **must lie above the GRB time-of-flight bound $E_\text{LV}\gtrsim10^{19}$ GeV** (Fermi GRB 090510). This is the one place where the SI choice is *empirically* constrained rather than conventional: a small enough $a$ pushes $E_\text{LV}$ above the bound; too large an $a$ would already be falsified. Fixing $a$ at (or near) the Planck length comfortably clears the bound, so the bound is permissive but not vacuous.

- **F30 — birefringence is the live observable.** The net time-of-flight LV cancels between helicities ($n=2$, untestable), but linear **vacuum birefringence** survives on the BCC body diagonal: $\Delta v_\phi/c=-k/9$. Whatever fixes $a$ also fixes the photon energy at which this becomes observable in GRB/AGN polarisation — so the SI choice has a concrete experimental consequence here, not just in lensing magnitudes.

- **F13 — dimensionality sharpens, doesn't resolve.** The 3D-BCC continuum-SR gap is ~10× the 2D gap at equal $v/c$. Confirms $d=3$ BCC is the physically correct lattice to fix the mapping against, and that a $d=4$ check ($c_\text{lat}=1/2$) remains the one open algebraic continuation.

---

## 5. The options

All four respect constraint §3.1 ($c_\text{lat}=1/\sqrt3$). They differ in which anchors they adopt.

### Option A — Planck length, derived tick *(Finding 10 resolution 1)*
Set $a=\ell_P$, then $\tau = t_P/\sqrt d \approx 3.11\times10^{-44}\,$s (faster than the conventional Planck time by $\sqrt3$).
*Reading:* $\ell_P$ is the fundamental length; the tick is a derived, sub-Planck-time quantity.
*Pro:* keeps the cell at the most-cited fundamental length; clears the F12 GRB bound easily. *Con:* abandons the textbook $\tau=t_P$; the tick has no independent justification.

### Option B — Planck tick, derived cell *(Finding 10 resolution 2)*
Set $\tau=t_P$, then $a=\ell_P\sqrt d\approx2.80\times10^{-35}\,$m.
*Reading:* $t_P$ is the fundamental tick; the cell is $\sqrt3$ larger than $\ell_P$.
*Pro:* keeps the canonical tick. *Con:* a larger cell *lowers* the UV cutoff $1/a$ and so *lowers* the predicted $E_\text{LV}$ — needs an explicit re-check against the F12 GRB bound before adoption.

### Option C — Lightcone reinterpretation *(Finding 10 resolution 3, and the F25/F26-preferred reading)*
Keep $a/\tau$ as the **lightcone** speed (one cell/tick) and *define* the physical pairing by $c \equiv (a/\tau)/\sqrt d$. "Planck's $c$" becomes the lightcone speed $c\sqrt3\approx5.20\times10^8\,$m/s, which no particle reaches.
*Pro:* the only option that is conceptually forced rather than chosen — F26 already says $c$ is a rotation rate, not the lightcone, so this just names the metre/second pairing consistently. Requires no claim about which of $a,\tau$ is "fundamental." *Con:* retires the convention $\ell_P/t_P=c$; needs a clear statement that the lattice lightcone exceeds $c$.

### Option D — Empirical (non-Planck) anchoring *(uses F46)*
Drop the Planck assumption entirely. Fix the three anchors from measured constants: $c$ (defines $a/\tau=c\sqrt3$), $\hbar$, and one fermion mass via $m_\text{lat}=m_\text{phys}ca/\hbar$ (F46). This leaves $a$ as the single free scale, then fixes it by the highest available constraint — either the F12 GRB bound (sets a floor on $1/a$) or, if gravity is in scope, by matching $G$ through the L4 EMQG sector.
*Pro:* every input is a measured number; the model predicts rather than assumes the Planck scale. The mass anchor is a genuinely new lever that did not exist when F10 was written. *Con:* defers a clean answer until the EMQG/gravity fork (`ca-dirac-gravity-plan.md`) gives a second absolute constraint to pin $a$ independently of $c$.

---

## 6. Recommendation for discussion

Adopt **Option C as the conceptual frame** (it is the only one F25/F26 actually forces) and **Option D as the operational procedure** for producing SI numbers, treating $a$ as a single runtime parameter rather than a hard-coded Planck value. Concretely:

1. Declare $a/\tau = c\sqrt3$ as the lattice lightcone identity (Option C), so $c_\text{phys}=c$ comes out automatically from $c_\text{lat}=1/\sqrt3$.
2. Carry $a$ as an explicit parameter (default $\ell_P$, but free), and derive every SI quantity — masses (F46), $E_\text{LV}$ (F12), birefringence onset (F30), lensing magnitude (L4) — as functions of $a$.
3. Use the F12 GRB bound as a one-sided check ($E_\text{LV}(a)\gtrsim10^{19}$ GeV) and the eventual gravity fork as the independent constraint that finally pins $a$.

This keeps every existing dimensionless result untouched (they are, per Finding 10, unaffected), makes the SI factor explicit and auditable, and uses the two anchors (rotation-rate $c$, mass-rotation $m$) that the model has *derived* rather than the Planck identification it merely *assumed*.

---

## 7. What stays open

- No first-principles derivation of $a$ itself — all options still need one external constraint (GRB bound floor, or a $G$-match from the EMQG/gravity fork) to fix the last scale.
- $d=4$ continuation ($c_\text{lat}=1/2$) is unverified in code; only $d\in\{2,3\}$ are closed (F13).
- The absolute L4 lensing coefficient $\Delta\theta=4GM/(bc^2)$ has not been checked against the lattice value; it is the natural second constraint for Option D and carries the $\sqrt d$ factor explicitly (Finding 10, "what changes").
