# Roadmap — Implementing $W_\mu$ as a Dynamical SU(2) Gauge Boson

**Date:** 2026-05-23 - 20:00
**Status:** Drafted, no phases started
**Closes:** F27 known limitation #1 (kinetic step not SU(2)-invariant without $W_\mu$); F29 known limitation (kinematic-only bridge)
**Linked findings:** F26 (rotation law), F27 (chiral SU(2)), F29 (W-triplet bilinear bridge)

---

## Why $W_\mu$ now

F27 confirmed chiral SU(2)$_L$ is a local gauge symmetry of the complex-mass coupling — but explicitly noted that the kinetic step is **not** SU(2)-invariant without $W_\mu$. F29 confirmed the kinematic bridge: a W-triplet bilinear built on the same Weyl primitives inherits F26's photon rotation law per component. Both findings end at the same wall: until $W_\mu$ exists as a dynamical field with its own propagation, self-coupling, and fermion vertex, the SU(2) sector remains kinematic.

This roadmap promotes $W_\mu^a$ from "implicit pure-gauge $U(x)$" (F27) and "bilinear-level triplet" (F29) to a first-class dynamical field on the BCC lattice with the same exactness standards as the photon and Weyl spinors.

---

## Design Commitments

1. **BCC lattice substrate.** Same 3D body-centered cubic lattice the photon and Weyl spinors live on. No new lattice.
2. **Link variables.** Store $W_\mu^a$ as $\mathrm{SU}(2)$ link elements $U_\ell = \exp\!\left(i\,\tau^a W_\ell^a / 2\right)$ on each BCC nearest-neighbor link. 8 links per site; 3 real components per link → 24 d.o.f. per site for the gauge field.
3. **Exactness goal.** Match F26/F27 standard: gauge-invariance Ward identities to machine precision; W dispersion to algebraic exactness in the small-$k$ / massless limit.
4. **Reuse F26 rotation law.** The free W propagation per $a$-component should reduce to F26's rotation law (verified at the bilinear level in F29 B5).
5. **No premature Higgs.** Defer the Higgs/Φ-condensate question to Phase 5; first three phases produce a massless W field.
6. **Gauge-invariance regressions.** Every phase ships with a Ward-identity test that holds to ≤ 10⁻¹⁴.

---

## Phase 1 — Link Variables & Covariant BCC Hopping

**Goal:** introduce $U_\ell \in \mathrm{SU}(2)$ on BCC links and a covariant Weyl step that preserves unitarity and reduces to the existing `weyl_step_3d_bcc` when $U_\ell = I$.

