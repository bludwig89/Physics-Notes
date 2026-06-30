# F167 — Rest mass derived from the QCA rule: it is the unique, unitarity-and-symmetry-forced zero-wavenumber rotation rate of the rule's generator — the same generator whose low-k slope is c_lat (closing the structural half of audit G1)

**Date:** 2026-06-29 - 18:05
**Numbering:** max existing is F166 (`F166-triple-gluon-vertex-branch-blind`, this session) alongside the concurrent F165 (`F165-hypercharge-quantisation-...`); this is **F167**. Re-checked before numbering per the concurrent-session caution.
**Status:** Confirmed — 6/6 checks (5 exact / structural-zero, 1 scope). Closes the **structural** half of audit G1 (Physics Audit Report 2026-06-29): rest mass is *derived*, not posited — it is the unique admissible zero-k deformation of the rule, forced by unitarity + lattice/spin symmetry, and it is the k=0 eigen-rotation of the same generator whose low-k slope is c_lat. The **magnitude** of m stays open (F119 overall-scale no-go), now sharply separated.
**Script:** `tests/findings/test_F167_restmass_from_rule.py`
**Results:** `test-results/F167_restmass_from_rule.json`
**Cross-references:** [[F46-pythagorean-lattice-mass]] (the spherical-Pythagoras identity and Ω_rest=arcsin m, which this re-reads as a derivation rather than an identification), [[F27-complex-mass-chiral-su2]] (the mass step whose m this finding shows is the *unique* physical parameter; T3/T4 = the chiral-phase pure-gauge result at k=0), [[F26-bcc-spin-axis]]/[[F25]] (c_lat = dΩ/d\|k\| at k→0, the slope half of the bridge), [[F105-axial-photon-exactly-dispersionless]] (on-axis exact linearity Ω=\|k\|/√3 used in T5), [[F119-kg-scale-three-routes]] (the overall-scale no-go = the open magnitude half), [[F120-electron-calibrated-spectrum]]/[[F121-tau-anchored-canonical-spectrum]] (spectrum *shape* from the locked cell; the anchor that fixes the scale). Modules: `ca-simulation/ca_bcc.py`, `ca-simulation/ca_dirac.py`.

---

## The question (audit G1)

The Physics Audit Report (2026-06-29, logical gap **G1**) stated:

> F26 establishes $c_\text{lat}=d\Omega/d|k|$ at $k\to0$. The mass $m$ enters through the F27 mass step $\cos(m\,dt)\,\mathbf I+i\sin(m\,dt)\,A$, where $m$ is a free parameter. F46 provides the geometric identity $E^2=p^2c^2+m^2c^4$, but this is an **identification, not a derivation**. The gap: "$c_\text{lat}$ is a rotation rate" → "rest mass is the zero-$k$ rotation rate" is **conceptual, not algebraic**.

G1 conflates two questions that this finding separates:

1. **Structural** — *is mass forced by the rule, and is it forced to be a rotation rate?* (the conceptual→algebraic gap)
2. **Magnitude** — *what is the value of $m$?* (the hierarchy / overall-scale problem)

This finding **closes #1 algebraically** and **sharpens #2 as the genuinely open part**.

## The derivation

### Step 1 — the mass term is the *unique* admissible deformation (mass is forced)

The single-tick Dirac update in Fourier space is the $4\times4$ unitary

$$D_k=\begin{pmatrix} n\,W_k & i m\,\mathbf I_2\\ i m\,\mathbf I_2 & n\,W_k^\dagger\end{pmatrix},\qquad W_k\ \text{the Weyl unitary}.$$

**Unitarity forces the kinetic rescale (T1).** Once the rule inserts a $k$-independent chirality coupling of strength $m$ (the off-diagonal block $i m\,\mathbf I_2$), the *only* diagonal rescale that keeps $D_k$ unitary is $n=\sqrt{1-m^2}$, i.e. $n^2+m^2=1$. This is not a modelling choice — any other $n$ breaks $D_k^\dagger D_k=\mathbf I$ (verified: correct $n$ gives residual $2\times10^{-16}$; a $5\%$-wrong $n$ gives $\sim0.1$).

**Symmetry forces uniqueness (T2).** Among the 16 Hermitian Dirac covariants, a *rest* (k-independent) term that can gap the spectrum must be (a) **chirality-off-diagonal** — it must anticommute with $\gamma^5$ to couple $\eta\leftrightarrow\chi$ — and (b) a **spin-rotation scalar** — it must commute with the spin generators $\Sigma_i=\tfrac12\mathrm{diag}(\sigma_i,\sigma_i)$, so it survives at rest without breaking $SO(3)$. Exactly **two** of the sixteen satisfy both:

