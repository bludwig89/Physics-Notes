# Electroweak Mass-Generation Design under Unified v2

*Design note. Sources: `ca-unified-v2.md` (the four-layer v2 stack and substitutions S1–S5), `ostoma-trushyk-1999-summary.md` (the EMQG three-mass framework). Does not modify any phase test; reorganises what v2 already proposes so that the mass-generating couplings are visible side-by-side.*

*Drafted 2026-05-17.*

---

## 1. Why an electroweak-specific design note

v2 (`ca-unified-v2.md`) decouples two jobs that v1 had collapsed onto one field: the Higgs scalar $\Phi$ keeps the fermion-mass job (Yukawa, S4), and a separate EMQG vacuum potential $\phi$ takes over the metric job (S1, Paper 6 Eq. 19.7). The composite-photon construction (S3, Paper 1 Eq. 35) replaces the externally-imposed U(1) phase as the canonical electromagnetic sector. Each of these three substitutions touches "mass" in a different way, but v2 itself does not lay them out as alternatives — it presents them as parallel mechanisms in different layers.

This note pulls them out into the three concrete paths through which something in v2 acquires the *effect* of mass: rest-energy coupling, source for gravitational deflection, and carrier-of-inertia for the gauge sector. The "cost" column for each is the engineering and conceptual price already implied by `ca-unified-v2.md`, not new work proposed here.

The electroweak framing matters because the standard Higgs mechanism does double duty in the Standard Model — giving fermions rest mass *and* giving W/Z gauge bosons their mass via symmetry breaking. v2 explicitly preserves only the fermion-Yukawa half of that. The W/Z mass and the photon "mass" question land on different paths.

---

## 2. The three mass-generation paths in v2

### Path A — Yukawa coupling of the Higgs scalar $\Phi$ to fermions

**Source in v2:** S4 (preservation), summary table row "Fermion mass."

The per-cell Yukawa relation from v1 is preserved verbatim (with the P2/P4 corrections from `ca-f3-propositions.md`):

$$m_{\text{eff}}(\mathbf{x}, t) = y\,\text{Re}\,\Phi(\mathbf{x}, t)$$

This drops into the Dirac stepper as a position-dependent mass term in the per-cell phase. In the $\Phi = v$ limit it reduces to a constant Dirac mass $m = yv$ everywhere; in the symmetry-restored phase $\Phi = 0$ the fermions are exactly massless. F1, F2, F4 are the gate tests.

What this path covers: rest mass of charged fermions. What it does **not** cover: W/Z gauge-boson mass (v2 does not address this — Weak sector is "unchanged per-cell SU(2) on left chirality"), or any "gravitational mass" sense.

**Costs implied by v2:**
- Engineering: zero new code. `ca_higgs.py` and the F3 Yukawa back-reaction handling are already in place.
- Conceptual: keeps a fundamental scalar in the theory. v2 makes no attempt to derive $\Phi$ from substrate dynamics — it is postulated, exactly as in the Standard Model.
- Validation: F1 (Yukawa per-cell mass), F2 ($\delta\Phi$ Higgs propagator), F4 (symmetry-restored massless phase). All passing in the existing 13/13 regression.

### Path B — Stress-energy sourcing of the EMQG vacuum potential $\phi$

**Source in v2:** S1, summary table row "Metric."

This is the path that v2 most heavily reworks relative to v1. Total stress-energy from every matter contribution (the Higgs scalar **and** the Dirac field) appears in the right-hand side of Paper 6 Eq. 19.7:

$$\nabla^2 \phi(\mathbf{x}, t) - \frac{1}{c_0^2}\frac{\partial^2 \phi}{\partial t^2} = 4\pi G\, \rho_{\text{tot}}(\mathbf{x}, t)$$

with $\rho_{\text{tot}} = \rho_\Phi + \rho_\Psi$ — Higgs stress-energy plus Dirac stress-energy. The Yukawa-induced effective fermion mass from Path A enters this sum via $m_{\text{eff}}c^2\Psi^\dagger\beta\Psi$ in the Dirac stress-energy expression, so Path A actually sources Path B.

