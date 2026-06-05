# P1 — The Binding Force: options / forks for 3+1D confinement (string-theory-free)

**Date:** 2026-06-03 - 00:35  (updated 2026-06-04 - 14:33)
**Status:** **Options C and A both BUILT.** C — F86, 6/6 (`ca_colour_dielectric.py`). A — F94, engine 6/6 + comparison 4/4 (`forks/lgt_fork_A_mc.py`). Options B, D remain available; see the per-option notes below. Original outline preserved.

> **2026-06-04 - 14:33 — Option A executed (F87), tested against Option C.** 3+1D SU(3) heat-bath/over-relaxation MC + Lüscher–Weisz two-level estimator (`forks/lgt_fork_A_mc.py`). Engine certified 6/6 (`test_FA_lgt_mc.py`): OR action-invariance $1.2\times10^{-16}$, staple/action-gradient identity (ratio 4) $8.9\times10^{-16}$, ⟨plaq⟩ matches published SU(3) to 0.6%, multilevel **84×** variance reduction (beats the `run_confinement_mc.py` wall). Smoke run: clean confining $V(R)$. Head-to-head with C 4/4 (`test_FA_vs_FC_comparison.py`): both confine; the gauge-MC $\sigma_A$ **fixes** C's free condensate $v^*=\sqrt{\sigma_A/2\pi}$ (A predicts C's input, to $10^{-16}$); the two potentials share the large-$R$ slope and differ by exactly the Coulomb $-e/R$ that C's BPS flux tube omits. A derives confinement from the gauge action (no condensate assumed) but is statistical; C is exact but assumes the condensate. Precise $\sigma\pm$err = user-run `run_lgt_confinement.py`. See `findings/F94-lattice-gauge-mc-confinement-vs-F86.md`.