| covariant | chirality-off-diag (anticommute $\gamma^5$) | spin-scalar (commute $\Sigma_i$) | role |
|---|---|---|---|
| $\gamma^0$ (scalar) | ✓ | ✓ | **physical mass** $m$ |
| $\gamma^0\gamma^5$ (pseudoscalar) | ✓ | ✓ | chiral phase $\theta$ (pure gauge) |
| $\gamma^i,\ \gamma^i\gamma^5$ | ✓ | ✗ (carry a spin index → kinetic, need $k$) | propagation |
| $\mathbf I,\ \gamma^5,\ \sigma^{\mu\nu}$ | ✗ (chirality-diagonal) | — | not a mass |

So the rule admits **exactly one physical mass parameter** (plus one pure-gauge phase). Mass *exists* and is *unique* — derived from the rule's unitarity and symmetry, not posited as an arbitrary structure. (The vector terms $\gamma^i$ are excluded as rest terms precisely because they carry a spin index; they are the kinetic Weyl walk, odd in $k$, vanishing at $k=0$.)

### Step 2 — rest mass *is* the zero-k rotation rate (T3)

At $k=0$, $W_0=\mathbf I$ (no propagation), so the rest map is

$$D_0=n\,\mathbf I_4+i m\,\gamma^0=\exp\!\big(-i\,\Omega_\text{rest}\,A\big),\qquad A^2=\mathbf I,$$

with eigen-phases $\pm\Omega_\text{rest}$ and

$$\boxed{\ \Omega_\text{rest}(m)=\arcsin m,\qquad \cos\Omega_\text{rest}=\sqrt{1-m^2}=n.\ }$$

The zero-wavenumber eigen-rotation of the unique deformation *is* the rest mass. This is the F46-P6 limit, but here it is the **conclusion of the derivation**, not an identification: given Steps 1–2, rest mass *must* be a rotation rate because it is the $k=0$ value of the rule's eigen-phase.

### Step 3 — the chiral phase is pure gauge (T4)

The pseudoscalar partner $\gamma^0\gamma^5$ enters as a phase $\theta$ on the complex mass $m\,e^{i\theta}$. The rest eigen-phase is **independent of $\theta$** (max deviation $2.2\times10^{-16}$ over $\theta\in\{0,0.7,\pi/3,1.9\}$) — the F27 T3/T4 dispersion-invariance, replayed at $k=0$. So only the magnitude $m$ is physical.

### Step 4 — c_lat and rest mass are one generator (T5, the bridge G1 names)

On the real BCC rule the full dispersion is one function of one generator,

$$\Omega_\text{Dirac}(\mathbf k,m)=\arccos\!\big(\sqrt{1-m^2}\,u(\mathbf k)\big),$$

and the two "constants" are two readouts of it:

$$\underbrace{\Omega_\text{Dirac}(0,m)=\arcsin m}_{\textbf{intercept = rest mass}},\qquad \underbrace{\frac{d\Omega_\text{Dirac}}{d|\mathbf k|}\bigg|_{\mathbf k\to0,\,m=0}=\frac1{\sqrt3}=c_\text{lat}}_{\textbf{slope}}.$$

(Verified to $<10^{-12}$; the slope uses on-axis exact linearity $\Omega=|\mathbf k|/\sqrt3$, F105.) **"$c_\text{lat}$ is a rotation rate" and "rest mass is the zero-$k$ rotation rate" are the same statement about the same generator — its slope and its intercept.** The conceptual gap G1 names is closed algebraically; F46's spherical-Pythagoras $\cos\Omega_\text{Dirac}=\cos\Omega_\text{rest}\cdot\cos\omega_\text{kin}$ is the law that joins them on one triangle.

### Step 5 — dimensional rest energy

Restoring the lattice clock $dt$ and $\hbar$, $E(\mathbf k)=(\hbar/dt)\,\Omega_\text{Dirac}$, so the rest energy is

$$E_0=\frac{\hbar}{dt}\,\arcsin m\ \xrightarrow[m\ll1]{}\ \frac{\hbar}{dt}\,m,\qquad m_\text{phys}=\frac{E_0}{c^2},$$