The output $\phi$ then feeds the variable-$c$ stepper through the GR-Shapiro reduction $c(\mathbf{x}, t) = c_0/(1 - 2\phi/c_0^2)$ (the 2026-05-16 sign correction documented in the v2 "Back-fix" box).

What this path covers: gravitational mass in the operational sense — the quantity that bends a probe ray's trajectory and produces gravitational redshift. What it does **not** cover: rest mass (that has to come from Path A first, before it can appear in $\rho_\Psi$).

**Costs implied by v2:**
- Engineering: the largest single implementation item in v2 (V11 gate). A time-dependent Poisson solver with implicit time stepping (Crank–Nicolson on the wave operator) is required to remain unitary with the retardation term. Estimated 1 week in the v2 build sequence; flagged as "the largest implementation risk" in honest-caveat 2.
- Conceptual: imports EMQG as a phenomenological assumption (honest-caveat 1 — "Paper 6 is a physics essay, not a derivation"). $G$ replaces v1's free exponent $\alpha$, which is a strict improvement, but Paper 6's modified Poisson is still postulated rather than derived from informational axioms.
- Validation: V11 (deflection $\Delta\theta \approx 2GM/(bc^2)$ or $4GM/(bc^2)$), V12 (gravitational redshift), F3b (existing Cayley lensing demo, rewritten against the new $c(\phi)$ law).

### Path C — Composite-photon construction giving the gauge sector its $E/c^2$ effective mass

**Source in v2:** S3, summary table row "Electromagnetic."

The composite-photon construction (Paper 1 Eq. 35) builds $\mathbf{E}_G$ and $\mathbf{B}_G$ from bilinears of two correlated Weyl fields:

$$G^i(\mathbf{k}, t) = \varphi^T(\mathbf{k}/2, t)\,\sigma^i\,\psi(\mathbf{k}/2, t)$$

$$\mathbf{E}_G := |\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T + \mathbf{G}_T^\dagger), \quad \mathbf{B}_G := i|\mathbf{n}_{\mathbf{k}/2}|(\mathbf{G}_T^\dagger - \mathbf{G}_T)$$

These obey free Maxwell at small $\mathbf{k}$. The composite photon is *manifestly* massless in the standard sense — there is no Yukawa term. But the photon nevertheless carries inertial and gravitational mass in the operational $E/c^2$ sense, because its energy density contributes to $\rho_{\text{tot}}$ in Path B and because it is deflected by the resulting $c(\mathbf{x})$ field. v2 inherits this implicitly: any test of Paper 6's "gravity as photon scattering" picture requires composite photons that can actually scatter, which is exactly what S3 supplies.

What this path covers: gauge-boson effective mass via energy. What it does **not** cover: a Higgs-style mass term for the W/Z. v2 explicitly does not address electroweak symmetry breaking for the gauge sector — the Weak row in the summary table is "Per-cell SU(2) on left chirality (unchanged)."

**Costs implied by v2:**
- Engineering: V4 gate, new `ca_maxwell.py`, estimated 4–6 days in the v2 build sequence. Highest leverage of the new modules — "the single largest architectural gap in v1: it has no genuine photon dynamics on the lattice."
- Conceptual: depends on bosonic statistics emerging only *approximately* from a smearing function $f_\mathbf{k}(\mathbf{q})$ over Weyl bilinears (Paper 4). Decoherence channels under L4 vacuum scattering are not addressed (honest-caveat 3).
- Validation: V4 (Maxwell curl equations violated at $\mathcal{O}(k^3)$), E1 (Aharonov–Bohm regression at $4 \times 10^{-16}$ — the external classical $A_\mu$ is retained as a fast approximation and the composite construction is the canonical reference).

### Path summary