**Files to add:**
- `ca-simulation/ca_wmu.py` — new module
  - `make_w_link_field(L, mode='identity'|'random'|'pure_gauge')` — initialise link variables on all 8 BCC link directions
  - `link_unitarity_residual(U_links)` — return $\max\|U_\ell^\dagger U_\ell - I\|$
  - `covariant_weyl_step_3d_bcc(f, g, U_links)` — real-space hop along BCC links with $U_\ell$ insertion
  - `gauge_transform_links(U_links, V_x)` — $U_\ell \to V_{x'} U_\ell V_x^\dagger$
- `model-tests/test_wmu_phase1.py` — see Tests below

**Mathematical core:**

The covariant BCC walk is the real-space form of the same unitary that `weyl_step_3d_bcc` applies spectrally, but with parallel transport on each leg. For a single BCC half-step in direction $\hat e_\alpha$:

$$\psi'(x) = \sum_{\alpha} c_\alpha\, U_{\ell(x, x+\hat e_\alpha)}\, \psi(x + \hat e_\alpha)$$

where $c_\alpha$ are the BCC coin coefficients (Paper 1 Eq. 14). Under gauge transformation $\psi \to V(x)\psi$ and $U_\ell \to V(x')\, U_\ell\, V(x)^\dagger$, the covariant step is exactly invariant.

**Tests (target residuals):**

| ID | Test | Target |
|----|------|--------|
| W1.1 | Link unitarity preserved under random initialisation | $\le 10^{-15}$ |
| W1.2 | Covariant step reduces to `weyl_step_3d_bcc` when $U_\ell = I$ | $\le 10^{-15}$ |
| W1.3 | Norm conservation over 100 covariant steps, random $U_\ell$ field | $\le 10^{-13}$ |
| W1.4 | Local SU(2)$_L$ Ward identity: $V(x)\cdot\mathrm{step}(\psi;U) = \mathrm{step}(V\cdot\psi; V\cdot U \cdot V^\dagger)$ | $\le 10^{-14}$ |
| W1.5 | Closes F27 known limitation: kinetic step + complex-mass step jointly SU(2)-invariant with $W_\mu$ | $\le 10^{-14}$ |

**Documentation:** `findings/F30-wmu-covariant-hopping.md`; exactness-inventory Tier 1 entries 66–68; project-status and changelog entries.

**Risks:**
- Spectral BCC step → real-space hop is a substantial refactor; performance will drop from $O(L^3 \log L)$ (FFT) to $O(L^3)$ per step, but with smaller prefactor. Manageable for $L \le 64$.
- Coin-coefficient assignment per BCC link direction needs care (the BCC two-tick walk uses 8 links, not 6).

---

## Phase 2 — Free W Propagation (Rotation Law per $a$-Component)

**Goal:** the W field obeys F26's rotation law in the small-amplitude / linearised limit. Build the W-field's free EM-style propagation and confirm $\Omega(k) = 2\omega_\text{BCC}(k/2)$ per $a$-component.

**Files to add/modify:**
- `ca_wmu.py`:
  - `extract_EW_BW(U_links)` — extract $(E_W^a, B_W^a)$ from the link field in the linearised limit (small $W$, $U_\ell \approx I + i\tau^a W_\ell^a/2$)
  - `w_propagation_step_spectral(E_W, B_W)` — apply F26 rotation law per $a$ ($a = 1, 2, 3$ independently)
  - `w_free_dispersion_check(...)` — measure $\Omega_W(k)$ from a plane-wave initial condition; compare to $2\omega_\text{BCC}(k/2)$
- `model-tests/test_wmu_phase2.py`

**Mathematical core:** in the linearised (small $W$) limit, each $W^a$ is a free spin-1 field on the BCC lattice. By F29 B5, each component obeys F26's rotation law:

$$\begin{pmatrix} \hat E_W^a(k, t+1) \\ \hat B_W^a(k, t+1) \end{pmatrix} = \begin{pmatrix} \cos\Omega & \sin\Omega \\ -\sin\Omega & \cos\Omega \end{pmatrix} \begin{pmatrix} \hat E_W^a(k, t) \\ \hat B_W^a(k, t) \end{pmatrix}, \quad \Omega(k) = 2\omega_\text{BCC}(k/2)$$

**Tests:**

| ID | Test | Target |
|----|------|--------|
| W2.1 | $\Omega_W(k) = 2\omega_\text{BCC}(k/2)$ across all 3 $a$-components | machine ε per F26 |
| W2.2 | $\|E_W^a\|^2 + \|B_W^a\|^2$ conserved per $a$ over 200 steps | $\le 10^{-13}$ |
| W2.3 | Transversality residual scales as $c_\text{lat}\,k$ (linearisation, F2/F26) | structural, matches photon |
| W2.4 | Free W reduces to triplet of decoupled photons in the abelian (small-$W$) limit | $\le 10^{-15}$ |

**Documentation:** `findings/F31-wmu-free-propagation.md`; exactness-inventory Tier 1 (~3 entries); project-status entry.

**Risks:** translating the link-variable representation into linearised $(E_W^a, B_W^a)$ correctly. The factor-of-2 and basis conventions must match F26/F29 exactly so that the rotation law applies without rescaling.

---

## Phase 3 — Non-Abelian Self-Coupling (Yang–Mills)

**Goal:** add the commutator term that distinguishes Yang–Mills from three copies of QED. Without it, W's are decoupled photons; with it, they self-interact.

**Files to add/modify:**
- `ca_wmu.py`:
  - `plaquette_field_strength(U_links)` — compute $F_{\mu\nu}^a$ from BCC plaquettes (Wilson plaquette form)
  - `w_self_interaction_step(U_links)` — non-abelian update including $[W, W]$ contribution
  - `bianchi_residual(F)` — verify $D_{[\mu} F_{\nu\rho]}^a = 0$
- `model-tests/test_wmu_phase3.py`

**Mathematical core:**

$$F_{\mu\nu}^a = \partial_\mu W_\nu^a - \partial_\nu W_\mu^a + g\,\epsilon^{abc} W_\mu^b W_\nu^c$$

On the lattice, use Wilson plaquettes:

$$P_{\mu\nu}(x) = U_\mu(x)\,U_\nu(x + \hat e_\mu)\,U_\mu^\dagger(x + \hat e_\nu)\,U_\nu^\dagger(x) \approx I + i g a^2 \tau^a F_{\mu\nu}^a + O(a^4)$$

**Tests:**

| ID | Test | Target |
|----|------|--------|
| W3.1 | $[W, W]$ vanishes when $W^a$ has only one non-zero component (no self-coupling for U(1)) | $\le 10^{-15}$ |
| W3.2 | Bianchi identity $D_{[\mu} F_{\nu\rho]}^a = 0$ on Wilson plaquettes | $\le 10^{-13}$ |
| W3.3 | Total energy $\sum_a \int (\|E_W^a\|^2 + \|B_W^a\|^2)$ conserved with self-coupling on | $\le 10^{-12}$ |
| W3.4 | Total SU(2) charge $T^a$ conserved (Noether for global SU(2)) | $\le 10^{-13}$ |
| W3.5 | Gauge-invariance of plaquette $P_{\mu\nu}$ under local SU(2) | $\le 10^{-14}$ |

**Documentation:** `findings/F32-wmu-yang-mills-self-coupling.md`; Tier 1 (~4 entries); project-status.

**Risks:**
- Energy conservation with self-coupling typically requires implicit / symplectic integrators. May need a Strang-split between free and self-interaction terms.
- BCC plaquettes are not the simple cubic plaquettes — must enumerate the BCC fundamental closed loops carefully. Defer until W2 is solid.

---

## Phase 4 — Fermion–$W_\mu$ Vertex (Covariant Derivative)

**Goal:** couple the SU(2) doublet $\psi = (\nu_L, e_L)$ to $W_\mu$ via the covariant derivative $D_\mu = \partial_\mu - i g \tau^a W_\mu^a / 2$, closing F27's known limitation #2.

**Files to add/modify:**
- `ca-simulation/ca_dirac.py`:
  - Extend `dirac_step_complex_mass_doublet` to accept a `U_links` argument and use Phase 1's covariant hopping for the kinetic step
- `ca_wmu.py`:
  - `fermion_current_isospin(psi_doublet)` — compute $J^{a,\mu} = \bar\psi \gamma^\mu \tau^a \psi$ at the bilinear level (reusing F29 W-triplet construction)
- `model-tests/test_wmu_phase4.py`

**Mathematical core:**

$$\mathcal{L}_{\psi W} = -g\, J^{a,\mu}\, W_\mu^a, \qquad J^{a,\mu} = \bar\psi_L \gamma^\mu \tau^a \psi_L$$

For chiral SU(2)$_L$, the current is left-handed only ($\eta$ sector). The fermion current sources the W field via:

$$\partial_\mu F^{a,\mu\nu} + g\, \epsilon^{abc} W_\mu^b F^{c,\mu\nu} = g\, J^{a,\nu}$$

**Tests:**

| ID | Test | Target |
|----|------|--------|
| W4.1 | Full kinetic + mass + W-coupled step is locally SU(2)$_L$ invariant (closes F27 limitation #2) | $\le 10^{-14}$ |
| W4.2 | Fermion current $J^{a,\mu}$ is conserved (continuity equation) when $g = 0$ | $\le 10^{-14}$ |
| W4.3 | Right-handed $\chi$ does not couple to $W_\mu$ (parity violation) | $= 0$ exact |
| W4.4 | $W^\pm$ vertex changes isospin: $\nu_L + W^- \to e_L$ produces $e_L$ to machine precision | $\le 10^{-13}$ |
| W4.5 | Energy conservation across full coupled system over 100 steps | $\le 10^{-12}$ |

**Documentation:** `findings/F33-wmu-fermion-vertex.md`; Tier 1 (~5 entries); project-status; **explicit retirement of F27 limitations #1 and #2 in `findings.md`**.

**Risks:**
- Strang-splitting the full $\psi$-$W$ coupled stepper may not preserve unitarity / gauge invariance simultaneously. Consider midpoint or Cayley schemes (parallel to F3b).
- Coupling constant $g$: project chooses lattice convention; document the dimensionful relation $g_\text{lat} \leftrightarrow g_\text{SM}$.

---

## Phase 5 — W Mass Generation (Higgs vs Ludwig $U(x)$)

**Goal:** generate $m_W$ without breaking gauge invariance. **Open question:** does F27's pure-gauge $U(x)$ admit a dynamical promotion that yields W mass, or do we need a Higgs doublet $\Phi$?

**Two paths to test:**

### Path 5A — Standard Higgs mechanism
- Add complex Higgs doublet $\Phi = (\phi^+, \phi^0)^T$ with potential $V(\Phi) = -\mu^2 \Phi^\dagger \Phi + \lambda (\Phi^\dagger \Phi)^2$
- VEV $\langle\Phi\rangle = (0, v/\sqrt 2)^T$
- Covariant kinetic $|D_\mu \Phi|^2$ → $W$ mass term $\tfrac{1}{4} g^2 v^2\,W^a_\mu W^{a,\mu}$ (after diagonalisation)

### Path 5B — Promote F27 $U(x)$ to dynamical
- F27's $U(x)$ was demonstrated pure-gauge (no physical d.o.f.). Test whether a dynamical $U(x)$ with kinetic term $|\partial_\mu U|^2$ (chiral Lagrangian style) generates W mass without a separate $\Phi$ field.
- This is the "Stueckelberg / nonlinear sigma" approach — known in SM literature but tested here in the CA setting.

**Files to add:**
- Path 5A: `ca-simulation/ca_higgs.py` (already exists; extend with doublet) and `ca_wmu.py::wmu_mass_higgs`
- Path 5B: `ca_wmu.py::wmu_mass_stueckelberg`
- `model-tests/test_wmu_phase5_higgs.py`, `test_wmu_phase5_stueckelberg.py`

**Tests (both paths):**

| ID | Test | Target |
|----|------|--------|
| W5.1 | Massive W dispersion $\omega^2 = m_W^2 + c_\text{lat}^2 \|k\|^2$ at small $k$ | $\le 10^{-12}$ rel err |
| W5.2 | Three massive d.o.f. per $W^a$ (longitudinal mode acquired) | structural |
| W5.3 | Gauge invariance preserved: $m_W$ unchanged under random $V(x)$ transformation | $\le 10^{-14}$ |
| W5.4 (5A only) | $m_W = \tfrac{1}{2} g v$ (algebraic relation) | exact |
| W5.5 (5B only) | $U(x)$ acquires kinetic term, F27's "pure gauge" status modified | structural |

**Documentation:** `findings/F34a-wmu-mass-higgs.md` and `F34b-wmu-mass-stueckelberg.md`; **comparison table** of paths.

**Risks:**
- Two paths run in parallel — pick winner based on which generates simpler exactness inventory, not theoretical taste.
- F27's strong result (mass gap *without* Higgs at the complex-mass level) hints that 5B may be natural for this model. But promoting $U(x)$ to dynamical may re-introduce a "scalar in disguise".

---

## Phase 6 — Electroweak Mixing ($W^3 \leftrightarrow B \leftrightarrow \gamma$)

**Goal:** introduce $U(1)_Y$ hypercharge gauge field $B_\mu$, mix with $W^3_\mu$ at the Weinberg angle, recover the **photon as the massless eigenvector** $\gamma = \cos\theta_W\, B + \sin\theta_W\, W^3$. This is where the photon constructed in `ca_maxwell.py` reconnects with the W sector.

**Files to add:**
- `ca-simulation/ca_hypercharge.py` — $U(1)_Y$ link variables, photon-like rotation law
- `ca_wmu.py::weinberg_mix(W3_field, B_field, theta_W)` — diagonalise the $W^3$-$B$ mass matrix
- `model-tests/test_wmu_phase6.py`

**Mathematical core:**

After EW symmetry breaking:

$$\begin{pmatrix} A_\mu \\ Z_\mu \end{pmatrix} = \begin{pmatrix} \cos\theta_W & \sin\theta_W \\ -\sin\theta_W & \cos\theta_W \end{pmatrix} \begin{pmatrix} B_\mu \\ W^3_\mu \end{pmatrix}$$

with $m_\gamma = 0$, $m_Z = m_W / \cos\theta_W$.

**Tests:**

| ID | Test | Target |
|----|------|--------|
| W6.1 | $A_\mu$ massless after diagonalisation | $\le 10^{-15}$ |
| W6.2 | $A_\mu$ recovers the F26 photon: dispersion $\Omega(k) = 2\omega_\text{BCC}(k/2)$ | machine ε |
| W6.3 | $m_Z / m_W = 1/\cos\theta_W$ to algebraic exactness | $\le 10^{-14}$ |
| W6.4 | Electric charge $Q = T_3 + Y/2$ for ν (Q=0), e (Q=−1) | exact |
| W6.5 | F26 photon construction (transverse Weyl bilinear) agrees with mixed-eigenvector photon | $\le 10^{-13}$ |

**Documentation:** `findings/F35-electroweak-mixing.md`; this finding **completes the photon-to-W bridge** and explicitly closes F29's known limitation re: hypercharge mixing.

**Risks:**
- $\theta_W$ is an input parameter in SM. Test whether the CA structure constrains it (it likely does not at this stage, but the question is worth posing).
- The F26 photon was constructed from Weyl bilinears without any hypercharge sector. Verifying agreement between the two constructions is the central physics check.

---

## Phase Dependencies & Sequencing

```
Phase 1 ─┬─→ Phase 2 ─┬─→ Phase 3 ──→ (W self-interaction validated)
         │            │
         │            └─→ Phase 4 ──→ (closes F27 limitations)
         │                  │
         └─→ ────────────── ┘
                            │
                            ├─→ Phase 5A (Higgs) ──┐
                            │                      ├─→ Phase 6
                            └─→ Phase 5B (Ludwig) ─┘
```

Phase 1 is the foundation — covariant hopping must work before anything else. Phases 2 and 4 can be developed in parallel after Phase 1. Phase 3 (self-coupling) can wait until 2 is solid. Phase 5 has two parallel paths; pick winner before starting Phase 6.

---

## Estimated Effort

| Phase | Lines of code (est.) | Test runtime | Sandbox-compatible? |
|-------|----------------------|--------------|---------------------|
| 1 | ~400 | < 5 s | Yes |
| 2 | ~300 | < 5 s | Yes |
| 3 | ~500 | 10–30 s | Yes |
| 4 | ~400 | < 10 s | Yes |
| 5 | ~600 (both paths) | 20–60 s | Borderline; may need user-run script |
| 6 | ~400 | < 10 s | Yes |

Sandbox cap is 45 s — Phase 5 should be split into smaller test scripts or provide a user-run version per CLAUDE.md guidance.

---

## Exactness-Inventory Forecast

Conservative estimate of new Tier-1 entries by phase: Phase 1 (3), Phase 2 (3), Phase 3 (4), Phase 4 (5), Phase 5 (3–5), Phase 6 (4). Approximately **22–24 new exact algebraic results** when complete.

Current count: 65. Forecast post-roadmap: **~88**.

---

## Decision Points Pending User Input

1. **Phase 5 path preference?** Start with Higgs (5A, standard) or with Stueckelberg/Ludwig (5B, novel)? Recommendation: 5B first — it tests a distinctive prediction of the F27 framework. Fall back to 5A if 5B fails.
2. **Coupling constant $g$ convention.** Use $g_\text{lat} = 1$ (CA-natural) or match $g_\text{SM} \approx 0.65$? Recommendation: $g_\text{lat} = 1$ initially; calibrate to SM only in Phase 6.
3. **Real-space vs spectral hopping in Phase 1.** Real-space is gauge-invariant by construction; spectral is faster. Recommendation: real-space, accept performance hit for cleanliness.

---

## Cross-references

- `findings/F26-speed-of-light-as-rotation-rate.md` — rotation law W will inherit
- `findings/F27-complex-mass-chiral-su2.md` — chiral SU(2) limitations this roadmap closes
- `findings/F29-w-triplet-bilinear-su2-bridge.md` — kinematic bridge this roadmap promotes to dynamical
- `roadmap-f26-rotation.md` — sibling roadmap (F26 adoption)
- `reference-research/ca-electroweak-design.md` — earlier design notes