i.e. the dimensionless rule parameter $m$ maps to physical mass through the lattice clock $\hbar/dt$ and $c$. The continuum $E^2=p^2c^2+m^2c^4$ (F46 §3.4) is the small-leg limit of the same identity.

## What this settles, and what it does not (the honest split of G1)

**Closed (structural half of G1):** that rest mass *exists*, is *unique* (one physical parameter, T1–T2), is *a rotation rate*, equals the zero-k eigen-phase $\arcsin m$ (T3), is free of the pure-gauge phase (T4), and shares **one generator** with $c_\text{lat}$ as intercept-vs-slope (T5). The "conceptual, not algebraic" objection is answered: the bridge is now algebra.

**Open (magnitude half of G1, T6):** the *value* of $m$ is **not** fixed by the *bare* rule — every $m\in(0,1)$ gives an equally-unitary admissible rule (T6, unitarity residual $2\times10^{-16}$ across $m\in\{0.05,\dots,0.999\}$). The spectrum *shape* (mass ratios) is the locked-cell result (F120/F121, F92/F76); the overall scale needs a dynamical mass-generation mechanism or an external anchor. This finding does not claim to close that; it sharpens it by proving everything *except* the magnitude is forced.

> **Update (2026-06-29):** "bare rule leaves $m$ free" does **not** mean the magnitude is underivable. The *dynamics* of the rule's derived strong coupling fixes the overall scale: **F144 lands $N$ to a factor ~1.9 with no tuning** via dimensional transmutation ($N\sim e^{-1/(2b_0\alpha_0)}$, $\alpha_0=1/16\pi$ rule-fixed), answering F119's "no marginal channel." So T6 should be read as "the *bare* rule leaves $m$ free; the running of the rule's strong coupling then fixes the scale up to a lattice scheme constant." See the deep-research roadmap `docs/roadmaps/mass-magnitude-derivation-2026-06-29.md` for the full route analysis (F144 transmutation + the residual scheme constant F162/F163 + the lepton↔colour scale link).

## Checks

| # | Check | Result | Tier |
|---|---|---|---|
| T1 | unitary completion forces $n^2+m^2=1$ (residual $2\times10^{-16}$; wrong $n$ → $\sim0.1$) | PASS | exact |
| T2 | exactly 2 of 16 Dirac covariants are k-indep + chirality-off-diag + spin-scalar → unique mass | PASS | exact (group theory) |
| T3 | rest eigen-phase $=\arcsin m$, $\cos\Omega_\text{rest}=\sqrt{1-m^2}$ | PASS | exact |
| T4 | rest eigen-phase independent of chiral phase $\theta$ (pure gauge) | PASS | exact ($2.2\times10^{-16}$) |
| T5 | $c_\text{lat}$ (slope) and rest mass (intercept) of one $\Omega_\text{Dirac}(\mathbf k,m)$ | PASS | exact ($<10^{-12}$) |
| T6 | magnitude of $m$ free — every $m\in(0,1)$ unitary (F119 no-go) | PASS | scope |

## Relation to prior findings

F46 proved the *dispersion identity* taking the Dirac block $D_k$ (mass inserted) as given. F167 proves the prior step G1 actually demanded: that the mass term is **forced and unique** (not an optional insert), and reframes $\Omega_\text{rest}=\arcsin m$ as the *derivation* of "rest mass is a rotation rate," unified with $c_\text{lat}$ on one generator. It does not supersede F46; it supplies the missing "why the mass step at all" link and the explicit $c_\text{lat}$↔$m$ bridge.

## Open / next

- **Magnitude (the remaining half of G1):** derive $m$ from a dynamical mechanism rather than an anchor — the natural target is the binding/condensate sector (F73 mass cap, F82 saturation, F92 fixed point) feeding the overall scale, closing the F119 no-go. High value, hard.
- **Quartic/anisotropy corrections:** the $O(\text{lattice}^4)$ deviation from $\arcsin m\oplus c_\text{lat}|\mathbf k|$ is F46 §3.4; a directional map of where the single-generator picture first deviates from Einstein dispersion would quantify the lattice signature of rest mass.

## Files
- Test: `tests/findings/test_F167_restmass_from_rule.py`
- Results: `test-results/F167_restmass_from_rule.json`
- Operators exercised: `ca_bcc._bcc_uvec`/`bcc_dispersion`; Dirac covariants built in-test from the Weyl-basis $\gamma$-matrices; cross-checks against `ca_dirac` mass-step structure.
