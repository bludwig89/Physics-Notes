# Audit — are the model's bound states emergent, or manufactured by their tests?

**Date:** 2026-06-12 - 00:50
**Scope:** Every finding claiming a bound state: F103 (pion), F104 (deuteron), F122 (baryon), F125 (hydrogen), F135/F136 (real-space confined proton), F137 (live colour-dielectric bag), F139 (self-consistent dual-GL), with F70/F99 (pure-gauge string tension) as the reference point.
**Method:** Re-ran the suites independently (not just reading the result JSONs), read the test code for circularity, ran two probes the suites omit, and ran a decisive new test — a confining flux tube with **no input string tension**.
**Artifacts:** `tests/runners/run_su2_3d_fluxtube.py`, `test-results/su2_3d_fluxtube.json`.

---

## 1. Question

"Verify that emergent bound states do in fact form and aren't just manufactured by tests." Two failure modes were checked: (i) the *tests* cheat — circular construction, unfair controls, tuned tolerances; (ii) the *binding* is an input dressed as a result, so nothing actually emerges from the dynamics.

## 2. The tests are honest (failure mode i: not found)

Re-running confirms the claimed numbers (F135 3/3, F137 3/3, F122 11/11, all reproduced). The controls are fair: in F135/F137 the "free" comparison uses the *identical* initial state, mass, and width, with only the confining channel toggled off; norms are conserved to machine precision; the pass thresholds are real separations (confined RMS plateau ≈ 3 vs free dispersal to box saturation ≈ 8), not tolerance-gamed. The spectral findings (F122, F125, F103, F104) are genuine eigenvalue solves cross-checked two ways (e.g. F122 `eigh` vs Cholesky to 4.5×10⁻¹², F125 numerical-Dirac vs Sommerfeld). No fabricated or circular pass conditions were found.

## 3. But "bound state" means two different things (failure mode ii: real, and the findings say so)

**Class A — spectral solves of a *posited* potential.** F122 (Cornell $V=\sigma r-\tfrac{2\alpha_s}{3r}$), F125 (Coulomb $-Z\alpha/r$), F103 (NJL+RPA ladder), F104 (one-pion-exchange Yukawa+tensor). These diagonalise a Hamiltonian whose **binding term is supplied**, not produced by the CA rule. They legitimately show "given this interaction plus model-derived parameters ($\sigma$, $m_\pi$, $f_\pi$, $m_e$, $\alpha$), the known spectrum/structure follows," and the findings flag this honestly (F122 §5 is Tier-B/P6-gated and overshoots $m_p/\sqrt\sigma$ by ≈3.6×; F104 tunes a core radius; external couplings $g_A$, $g_{\rho\pi\pi}$ are marked). The binding interaction is an input.

**Class B — real-space lattice time-evolution.** F135/F136/F137 actually propagate quanta on the BCC lattice and watch a cluster stay bound versus a dispersing free control. This is the genuine "universe in a bottle" demonstration, and the binding does emerge as non-dispersion under the update rule. Confirmed independently: the confined cluster RMS plateaus at ≈ 2.95 and holds flat across 300 ticks (not a wall bounce); the free control disperses to box saturation.

## 4. The model's gauge sector does not confine on its own

In every "free" control the gluon channel (`gluon_sourced`, F43) is active, yet the quarks still disperse to the box — corroborating F134's U1 null. Confinement appears **only once a scalar bag is installed** (the input $\sigma$ in F135, or $M_\text{bag},\phi_0,\lambda$ in F137). The binding in Class B comes from the installed Lorentz-scalar mass, not from SU(3) exchange.

## 5. New probe — the self-sourced bag self-traps a *single* charge

The suites do not test this. Running the F137 "live, self-sourced" bag on a **single** colour blob:

| configuration | RMS last | RMS max |
|---|---|---|
| single blob, bag on | 2.23 | 2.39 |
| single blob, bag off (free) | 8.15 | — |
| `uud` cluster, bag on | 2.95 | 2.97 |
| `uud` cluster, bag off (free) | 8.86 | — |

A single isolated colour charge is trapped just as well as the three-body cluster. So F137's "the proton digs its own bag" is mechanically "**any** colour-charge density digs a well and self-traps" — a generic mean-field self-trapping that would also hold a lone quark, which real QCD forbids. The three-body / colour-singlet structure is not what produces the binding. **Recommendation:** add this single-blob run to the F137 suite as an explicit caveat — it is the cleanest demonstration that the mean-field bag does not enforce colour-singlet confinement.

## 6. F139 closes the smear, not the scale

F139's self-consistent dual-Ginzburg–Landau back-reaction is real and cures the F137 mean-field pinch-off (the smear $\lambda$ now emerges from the coherence length $\xi$). But the confinement **scale** $\sigma=2\pi v^2 n$ is still F86's analytic input (the condensate VEV $v$), it is the Abelian Cartan-projected reduction, and F139 itself states the tension is reproduced "qualitatively (constant tension), not yet to algebraic exactness." The scale is still imported.

