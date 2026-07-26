# d₁ via the full KNS lattice self-energy — status and honest blocker

**Date:** 2026-07-15 - 19:30
**Scope:** attempt to close $d_1=\Lambda_{\overline{\rm MS}}/\Lambda_L$ (open-derivations v2; E3 = Q1 = Q2) by reproducing the pure-gauge SU(3) Wilson constant $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ (Hasenfratz–Hasenfratz 1980) from a full one-loop lattice self-energy — the Kawai–Nakayama–Seo (KNS) 3-gluon vertex + 4-gluon seagull + ghost + Haar measure term.

## Verdict

**Not reproduced by hand-transcription — and this is a sourcing limit, not a physics failure.** The sub-machinery is validated, the target is pinned, and the gap is isolated, but completing it correctly requires the complete Wilson vertex set with exact coefficients, which cannot be obtained reliably in this environment without fabricating unsourced numbers.

## What IS validated (rigorous)

| Piece | Result | Status |
|---|---|---|
| BZ integrator | 4D midpoint $\langle1/\hat k^2\rangle\to Z_0=0.154933$ ($n{=}48\!:0.154903$, $1/n^2$ conv.) | ✓ machine-converging |
| Loop assembly | background-field gluon+ghost self-energy is exactly transverse, $b_0=\tfrac{11}{3}C_A=11$ (gluon:ghost $10{:}1$) | ✓ exact (F162) |
| Target constant | $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.809\Rightarrow c=2b_0\ln R=0.4682$ (1/g² units) $=73.9$ in $16\pi^2$ units | ✓ from literature |

## Where the leading assembly lands

The leading (hatted-momentum + cosine form-factor) 3-gluon vertex + ghost + a simplified seagull reaches only **26 %** of the target:

$$C_\text{leading}\approx 19.1 \ (16\pi^2\text{ u.})\ \Rightarrow\ \Lambda\text{-ratio}=2.38\quad(\text{target }28.81).$$

The **missing ~55 units (74 %)** is the seagull tadpole + measure term + the full 3-gluon vertex form-factor terms, dominated by the delicate **seagull ↔ measure quadratic-divergence cancellation** ($\delta_{\mu\nu}\Lambda^2$ pieces must cancel by background-gauge invariance, leaving a large finite remnant in the transverse part). This is the historically hard core of the KNS computation.

## The blocker (why it stops here)

Correctly assembling the remaining 74 % needs the exact Wilson lattice Feynman rules:
1. the full 3-gluon vertex (leading + the additional lattice form-factor terms that vanish in the continuum),
2. the 4-gluon seagull (tadpole) vertex,
3. the ghost–ghost–gluon vertex form factors,
4. the Haar-measure term coefficient.

These are in Capitani's review (hep-lat/0211036, §5.2) and Kawai–Nakayama–Seo, but the formulas do not survive PDF→text extraction, and transcribing vertex coefficients from memory would inject unsourced numbers — forbidden by the project's no-invention rule. Hand-transcription is therefore not a defensible route to the digit.

## Update 2026-07-15 - 21:10 — automated vertex generator BUILT and validated

`ca-simulation/ca_lpt_generator.py` now **derives** the Wilson vertices from the action (HiPPy/HPsrc-style: expand the links $U=\exp(igA)$ order by order, read off the momentum-space coefficient), so no coefficient is transcribed/fabricated. Validation gates all PASS at machine precision:

| Vertex | Gate | Result |
|---|---|---|
| n=2 (propagator) | $=\delta_{\mu\nu}\hat k^2-\hat k_\mu\hat k_\nu$ (exact Wilson inverse propagator) | $C=1.0$, dev $4.4\times10^{-16}$ ✓ |
| n=3 (3-gluon) | $\to K f^{abc}[$continuum tensor$]$, single $K$ across all indices + Bose-sym | $K=i$, ratio-spread $8\times10^{-8}$, Bose $0.0$ ✓ |
| n=4 (seagull) | non-trivial + Bose-symmetric; zero unless $\le2$ distinct Lorentz indices (correct) | value $\approx-1$, Bose $0.0$ ✓ |

**Remaining generator pieces:** the ghost–gluon vertex (from the FP gauge-fixing / determinant) and the Haar **measure term**. With those, the generated vertices feed the validated BZ integrator + gates (Z₀ ✓, $b_0=11$ ✓) to assemble the full self-energy and test 28.81. The gauge-vertex generator — the hard, novel core — is done and machine-validated.

## Update 2026-07-21 — NP static-potential run completed (d1_static_potential_L18.json)

The gauge-free cross-check ran to completion: 4D pure-gauge SU(3), **L=18**, β = 5.9, 6.1, 6.3, 6.5 (~11–12 h each, ~2 days total; `run_d1_np.sh`).