| Path | What it generates | Where it acts | Gate test | v2 reduction limit |
|---|---|---|---|---|
| A — Yukawa | Fermion rest mass $m = y\,\text{Re}\,\Phi$ | L3 (Dirac stepper) | F1, F2, F4 | $\Phi = v$ → v1 vacuum regression |
| B — EMQG $\phi$ sourcing | Operational gravitational mass | L4 (Poisson solver feeding $c(\mathbf{x})$) | V11, V12, F3b | $\rho_{\text{tot}} = 0$ → $\phi = 0$, $c = c_0$ |
| C — Composite photon $E/c^2$ | Gauge-boson inertial mass via energy | L3 (composite Maxwell) | V4, E1 | Coherence enforced by hand → external classical $A_\mu$ |

Path A feeds Path B (Yukawa rest mass appears in $\rho_\Psi$). Path C feeds Path B (photon energy density appears in $\rho_{\text{tot}}$). Path B does not feed back into A or C directly — it only changes the propagation medium $c(\mathbf{x})$.

---

## 3. What v2 does **not** generate mass for

Three real-world mass sources are absent from v2 and worth flagging before any comparison:

1. **W/Z gauge-boson mass.** Standard-Model electroweak symmetry breaking gives W and Z their masses through the Higgs vacuum expectation value. v2 keeps the Higgs but leaves the SU(2) sector "unchanged per-cell SU(2) on left chirality," with no symmetry-breaking coupling between $\Phi$ and SU(2). E2 is the existing weak-sector gate, but it tests left-chiral coupling, not gauge-boson mass.
2. **Confinement-induced QCD mass.** v2 has no SU(3). Roughly 99% of proton/neutron mass is QCD binding energy, none of which is in scope.
3. **Composite/bound-state mass.** v2 has no model of how Higgs-bound fermion patterns assemble into hadrons or atoms.

---

## 4. Comparison to Ostoma–Trushyk's three mass definitions

`ostoma-trushyk-1999-summary.md` §7 names three masses in EMQG:

| OT mass | OT definition | OT mechanism |
|---|---|---|
| **Inertial mass $m_i$** | From $F = ma$ — resistance to acceleration via EM coupling to accelerating charged virtual vacuum | Quantum Inertia (§8): sum of photon exchanges between mass's charged particles and the local vacuum |
| **Gravitational mass $m_g$** | From $F = GM_1M_2/r^2$ — what a scale measures | Photon-mediated coupling to the downward-accelerating vacuum near a real mass (§17) |
| **Low-level "mass charge"** | Pure graviton-emission rate, analogous to electric charge | Postulated property of the masseon; not directly measurable; swamped by EM interactions (§7) |

Mapping v2's three paths onto OT's three masses:

### Path B ↔ OT gravitational mass $m_g$ — **direct correspondence**

v2's S1 imports Paper 6 Eq. 19.7 verbatim. OT writes the same equation as Eq. 15.2 in `ostoma-trushyk-1999-summary.md`:

$$\nabla^2 \phi - \frac{1}{c^2}\frac{\partial^2 \phi}{\partial t^2} = 4\pi G\, \rho(x,y,z,t)$$

with the retarded form Eq. 19.6 identical to v2's. v2's $c(\mathbf{x}) = c_0/(1 - 2\phi/c_0^2)$ is the same physics as OT's photon-scattering-off-accelerating-vacuum interpretation (§11, §18), reduced to the weak-field limit. **This is the cleanest match between the two models.** Path B is OT's $m_g$.

### Path C ↔ OT inertial mass $m_i$ (partial) — **mechanism differs, observables agree**

OT inertia (§6, QI postulate) is operationally "the EM-sum of photon exchanges between a mass's charged particles and the surrounding accelerating charged virtual vacuum particles." Path C gives v2 a *genuine* lattice photon (the composite construction) — which is the prerequisite for QI to be testable on the lattice at all. Without Path C, v2 inherits inertia only as kinematic momentum on the lattice; with Path C in place, the QI mechanism becomes the natural interpretation of the inertial response. OT's photon $m_p = E/c^2$ derivation (§7) — from $p=mc$, $c=\nu\lambda$, $E=h\nu$, $\lambda = h/p$ — is exactly the operational sense in which the composite photon "carries mass" in v2. **Mechanism overlap rather than identity:** OT requires the masseon and a virtual-particle vacuum to make QI sharp; v2 has neither. Path C delivers the photons that QI would need, but not the vacuum of charged virtual particles those photons would scatter off.