## 7. The decisive test — a flux tube with **no input $\sigma$/$v$**

The line between "installed" and "emergent" is: can a confining linear potential appear from the gauge coupling alone, with no string tension or condensate fed in? F70 already answers yes — $\sigma(\beta)=-\ln w(\beta)>0$ from the SU(3) group integral, no $\sigma$ input — but **only in 2D**, where every gauge theory confines at all couplings, so the test cannot fail. The honest test needs a dimension where confinement is dynamical.

I ran pure **SU(2) lattice gauge theory in 3D** (exact Creutz/Kennedy–Pendleton heat bath, unit-quaternion links so all arithmetic is real — the CLAUDE.md numpy/chiral caveat does not bite). The **only inputs are $\beta$ and the lattice**: no $\sigma$, no $v$, no $M_\text{bag}$, no smear. Reproducibility checks first: cold start gives $\langle\text{plaq}\rangle=1$ exactly; checkerboard updating is required (a $\mu$-link's staple contains the $\mu$-link at $x\pm\nu$, so naïve simultaneous updates break detailed balance and run away to disorder — fixed); the heat-bath single-link mean reproduces $I_2/I_1$ to <0.5%; and $\langle\text{plaq}\rangle$ tracks $\beta/4$ at strong coupling, $\to1$ at weak.

**Strong coupling — the area law matches the analytic prediction.** $\sigma$ from $-\ln W(2,2)/4$ versus the leading character-expansion value $-\ln(\beta/4)$:

| $\beta$ | $\langle\text{plaq}\rangle$ | $\sigma=-\ln W(2,2)/4$ | $-\ln\langle\text{plaq}\rangle$ | $-\ln(\beta/4)$ |
|---|---|---|---|---|
| 1.0 | 0.245 | 1.279 | 1.406 | 1.386 |
| 1.5 | 0.352 | 1.067 | 1.045 | 0.981 |
| 2.0 | 0.455 | 0.780 | 0.789 | 0.693 |

The MC string tension tracks the analytic strong-coupling law (the small overshoot of $-\ln(\beta/4)$ is the known higher-order correction, since the true plaquette exceeds $\beta/4$).

**Intermediate/weak coupling — a linear confining potential.** $V(R)=-\ln[W(R,T)/W(R,T+1)]$, fitted to $\sigma R+V_0$, with the Creutz ratio as an independent estimator:

| $\beta$ | $\langle\text{plaq}\rangle$ | $V(1),V(2),V(3),V(4)$ | $\sigma_\text{fit}$ | Creutz $\chi(2,2)$ |
|---|---|---|---|---|
| 3.0 | 0.625 | 0.45, 0.89, 1.27, 1.08 | 0.228 | 0.407 |
| 4.0 | 0.729 | 0.28, 0.49, 0.66, 0.84 | 0.184 | 0.230 |
| 5.0 | 0.785 | 0.21, 0.36, 0.48, 0.59 | 0.127 | 0.163 |
| 6.0 | 0.824 | 0.16, 0.26, 0.35, 0.42 | 0.085 | 0.122 |
| 7.0 | 0.851 | 0.13, 0.21, 0.28, 0.33 | 0.065 | 0.097 |

$V(R)$ rises linearly, $\sigma>0$ at every coupling (3D SU(2) confines at all $\beta$, as it must), and $\sigma(\beta)$ decreases smoothly toward the continuum — the correct, falsifiable, quantitative behaviour. **A confining flux tube emerged with the coupling as the sole input.** This is dimensional transmutation, and it is exactly the step the bound-state chain (F135/F137/F139) skips: the gauge sector *does* generate its own confinement scale; the real-space proton findings re-import $\sigma$ (or $v$) instead of using it.

## 8. Verdict

Bound states do form under time evolution and are **not** conjured by test rigging. But the strongest *honest* claim the model currently supports is: *the lattice kernel binds correctly when handed a Lorentz-scalar string, and the scalar-binds / vector-Klein-tunnels distinction is a real emergent kernel response* — **not** *confinement emerges from the SU(3) dynamics*. The entire QCD bound-state tower rests on a mean-field bag whose scale is imported from F86, and that bag self-traps even a single colour charge.

Separately, the pure-gauge sector **does** produce emergent confinement from the coupling alone (F70 in 2D; §7 here in 3D SU(2)). The open, decisive work is to wire that emergent $\sigma$ — measured from the model's own SU(3) BCC kernel in 3D/4D, not re-supplied — into the real-space bound state, so the proton is confined by the string the dynamics generate rather than one installed by hand.

## 9. Recommendations

1. Add the **single-blob self-trapping** control (§5) to the F137 suite and its honest-edge section.
2. Reproduce §7 with the **model's own SU(3) BCC gauge kernel** (`ca_strong`/`ca_confinement` extended to 3D) and feed the *measured* $\sigma(\beta)$ into the F135 scalar-mass / F137 bag — closing the import.
3. Treat Class-A absolute masses (F122 $m_p/\sqrt\sigma$, F104 binding) as P6-gated until the scale is emergent rather than anchored.
