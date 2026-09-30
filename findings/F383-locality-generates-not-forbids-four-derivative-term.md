# F383 — Locality generates, not forbids, the four-derivative curvature term: F345's "at-most-second-order" sub-item closes NEGATIVE

*2026-09-10 - 16:10 · sector `interactions` · module `casim.engine.interactions.gravity_four_derivative_locality` · test record `F383-four-derivative-locality` (result_dump, battery tier, 7/7 legs PASS) · results `test-results/F383_four_derivative_locality.json`*

**Status:** Confirmed — 7/7 legs PASS (M2b added post-review, see below).
**Reviewed:** 2026-09-10 — **CONFIRMED-NARROWER** (cold subagents: blind re-derivation + adversarial referee). The qualitative conclusion (locality generates, does not forbid, the four-derivative term) survived; the referee found the specific $\Pi_4$ *magnitudes* M2 reports are a fit-order artifact (a bare quartic fit is ill-conditioned at these $q$-scales — a $q^6$-augmented fit shifts every variant by $\sim2.6$–$3\times$, sign-preserving) that this finding had not disclosed. Fixed: leg **M2b** added (the referee's own perturbation, kept as a permanent regression check rather than a one-off), M2's claim narrowed to sign/order-of-magnitude, and the caveats below updated. See `docs/reviews/F383-review-2026-09-10.md`.

**Target.** Rubric row **E1** (`POSIT`), ledger row **E1g** (`docs/status/open-derivations.md` Part C). F345 (2026-09-01, reviewed CONFIRMED-NARROWER) narrowed E1's posit to one sentence — *"that the long-wavelength description of the lattice is a local, diffeomorphism-invariant metric theory at all"* — with **two open sub-items named inside it**: **at-most-second-order** (holds only to $\sim10^{-76}\times$ an **uncomputed** $O(1)$ coefficient, per F345 §5/L4) and **metric-only-LHS** (closed for Brans–Dicke and $f(R)$ only). This finding attacks the first sub-item.

**The question.** Can the lattice's own locality — finite-range coupling, a compact Brillouin zone — *forbid* the four-derivative (curvature-squared) term in the induced gravitational action outright, which would promote at-most-second-order from posit to derivation? Or does locality only ever *suppress* such terms, generating a full derivative tower with generically nonzero coefficients (ordinary Wilsonian EFT), which would instead close the sub-item **negative** — provably not exact, only parametrically small?

**The answer: negative.** Locality does not forbid the four-derivative term. It generates it, via the identical mechanism that already generates the accepted two-derivative (Einstein–Hilbert) term.

---

## 1. The route: extend F57's own machinery one order further

F56 assumed a Sakharov induced Einstein–Hilbert term; **F57** (2026-05-29) *exhibited* it as an explicit, finite lattice integral — the static matter-density polarization over the model's own F26/BCC dispersion $\omega(\mathbf k)$ (`casim.engine.lattice.bcc.bcc_dispersion`):

$$\Pi(\mathbf q) = \int_\text{BZ}\frac{d^3k}{(2\pi)^3}\,\frac{1}{\omega(\mathbf k)+\omega(\mathbf k+\mathbf q)}, \qquad \Pi(\mathbf q) = \Pi_0 - \Pi_2 q^2 + \Pi_4 q^4 - \dots$$

$\Pi_0$ is the vacuum-energy/$\Lambda$ sector (F56, $\propto\Lambda^2$); $\Pi_2>0$ is the induced Einstein–Hilbert kinetic coefficient (F57: $\Pi_2=+0.061$, UV-finite on the compact BZ, running logarithmically — Adler–Zee). $\Pi_4$, the **next term in the same small-$q$ expansion**, is in position space the coefficient of $(\nabla^2\Phi)^2$ — the scalar/rest-leg-channel analogue of a four-derivative curvature-squared operator. This finding computes it, using the **canonical** dispersion module rather than F57's fork copy, and asks whether it is forced to vanish or is generically present.

**What this does *not* claim.** $\Pi_4$ is not the gravitational $R^2$/$\mathrm{Ricci}^2$ Wilson coefficient F345 L4 called uncomputed — that lives in the tensor $T_{ij}T_{kl}$ (kinetic-leg, F55) channel, which F57 itself left open. $\Pi_4$ is a **proxy**: the same *kind* of object, in the one channel the tree has actually computed at two-derivative order, extended one order further. A nonzero $\Pi_4$ answers the narrower, logically prior question — can locality force such a coefficient to zero — not the numerical value of F345's uncomputed coefficient.

## 2. Legs

| Leg | Claim | Result | Verdict |
|---|---|---|---|
| M1 | quartic fit still reproduces F57's $\Pi_2$ | $\Pi_2=0.0615$ (quadratic-only fit) vs $0.0756$ (quartic fit) — same sign, same order of magnitude as F57's $0.061$ | PASS |
| M2 | $\Pi_4$'s **sign** is nonzero and robust across independent perturbations, at a quartic fit | baseline $0.555$; finer grid $0.523$; wider $q$-window $0.187$; body-diagonal direction $0.568$ — **same sign in all four**, ratio max/min $=3.0<5$, fit $R^2>0.999$ throughout | PASS |
| M2b | $\Pi_4$'s sign (not magnitude) survives adding a $q^6$ term — the adversarial-review perturbation, kept as a permanent check | order-6 values: $1.511,\ 1.410,\ 0.489,\ 1.712$ — **same sign as order-4 in all four**, shift factor $2.6$–$3.0\times$ per variant, order-6 ratio max/min $=3.5<8$ | PASS |
| M3 | $\Pi_4$ converges under grid refinement (genuine finite integral, not a quadrature artifact) | $n_\text{grid}=64,96,128,160$: $\Pi_4=0.409,0.508,0.478,0.422$ — bounded, relative change shrinking, no divergence | PASS |
| M4 | $\Pi_4$ stays finite across a swept cutoff | flat to 4 significant figures ($\approx0.2937$) over $\Lambda=1.2$–$2.4$, then a jump to $1.65$ at $\Lambda=2.8$ — **flagged, not smoothed over**: the jump is not diagnosed (plausibly a cube-domain quadrature artifact as the window nears the $\pi$ BZ-proxy edge) and is explicitly **not** load-bearing for M2/L | PASS (finiteness only) |
| M5 | direction dependence (axis / face-diagonal / body-diagonal) | $0.4511,\ 0.4455,\ 0.4531$ — same sign, isotropic to $1.7\%$ in the sample tested | PASS |
| L | conclusion | given M2, at-most-second-order is **not** forced by locality | PASS |

Full values, all four M2 variants and the M4 cutoff sweep: `test-results/F383_four_derivative_locality.json`.

## 3. Why this settles the question in the negative

The logic is the same argument F345 §1 already made explicit for the two-derivative order and did not carry through to the four-derivative order: **any** $E_{\mu\nu}$ derived from a local, diffeomorphism-invariant action is automatically conserved by Noether — divergence-freedom does not select the two-derivative term over a four-derivative one. What *would* select it is a special identity making the four-derivative variation vanish, the way the Gauss–Bonnet variation vanishes identically in $d=4$ (F345 L3, the Lanczos–Bach identity). But that identity is a property of the **full nonlinear curvature-squared invariant under metric variation** — it has no analogue in a scalar matter-density polarization, which is what $\Pi_4$ is. Nothing in this model's construction gives $\Pi_2, \Pi_4, \Pi_6,\dots$ a reason to vanish at any order; each is simply the next moment of a smooth, bounded integrand over a compact domain, generically nonzero, as $\Pi_4$'s robust positivity across four independent numerical checks now confirms directly rather than by analogy.

So: **locality is why every term in the derivative expansion is UV-finite (the compact BZ removes the regulator ambiguity F56 called "scheme-dependent," exactly as F57 argued for $\Pi_2$) — it is not why the expansion stops.** That is the ordinary content of a Wilsonian effective field theory: an EFT converges term-by-term because each operator is suppressed by additional powers of (scale/cutoff), not because the tower is truncated by symmetry. F319 already carried this reading for the *matter*-sector dimension-6 operator; this finding carries it, for the first time with a computed nonzero coefficient rather than a stated expectation, into the *gravity* sector F345 L4 left uncomputed.

**Net effect on F345 L7 / ledger E1g.** The "at-most-second-order" sub-item is not promoted to a derivation — the opposite: it is now positively established (not merely assumed) that no locality-based mechanism can promote it, in the one channel this tree can actually compute. What F345 already called an order-of-magnitude suppression ($\sim10^{-76}\times$ an uncomputed $O(1)$) is now known to have a **structurally nonzero** $O(1)$, at least in the scalar/Newtonian channel — closing the "is it perhaps exactly zero by some undiscovered symmetry" possibility that F345 §5 left open, without needing to. Row **E1** stays `POSIT` for the reason F345 already gives (the surviving one-sentence premise); this finding removes one route that could have shrunk it further, and records that removal as a result rather than leaving it silently unexamined.

## 4. Ledger disposition

Per the task framing (derive the posit, or prove a piece of it underivable and move it to Part B): this finding proves the **at-most-second-order-by-locality** route underivable, and adds a `docs/status/open-derivations.md` Part B row (CN28) recording that as a closed-negative result, cross-referenced from E1g's Part C entry rather than replacing it — E1g's own posit content (F345's one-sentence premise) is unchanged.

## 5. Test record, controls

**Test record:** `F383-four-derivative-locality` (`tests/registry/interactions.yaml`, kind `result_dump`, tier `battery` — matching F57's own precedent for this class of BZ-quadrature measurement, not an exact/symbolic assertion). 7/7 legs PASS. `path: tests/findings/test_F383_four_derivative_locality.py`. No D9 controls declared (a `result_dump` record fails by baseline diff against git HEAD, per D9; the baseline is armed on first commit).

**Also this session:** F345's three previously-stale declared controls (`lovelock_dim=5`, `gb_ricci_coeff=-3`, `model_gamma=0.999999`) were re-run and journalled via `tools/check_control_soundness.py --run --id F345-field-equation-uniqueness` (i.e. `make control`) and all three verified RED exactly as declared (`test-results/control-soundness.json`), clearing the stale flag noted in the research prompt. Note for future sessions: `casim test --control` verifies but does **not** persist the verdict to the journal `check_control_soundness.py --gate` reads unless given an explicit `--journal PATH` — `make control` is the form that actually arms it.

## 6. Caveats

- **The specific $\Pi_4$ magnitudes in M2's table are a fit-order artifact, not a converged number — only the sign and order of magnitude are numerically supportable.** A bare quartic (order-4) fit is ill-conditioned at the $q$-scales used ($q^2$ and $q^4$ are nearly degenerate over a narrow small-$q$ window): adding a $q^6$ term (leg M2b) shifts every variant's $|\Pi_4|$ by $\sim2.6$–$3\times$ (e.g. baseline $0.555\to1.511$), never flipping the sign. This was found independently twice — by this session's blind-rederivation subagent (which needed the same $q^6$ correction to stabilize its own estimate) and by its adversarial referee (who reran M2's own settings at order 6) — and was **not disclosed** in the finding's first version. M2b is now a permanent regression check of what does survive (sign, magnitude within an 8× band); nothing in this finding's prose ever asserted a $\Pi_4$ value to more than order-of-magnitude precision, but the table's 3-sig-fig numbers invited that reading, which this note forecloses.
- $\Pi_4$ is computed on the same cube-domain BZ proxy ($[-\Lambda,\Lambda)^3$, $\Lambda=\pi$) F57's fork used, not the exact truncated-octahedron BCC Brillouin zone. F57 itself used this proxy without incident; carried here for direct comparability, not re-justified.
- The M4 cutoff-scaling anomaly at $\Lambda=2.8$ is unresolved. It does not touch this finding's conclusion (M2, not M4, is what L depends on) but is named as a follow-up rather than hidden.
- This finding does not compute the actual gravitational $R^2$/$\mathrm{Ricci}^2$ Wilson coefficient F345 L4 called uncomputed. That remains open, and remains the natural next step (the kinetic-leg $T_{ij}T_{kl}$ channel F57 §"what is reduced vs what remains" already named).
- The metric-only-LHS sub-item (F345 §6/§7) is untouched here.

**Cross-references:** [[F345-field-equation-uniqueness-lovelock]] (the residual this answers, L4/L7), [[F57-induced-eh-term-from-leg-field-backreaction]] (the $\Pi(q)$ mechanism extended here), [[F56-einstein-coupling-from-lattice-phase-matching]] (the assumed-Sakharov starting point, $\Pi_0$ sector), [[F319-uv-sector-reconciled-physical-cutoff-and-counterterms]] (the matter-sector sibling statement — dimension-6 operators present, not computed, not forced to zero), [[F178-gravity-full-tensor-adoption]] (the decision this is downstream of), [[F291-why-three-plus-one-dimensions]] / [[F326-the-plus-one-closes-no-second-generator]] (the derived $d$ that F345 L3's protection depends on — not re-used here, since this finding's channel has no analogous protection).

**Test record:** none beyond §5. **Claim:** none — this closes a candidate promotion route (does locality force at-most-second-order?) with a negative result; it does not itself extend, derive, or contradict Standard Model/QM/GR/SR content beyond what F345 already established, so no new card is issued per decision D12's bar ("extends established physics," not "is interesting"). It leaves CL292 unchanged (its premise, falsifier and status stand as written) — CL292 never claimed at-most-second-order was exact, only that it needs $\sim10^{-76}\times$ an uncomputed $O(1)$, which this finding does not narrow, only forecloses one route to eliminating.