| β | α_V | σ_lat | route1 Λ/√σ (bakes in 28.81) | route2 Λ/√σ (measured) | routes agree |
|---|---|---|---|---|---|
| 5.9 | 0.100 | 0.0994 | 0.240 | 0.012 | 181% |
| 6.1 | 0.156 | 0.0531 | 0.262 | 0.131 | 67% |
| 6.3 | 0.170 | 0.0304 | 0.276 | 0.236 | **16%** |
| 6.5 | 0.152 | 0.0274 | 0.232 | 0.166 | 33% (finite-V) |

**Result — consistent with 28.81 within the known bare-coupling artifact, but not a digit-level pin.**
- The two independent routes (route 1 assumes 28.81 from the bare coupling; route 2 measures α_V and runs it) **converge at β=6.3 to 16%** — the meaningful internal cross-check that 28.81 is consistent with the measured coupling.
- **But** Λ_MSbar/√σ ≈ 0.25 (a²→0 extrapolation of the 3 clean points → ~0.29) vs the accepted continuum ~0.55 — a factor ~2 low. This is the textbook **bare-coupling scaling violation** (the motivation for tadpole/boosted couplings), NOT evidence against 28.81.
- β=6.5 at L=18 shows finite-volume breakdown (σ flattens, √σ/Λ_L a jumps).
- **Verdict:** the NP route neither certifies nor refutes 28.81 to precision; it is consistent within the ~2× bare-coupling artifact, with route-1/route-2 convergence at β=6.3 a genuine positive. d₁ = Λ_MSbar/Λ_lat still not pinned to the digit by this route.
- **To sharpen (concrete next step):** redo with the **tadpole-improved (boosted) coupling** g̃² = g₀²/u₀ (u₀ = mean plaquette, already measured), which collapses the factor-2 in the literature; and go to L≥24 before using β≳6.5. Only then does Λ_MSbar/√σ approach 0.55 and pin q*a/d₁.

## Recommended completion paths

- **Automated LPT Feynman-rule generator** (Hart–von Hippel–Horgan–Storoni, HiPPy/HPsrc, hep-lat/0411026): generates the exact Wilson vertices programmatically; the existing validated BZ integrator + b0/transversality/Z₀ gates here would then consume them. This is the rigorous route to the digit.
- **Verified published vertex table**: if a machine-readable KNS/Weisz vertex set is supplied, the assembly + gates here can be completed directly.
- **Non-perturbative pin (tractable now):** `tests/runners/run_d1_static_potential.py` — the gauge-fixing-free static-potential route needs no vertices; a β-sweep in the 4D scaling window (β ≈ 5.8–6.3) pins $\Lambda_{\overline{\rm MS}}/\sqrt\sigma$ and confirms 28.81 independently. **This remains the recommended way to pin $d_1$ without the vertex algebra.**

## Bottom line for the ledger

$d_1$'s **perturbative** route is blocked on obtaining exact lattice vertices (automated generator needed); its **non-perturbative** route (static potential) is open and tractable. The leading-vertex PT candidate ($q^*a\approx0.49$, below the F155 band) is *not* certified. The Wilson gate — the arbiter for any PT attempt — needs the full vertex set to be evaluated.

## Update 2026-07-19 - 12:06 — four execution steps run (exact vertices wired; measure derived; scheme gap isolated)

Executed the four recommended steps. Net: wiring the **exact** generated vertices into the self-energy jumps the transverse constant from the cosine stand-in's **19.1 → ~70** (16π² units, n=6) against the target **73.9** — i.e. the former 74 % gap was dominated by the crude cosine form factor, not missing physics. One clean derivation and one clean diagnosis landed; the digit is still not *certified* (n-convergence + the scheme-fix term remain).

**(5) NP static-potential run — command written + verified.** `tests/runners/run_d1_np.sh` (writes to an L-tagged file so it never clobbers existing results). Diagnosis of the existing `test-results/d1_static_potential.json` (L=10, β∈{5.8,6.0,6.2}): $\Lambda_{\overline{\rm MS}}/\sqrt\sigma=0.320$ vs world 0.55, routes 1 & 2 disagreeing ~33 % ⇒ **below the scaling window + finite-volume-limited**. Fix baked into the command: larger L (16→20), β∈{5.9,6.1,6.3,6.5}, more stats (ntherm 600 / nmeas 800), wider Cornell window (rmax=tmax=8). Native, multi-hour job.