> **2026-06-04 - 01:18 — Option C research risk closed (F88).** The flagged item "colour-magnetic condensate is assumed, not derived" is resolved: F88 derives the condensate within the model — Route 1 (Nielsen–Olesen instability + Savvidy minimum, sympy-exact, driven by F43's structure constants) shows the trivial vacuum is unstable and condensation is energetically favoured for every $g>0$; Route 2 (compactness ⇒ DeGrand–Toussaint monopoles ⇒ exact Villain/Coulomb-gas duality ⇒ dual Meissner) identifies what condenses and hands F86 a **measured** VEV $v = m_D/e$. See `findings/F88-colour-condensate-from-model.md`.

> **2026-06-03 - 23:58 — Option C executed (F86).** Dual-superconductor flux tube recast as a colour-dielectric $\varepsilon_c(x)$ renormalising the F43 gluon rotation rule — the confining analogue of F64's gravity dielectric (same mechanism, opposite impedance regime). Exact BPS tension $\sigma=2\pi v^2 n$ (CD1 algebraic, CD3 numeric to $5\times10^{-6}$); dielectric gluon step reduces to the free F43 propagator bit-for-bit (CD4); dual-Meissner $\lambda=1/(ev)$ (CD5); constant cross-section ⇒ linear $V(R)=\sigma R$ (CD6). Connects $\sigma$ to the condensate VEV $v$ as the roadmap asked. **Does not** beat the `run_confinement_mc.py` MC wall (it replaces the observable) — Option A remains the route for a rigorous 3+1D gauge-loop $\sigma$. Colour-magnetic condensate is assumed, not derived (the flagged research risk). See `findings/F86-colour-dielectric-dual-superconductor.md`.
**Context:** P0 is closed (F85). P1 is the binding force — the mechanism that confines quarks in 3+1D and supplies (most of) the proton mass. Per user direction, **string theory is excluded** as a mechanism; the QCD flux tube is treated as a lattice-gauge / field object (a colour-electric flux configuration), not a fundamental string.

---

## Why P1 is non-trivial (what the model has, and the wall it hit)

- **F43** — dynamical SU(3) gluons: rotation-law propagation, $f^{abc}$ self-coupling, Wilson-loop primitives, on both 2D-square and 3D-BCC. Kinematics are in place.
- **F70** — confinement as a **prediction, but 2D-exact only**: the area law $\langle W\rangle=w^{RT}$ is special to two dimensions (plaquettes are statistically independent), so $\sigma=-\ln w>0$, $\chi(R,T)=\sigma$, $V(R)=\sigma R$ are all exact by quadrature — no Monte-Carlo needed. **This does not carry to 3+1D.**
- **The wall (just diagnosed).** In 3+1D you need real Monte-Carlo. `run_confinement_mc.py` (2D heavy MC) already exposes the blocker: the area law makes loops decay as $w^{RT}$, so a 2×2 loop is $\sim10^{-3}$ and a 3×3 is $\sim10^{-8}$ — far below the plain-Metropolis noise floor $\sim1/\sqrt{N_\text{cfg}}$. The loop estimates fluctuate through zero and the Creutz ratio's $-\ln(\text{neg})$ is NaN. **Plain Metropolis cannot resolve the confining observables.** (Now guarded so it reports "under-resolved" instead of erroring.) Beating this wall is itself part of P1.

So P1 is really two coupled questions: **(1) what confinement mechanism do we commit to in 3+1D, and (2) what estimator makes its order parameter measurable.**

---

## The four options

### Option A — 3+1D lattice gauge Monte-Carlo + multilevel (Lüscher–Weisz) estimator
**The standard, rigorous route.** Build SU(3) heat-bath + over-relaxation updates on the 3D BCC (or Euclidean 4D) lattice; add a **two-level/multilevel** estimator that factorises the Wilson/Polyakov correlator into sublattice averages, beating the exponential signal-to-noise wall so the static potential $V(R)=\sigma R+\mu-e/R$ and Creutz ratios become measurable; locate the **deconfinement transition** via the Polyakov loop.
- **Builds:** `ca_lgt_mc.py` (heat-bath/OR), `ca_multilevel.py` (LW estimator), 3D extension of `ca_confinement`; user-run scripts (compute-heavy).
- **Exactness:** Tier-3 statistical — $\sigma$, Coulomb coeff, $\beta_c$ to MC error bars; cross-check vs strong-coupling $\sigma\approx-\ln(\beta/18)$.
- **Pros:** Textbook-defensible; directly repairs the `run_confinement_mc.py` wall; gives a real $\sigma$ to feed P2. **Not string theory** (pure lattice gauge).
- **Cons:** Most engineering; heaviest compute; statistical (not exact) — least aligned with the project's algebraic-exactness preference.

### Option B — Hamiltonian / Kogut–Susskind strong-coupling route (real-time, algebraic)
Use the **Hamiltonian** lattice gauge formulation instead of Euclidean MC. The strong-coupling expansion gives the linear potential **analytically** ($\sigma=\ln(g^2)+\dots$ order by order) and the colour-electric **flux-tube** picture directly, in real time — no MC noise wall at all. Confinement appears as a controlled, term-by-term-exact expansion.
- **Builds:** `ca_ks_hamiltonian.py` (electric-field/link Hilbert space, plaquette magnetic term), strong-coupling series to a few orders, a real-time flux-tube formation demo between a static $q\bar q$ pair.
- **Exactness:** Tier-1/2 — the strong-coupling series coefficients are exact rationals; the flux tube is an exact eigenstate at leading order.
- **Pros:** **Real-time and algebraic — matches the project's CA spirit and exactness preference**; sidesteps the signal-to-noise wall entirely; the same Hamiltonian feeds P2's real-time baryon naturally. The flux tube is a colour-electric field object (not a fundamental string).
- **Cons:** Strong-coupling → continuum-limit connection is subtle (the series is not the continuum limit); truncation control needs care.

### Option C — Colour-dielectric / dual-superconductor fork (the model-native mechanism)
The most **project-aligned** fork, and the one the notebook actually gestures at. The model's signature is *rotation-rate physics*: F26 (c = rotation rate), F64 (gravity = a **dielectric** renormalising the $(\mathbf E,\mathbf B)$ rotation rule), F46 (mass = rest-leg rotation). The natural binding-force analogue is the **dual superconductor**: the QCD vacuum as a colour-**magnetic** condensate that, by the dual Meissner effect, squeezes colour-**electric** flux into a tube of fixed energy/length $=\sigma$. Recast in the model's language this is a **colour-dielectric** that renormalises the gluon rotation rule — exactly parallel to F64's gravitational dielectric. The notebook (pp. 5–6) independently reaches for this: "superconductivity… two electrons pair up… the superconductivity state = travel at $c$ without hindrance from the lattice… negative binding energy."
- **Builds:** `ca_colour_dielectric.py` fork — a colour-dielectric profile $\varepsilon_c(x)$ renormalising the F43 gluon step; test that a static $q\bar q$ pair forms a constant-cross-section flux tube ⇒ linear $V(R)$; connect $\sigma$ to the dielectric/condensate parameter.
- **Exactness:** mixed — the dual-Meissner flux-tube profile can be solved analytically (Tier-1/2 for the profile), $\sigma$ then quantitative.
- **Pros:** Most novel and most consistent with the model's existing gravity/EM treatment (one mechanism — dielectric rotation-rule renormalisation — for both gravity and confinement); directly answers the notebook's BCS questions; **no string theory** (dual superconductor is a field-condensate mechanism).
- **Cons:** Least certain; needs the colour-magnetic condensate to be demonstrated, not assumed; highest research risk.

### Option D — Borrow σ, go straight to the dynamical baryon (pragmatic shortcut to P2)
Defer the 3+1D confinement *derivation*: take $\sigma$ from F70 (or a calibrated value) as an **input**, and feed $V(R)=\sigma R-\tfrac{4}{3}\tfrac{\alpha_s}{R}$ directly into the F74-style relative-coordinate solver to build the dynamical proton/neutron now.
- **Builds:** nothing new for P1; jumps to `ca_baryon_dynamics.py` (P2).
- **Exactness:** the solver is machine-precision-internal; the proton mass is then $m_p/\sqrt\sigma$ (a ratio), absolute only after P6.
- **Pros:** Fastest path to a real proton; uses machinery that already exists (F74).
- **Cons:** Does **not** establish 3+1D confinement from the gauge sector — it assumes the answer P1 is supposed to prove. Best treated as a parallel "get a number now" track, not a replacement for A/B/C.

---

## Recommendation framing (not a decision)

- If the priority is **rigor / defensibility** → **A** (with the multilevel estimator, which also fixes the MC wall).
- If the priority is **algebraic exactness + real-time alignment with the CA model** → **B**.
- If the priority is **a genuinely model-native mechanism** that unifies with the F64 gravity-dielectric and answers the notebook's own BCS thread → **C**.
- If the priority is **a dynamical proton as fast as possible** → **D** (parallel track).

A and B both independently repair the `run_confinement_mc.py` signal-to-noise wall (A by multilevel, B by avoiding MC). C and D do not address it (C replaces the observable; D sidesteps confinement). These are not mutually exclusive — e.g. B or C for the mechanism + D to get an early proton number is a coherent combination.

**Next action: user picks the direction(s) before any P1 code is written.**