### Path A ↔ **no OT analog**

This is the substantive divergence. OT has **no Higgs scalar and no Yukawa coupling**. In OT, rest mass is not generated by a separate scalar field — it emerges from the masseon's EM coupling to the vacuum (the same mechanism as inertia). OT's $m_i = m_g$ to ~$10^{-40}$ precision because *both* are EM-vacuum effects on the same underlying mass charge; in OT there is no separate origin for "rest mass" that would generate a third distinct quantity.

v2's Path A imports the Standard-Model Higgs scalar wholesale (S4 preserves v1's Yukawa). This is a stronger ontological commitment than OT makes — v2 has a fundamental scalar field that OT explicitly does not need. From OT's standpoint, what v2 calls "rest mass via Yukawa" would be re-interpreted as part of the inertial $m_i$ already accounted for by vacuum coupling.

### OT low-level mass charge ↔ **no v2 analog**

v2 has no gravitons. All gravitational physics in v2 is routed through Path B (the EMQG $\phi$ potential), which corresponds to OT's *photon-mediated* gravity (the dominant ~$10^{40}$ part). OT's "low-level mass charge" is specifically the pure graviton-emission rate — the *subdominant* part of gravity that drives the predicted ~$10^{-40}$ WEP violation. v2 cannot test this prediction (honest-caveat 7: "WEP violation at $10^{-40}$ is unfalsifiable in float64"), and it has no carrier corresponding to OT's mass charge. v2 collapses OT's "$m_g$ = photon-vacuum part + graviton-mass-charge part" into "$m_g$ = stress-energy sourcing $\phi$."

### Comparison table

| v2 path | OT analog | Status |
|---|---|---|
| A — Yukawa | None | v2-only; reflects v2's retention of the Standard-Model Higgs |
| B — EMQG $\phi$ sourcing | $m_g$ (gravitational mass) | Direct correspondence via Paper 6 Eq. 19.7 ≡ OT Eq. 15.2 |
| C — Composite photon $E/c^2$ | $m_i$ (inertial mass), partial | Same observables, weaker mechanism: v2 has lattice photons but no masseon/QI vacuum |
| None | Low-level mass charge | v2 has no graviton; the subdominant gravity channel and the $10^{-40}$ WEP violation it predicts are absent |

---

## 5. Takeaway

v2's three mass-generation paths are not parallel in OT's sense — they live in different layers (L3 for A and C, L4 for B) and chain into each other rather than competing. The clean match between v2 Path B and OT's gravitational mass is the strongest agreement between the two models and is what makes v2 a real test program against EMQG. The Yukawa Path A is the largest *philosophical* divergence: OT does not postulate a Higgs scalar at all, treating what would be "rest mass" as a special case of vacuum-coupled inertia. The composite-photon Path C is the prerequisite for v2 to ever test OT's QI mechanism directly, but v2 supplies the photons without supplying the masseon/charged-virtual-vacuum that QI requires.

If a future iteration of v2 were to drop the Higgs Path A and try to derive fermion rest mass from substrate dynamics (e.g., via masseon-style bound states of the Weyl fields plus the L4 vacuum potential), it would converge much more closely on OT's three-mass picture. That direction is not in scope for v2 as drafted.

---

## Cross-references

- `ca-unified-v2.md` §"Concrete substitutions for v1" (S1, S3, S4) and §"Summary table" — primary source for the three paths.
- `ostoma-trushyk-1999-summary.md` §7 "Three Mass Definitions," §6 "Quantum Inertia," §10 "EMQG Field Equations" — primary source for the comparison.
- `ca-f3-propositions.md` P1/P2/P4 — the corrections preserved on top of the v1 Yukawa (Path A).
- `qca-papers-1-4-overview.md` — Paper 1 Eq. 35 (Path C), Paper 6 Eq. 19.7 (Path B), test gates V4 and V11.
- `model-observations.md` item 1 and `changelog.md` 2026-05-16 — the GR-Shapiro sign correction that fixed Path B.