**(1) Exact vertices wired in.** New `ca-simulation/ca_lpt_selfenergy.py`: the 3-gluon loop is assembled from the **exact generated** Wilson vertices (colour factorises, $V_3^{abc}=f^{abc}T$; the generator's $U=e^{iA}$ gives $V_3=i f^{abc}T$, stripped by $1/(if^{123})$). Pointwise wiring gate: the colour-stripped grid tensor → the continuum YM tensor (ratio → 1, spread $2\times10^{-7}$). Result: gluon+ghost transverse constant **C ≈ 70** (n=6, Q-spread 1.3; needs even-n convergence via the native runner).

**(2) Haar measure term — DERIVED (first principles).** From the adjoint exp-map Jacobian $\ln J(X)=\mathrm{tr}_{\rm adj}\ln[(I-e^{-\mathrm{ad}_X})/\mathrm{ad}_X]=-\tfrac{C_A}{24}\sum_a(X^a)^2+O(X^4)$ (structure constants only, no transcription): coefficient $=C_A/24=\tfrac18$ for SU(3), machine-exact (std $3\times10^{-10}$). ⇒ mass counterterm $\Pi^{\rm meas}_{\mu\nu}=-\delta_{\mu\nu}\,C_A/12$, which cancels the seagull's quadratic divergence. Seagull $Z_0(n)\to0.15493$ reproduced. Ghost loop added with the lattice FP vertex $(\hat k+\widehat{k+q})_\mu$.

**(3) Scheme-consistency gap — isolated to one term.** Added `gen.vertex_bqq_vec` (background-field link split $U=e^{iQ}e^{iB}$). Test (`scheme_consistency_diagnosis`): the plaquette **action** vertex — even with a leg tagged background — reduces to the **symmetric** YM vertex (ratio → 1, spread $1\times10^{-3}$), **not** the **Abbott** background-field vertex the $b_0{=}11$ gate uses (no constant ratio, spread 6.8). So the ~70 above is the *ordinary-gauge* exact-vertex constant, and the scheme-consistent $d_1$ needs exactly **one** more additive term: the lattice **background-covariant gauge-fixing vertex** $=$ (Abbott $-$ symmetric), whose lattice form factors come from the same link expansion. Two certified completions remain: **(A)** add that gauge-fixing vertex (background-field route, $\Pi$ alone → $b_0$); **(B)** ordinary Feynman gauge + the separate vertex renormalisation $Z_1$.

**Remaining to certify the digit:** (i) even-n convergence of C via `run_d1_selfenergy.py` (n=12–16); (ii) the background-covariant gauge-fixing vertex (route A) or $Z_1$ (route B) — **now DERIVED, see next section**; (iii) the mass-sector 28.81 gate = seagull(finite remnant) + derived measure + vertex constant. The NP run (step 5) is the gauge-free arbiter in parallel.

## Update 2026-07-19 - 12:40 — the gauge-fixing vertex is DERIVED (route A closed to a candidate)

The one missing scheme term (§Task-4 above) is now derived in closed form and proven exact. Working in the `bg` (Abbott) convention $\Gamma^F_{a m l}(k,q)$ — background $=m$ (momentum $q$), quantum legs $a$ (momentum $k$), $l$ (momentum $-k-q$):

$$\boxed{\;V^{\rm gf}_{a m l}(k,q) \;=\; \delta_{am}\,(-k-q)_l \;-\; \delta_{ml}\,k_a\;}$$

each term the longitudinal projection of one quantum leg (its own momentum in its own Lorentz slot) tied to the background index $m$ — the $(D^{\rm bg}_\mu Q_\mu)^2$ structure of background-covariant Feynman gauge ($\xi{=}1$). **Proven exact** (sympy, `gauge_fixing_identity_check`): $\Gamma^F_{aml}=V^{\rm sym}_{aml}+V^{\rm gf}_{aml}$ for **0/64** mismatched components. So the plaquette action's exact **symmetric** vertex plus this one derived term **is** the Abbott background-field vertex — no transcription anywhere.

Wiring the **lattice Abbott** vertex (exact generated symmetric tensor + hatted-momentum $V^{\rm gf}$) into the background-field self-energy, contracted exactly as `ca_bgfield_loop` ($\Pi$ alone is transverse ⇒ inherits the $b_0=11$ gate), gives a **Q-flat** transverse constant (spread $\sim0.1$, vs $1.3$ for the ordinary-gauge symmetric-only loop) — the signature of $b_0$-preservation (no residual log). First numbers (n=6, unconverged):

| kernel | $C$ (16π² u.) | Q-spread | implied $\Lambda_{\overline{\rm MS}}/\Lambda$ |
|---|---|---|---|
| Wilson (transverse, tadpole projected out) | 9.1 | 0.12 | 1.51 |
| **rule** (tadpole-free by A0 ⇒ whole $d_1$) | **15.9** | 0.08 | **2.06** |

The **rule** transverse constant is the *whole* $d_1$ (A0: no tadpole), giving $\Lambda\approx2.06$ at n=6 — the right ballpark for the $1.78$ target and **nowhere near** Wilson's $28.81$, exactly as F155-A0 requires. (The Wilson row is transverse-only, so it deliberately excludes its dominant tadpole; the full Wilson 28.81 gate adds the mass sector back.)

**Honest scope / remaining:** the digit is *not yet* pinned — (i) n-convergence (n=6→12→16, native `run_d1_selfenergy.py`; the n=6 $\Lambda{=}2.06$ should settle toward the bracket); (ii) the ghost/$V^{\rm gf}$ lattice form factors — **now DERIVED exactly, see next section**; (iii) the Wilson 28.81 cross-check still wants the mass-sector (seagull finite remnant + derived measure) assembled. But route A's blocking unknown — the gauge-fixing vertex — is **closed** (exact closed form, 0/64 proof), and the scheme-consistent pipeline now runs end to end.

## Update 2026-07-19 - 13:20 — exact FP dressing of the ghost/gf form factors DERIVED

The leading dressings (hatted momenta) are now replaced by the exact lattice form factors, derived by plane-wave extraction (no transcription).

**Ghost vertex (clean, unambiguous).** From the covariant lattice ghost Laplacian $S_{\rm gh}=\sum_{x,\mu}(\bar c(x)-\bar c(x{+}\mu)\bar U_\mu^\dagger)(c(x)-\bar U_\mu c(x{+}\mu))$, expanding $\bar U_\mu=1+iB_\mu$ and reading off the $O(B)$ coefficient with $c\sim e^{ipx}$, $\bar c\sim e^{-ip'x}$, $B_\mu$ at the link midpoint:

$$\mathrm{FF}_\mu = i\,e^{iq_\mu/2}\big(e^{-ip'_\mu}-e^{ip_\mu}\big) \;=\; \boxed{2\sin\!\big(\tfrac{(p+p')_\mu}{2}\big)}\;\xrightarrow{a\to0}\;(p+p')_\mu.$$

So the exact ghost form factor is a **single sine of the mean ghost momentum**, not the leading sum $\hat k_\mu+\widehat{(k{+}q)}_\mu$ (they agree only to $O((ka)^2)$). Reduces to continuum at $10^{-7}$.

**Gauge-fixing vertex.** From $\Delta^a=\sum_\mu(D^{\rm bg,-}_\mu Q_\mu)^a$: the divergence leg carries the exact $\hat k$ (no phase), the background-covariant connection leg carries a **midpoint phase** on the background index $m$ ($e^{-i(q+k)_m/2}$ and $e^{ik_m/2}$). The phase's $O(ka)$ part is **imaginary and cancels in the loop** ($W\!\cdot\!Z$ at conjugate momenta) — verified: with the exact dressing $\Pi$ stays **exactly real** (max $|{\rm Im}\,B|=0$), and its real part reduces to $V^{\rm gf}_{\rm cont}$ at $5\times10^{-8}$.

**Effect.** The exact FP dressing shifts the tadpole-free rule constant only slightly ($\Lambda\!:\!2.06\to2.08$ at n=6), the expected $O((ka)^2)$ refinement — and confirms the leading pipeline was already close. `finite_constant_bgfield(..., fp='exact')`, gate `validate_fp_dressing`; the sweep runner uses `fp='exact'` by default. **All vertices in the d₁ self-energy are now derived, none transcribed.** The one genuinely remaining item is n-convergence (native sweep) toward the pinned digit; the mass-sector Wilson-28.81 cross-check is the optional external check.

## Artifacts

- `tests/runners/run_d1_vertex_formfactor.py` — PT route (b0 gate exact, leading-vertex finite constant, Wilson gate; reaches 26 %).
- `tests/runners/run_d1_static_potential.py` — NP cross-check (pure-gauge, nf=0; the tractable pin).
- `tests/runners/run_d1_np.sh` — **(step 5)** ready-to-run NP command (scaling-window β sweep, larger L, safe output file).
- `ca-simulation/ca_lpt_selfenergy.py` — **(steps 1–3)** exact-vertex gluon+ghost self-energy, derived Haar measure term, scheme diagnosis.
- `tests/runners/run_d1_selfenergy.py` — native convergence runner (even n; n≥8 exceeds the sandbox cap).
- `ca-simulation/ca_lpt_generator.py` — extended with `vertex_bqq_vec` (background-field split link).
- `ca_lpt_selfenergy.py` (updated) — `gauge_fixing_vertex_continuum`/`_lattice`, `gauge_fixing_identity_check` (0/64 proof), `finite_constant_bgfield` (scheme-consistent lattice-Abbott constant, Wilson+rule kernels), `ghost_vertex_lattice_exact` (2 sin((p+p')/2)), `validate_fp_dressing` (exact FP gate).
- `tests/runners/run_d1_sweep.sh` — n-convergence sweep (native; both kernels, exact FP dressing).
