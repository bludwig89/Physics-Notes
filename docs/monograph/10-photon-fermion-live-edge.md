# Chapter 10 — Photon ↔ fermion: the coupled channels and the push — the live edge

*Chapter 10 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F387-curl-anisotropy-omega-pair-mismatch.md`, `findings/F388-fermion-photon-coupled-channels.md`,
`findings/F389-radiative-transverse-em-current.md`, `findings/F390-photon-fermion-push-scenario.md`,
`findings/F391-ck-transverse-beam-mechanism.md`, `findings/F392-beam-polarization-null-fix.md`,
`findings/F393-curl-grad-identity-diagnostic.md`, `findings/F394-bcc-dec-curl-part-c-decision.md`,
`findings/F395-stage5-circular-beam-rerun.md` — the nine findings `00-plan.md` §2 assigns to this chapter,
all read in full, dated 2026-09-15 through 2026-09-16, the most recent activity in the repository as of
this writing (2026-09-17) — cross-checked against their independent attack-and-fix reviews
(`docs/reviews/F387-review-2026-09-15.md` through `docs/reviews/F395-review-2026-09-16.md`, all nine
present and read), `docs/claims/CL307-photon-fermion-push-partial-recoil-not-conservation.md` (read in
full, the chapter's one claim card), and the relevant tail of `docs/status/changelog.md`
(2026-09-15/16 entries — legitimate primary source material for this specific chapter, per the build
instructions, since the changelog's blow-by-blow narrative *is* the investigation's own record of what
was tried, found, and fixed in what order). Numbers were spot-checked against the committed result
artifacts (`test-results/F387_curl_anisotropy_omega_pair_mismatch.json`,
`test-results/F388_fermion_photon_coupled_channels.json`,
`test-results/F389_radiative_transverse_current.json`, `test-results/F389_radiative_current_backreaction.json`,
`test-results/F390_photon_fermion_push.json`, `test-results/F391_ck_transverse_beam_mechanism.json`,
`test-results/F392_beam_polarization_null_fix.json`, `test-results/F393_curl_grad_identity_diagnostic.json`,
`test-results/F395_stage5_circular_beam_rerun.json` — F394 has no test record, an analysis-only deferral
decision) and found to reproduce the findings' own reported values exactly, not merely approximately.
Notation, postulates and results are those of Chapters 1, 8 and 9
(`01-postulates-and-ontology.md`, `08-the-photon.md`, `09-electromagnetism.md`) — $\mathbf k$,
$\Omega_\text{pair}(\mathbf k)$, $\hat{\mathbf C}(\mathbf k)$, $\rho$, $\mathbf J$, $\mathbf A$, R8.1–R8.16,
R9.1–R9.12 — extended, never redefined.

**This chapter documents ongoing, unresolved research, not a settled result.** Every other chapter in this
monograph presents a derivation that closed — exactly, to machine precision, or as a characterized no-go
with a stated reason it cannot close. This chapter presents a derivation that has **not** closed, is
actively being worked on as of the date these findings were written, and whose own authors — across nine
findings and nine independent adversarial reviews, all in the space of about 40 hours of project time —
repeatedly found their own first-draft claims to be *factually wrong as written* and rewrote them narrower.
The question is simple to state: does a photon beam push a fermion the way momentum conservation says it
must? The honest answer, as of the latest work in this repository, is: **the model gets the push's
direction right, in a narrow domain, for a reason nobody has derived; it does not conserve momentum, for a
reason that is understood; and every fix attempted for the direction's own narrow domain has changed
nothing, which is itself the chapter's most informative result.** This chapter narrates the investigation
stage by stage (§10.3, F387→F395), reports every number as measured, and keeps the failures in view rather
than smoothing them into a clean line.

## 10.1 Inputs

**Postulates used.** **P4** (exact unitarity) is what every exactness claim in this chapter's settled
sub-results (the transversality identities, the translation-covariance check) rests on, exactly as it did
in Chapters 8 and 9. **P5** (the primitive field is a Weyl 2-spinor $\psi\in\mathbb C^2$) is what every
finding in this chapter works with — the massive Dirac case is explicitly out of scope everywhere in this
chapter, inherited unchanged from Chapter 9's own scope statement. **P6** (the chiral $SU(2)$ connection)
is background, not re-examined here; this chapter's whole construction sits inside the already-isolated
U(1) electric-charge channel Chapters 8–9 built.

**Prior results used, precisely.** **R8.4/R8.5** (the paired photon, its dispersion $\Omega_\text{pair}$,
non-birefringence) is the photon channel every finding in this chapter couples to. **R9.4/R9.5** (F384, the
BCC Weyl walk's exactly conserved current, $\rho$ trivial and $\mathbf J$ the minimal purely
$\hat{\mathbf C}(\mathbf k)$-longitudinal solution to discrete continuity) is the current this chapter's
entire investigation turns on — its purely-longitudinal character, flagged in F384 itself as "free,
unconstrained gauge freedom" left unassigned, is the single fact from which almost everything else in this
chapter follows. **R9.6/R9.7** (F385, the per-link covariant U(1) step, exact for uniform $\mathbf A$,
trading unitarity for an $O(|qA|\cdot a)$ momentum transfer for curl-carrying $\mathbf A$) is the field→
fermion recoil mechanism every scenario in this chapter uses unmodified. **R9.8/R9.9** (F386, the
Coulomb-gauge `solve` convention for $\mathbf A$) is the field convention every coupled channel in this
chapter reads. This chapter picks up exactly where Chapter 9's §9.7 hand-off stops, and explicitly
confirms — rather than merely inherits — the two technical seams that section named as the ones a reader
should expect this investigation to hit first: the curl-carrying-vs-curl-free scope limit of the per-link
step (R9.7), and the $\Omega_\text{pair}(\mathbf k)$-vs-$|C_\text{odd}(\mathbf k)|$ propagator mismatch
Chapter 9's own review traced. Both are hit, in the chapter's very first finding (§10.3.1).

**Free inputs consumed.** Nothing new. This chapter introduces no new fitted constant; every number
reported below is a measured consequence of the already-fixed lattice rule, the already-adopted photon
(decision 5) and current (F384) constructions, and the coupling constants $q$ (fermion charge) and
$g_\text{lat}$ (the field-sourcing strength), both of which are scenario *parameters* this chapter sweeps,
not new physical inputs to the model. The one genuinely open modelling choice this chapter's whole narrative
turns on — *which* $\hat{\mathbf C}(\mathbf k)$-transverse current to add to F384's minimal solution
(§10.3.3) — is disclosed precisely as a constitutive choice, not a derivation, at the point it is made.

## 10.2 Chapter-wide caveat on exactness classes

Unlike every prior chapter, most of this chapter's numbered results are not closed-form identities or
machine-precision checks of one. A handful are (the transversality/continuity algebra in F387–F389, F392's
null-field construction, F395's translation-covariance check) and are labelled `exact`/`machine` in the
results table accordingly. The majority are **quantitative, threshold, or purely negative/characterization
results on a genuinely dynamical, 20-tick coupled-channel run** — cosine correlations between measured
momentum vectors, scaling exponents fit to a handful of coupling-strength doublings, a residual that is
"not achieved," a ratio that "spans an order of magnitude with no principled comparison value." These are
reported with the same numerical precision the source findings use, but a reader should not read five or
six significant figures on a correlation coefficient as a claim of algebraic exactness — it is the
precision of the measurement, on the one run configuration tested, not a claim about every configuration.
Every finding in this chain is explicit about this distinction in its own text, and this chapter preserves
that distinction rather than erasing it for uniformity with earlier chapters.

## 10.3 The derivation — a research narrative, stage by stage

### 10.3.1 F387 — the curl generator's own direction is anisotropic, and the fix is a sector split, not a propagator swap

Chapter 9's own hand-off (§9.7) left two structural facts open, both surfaced by the review of F386: whether
`bcc_curl_symbol`'s direction anisotropy needed its own finding, and what Stage 4 of the coupling roadmap
should do about $\Omega_\text{pair}(\mathbf k)$ and $|C_\text{odd}(\mathbf k)|$ — the paired photon's own
scalar dispersion and the Maxwell curl generator's magnitude — being different functions of $\mathbf k$.

**The direction anisotropy.** `bcc_curl_symbol`'s direction does not converge to $\hat{\mathbf k}$ as
$\mathbf k\to0$ off the cubic axes:

| Direction | $\angle(\hat{\mathbf C}(\mathbf k),\hat{\mathbf k})$ | Predicted |
|---|---|---|
| cubic axis $(1,0,0)$ | $0.000000°$ | $0°$ |
| face diagonal $(1,1,0)$ | $90.000000°$ | $90°$ |
| body diagonal $(1,1,1)$ | $70.528779°$ | $\arccos(1/3)$ |

stable exactly from $L=16$ to $L=256$ — a genuine continuum-limit property, not a finite-lattice artifact.
The exact limiting direction is $\hat{\mathbf C}(\mathbf k)\to(k_x,-k_y,k_z)/|\mathbf k|$: the same sign
convention `_bcc_uvec` carries for the fermion walk's own spin-quantisation axis (`bcc_spin_axis`), correct
and load-bearing there for spin–momentum locking, reused unchanged when `bcc_curl_symbol` repurposes the
same object as a Maxwell curl generator for the photon's $(\mathbf E,\mathbf B)$ field — a different
physical quantity the sign convention was never previously flagged as defining "transverse" for. The
magnitude is unaffected ($|\mathbf C|/|\mathbf k|\to1/\sqrt3$ isotropically to $O(k^2)$), so every existing
speed/$c_\text{lat}$ check (F87's own MX1, F26) is untouched.

**The $\Omega_\text{pair}(\mathbf k)/|C_\text{odd}(\mathbf k)|$ mismatch — real, but not the cause of
anything.** The two agree only at small $k$ ($1.000134$ at the smallest nonzero mode, $L=64$), diverging to
a factor of $1.954$ at the Brillouin-zone edge — a genuine, quantified disagreement. F387's first-pass prose
attributed the sourcing pipeline's own "no magnetic monopoles" violation to this mismatch; **the review
tested that attribution directly by elimination** — substituting $|C_\text{odd}(\mathbf k)|$ exactly for
$\Omega_\text{pair}(\mathbf k)$ inside an otherwise-identical rotation step still produces
$\|i\hat{\mathbf C}\cdot\mathbf B\|=2.485$ by tick 6, *larger* than the $2.415$ measured with the real
$\Omega_\text{pair}$, not smaller. **The mismatch is not the driver, even partially, of the defect this
finding was built to fix.** The actual, structural, value-independent cause: `photon_step_spectral` applies
the *same* 2×2 rotation to every Cartesian component of $(\mathbf E,\mathbf B)$ identically, performing no
$\hat{\mathbf C}(\mathbf k)$-projection whatsoever — true of *any* scalar per-mode rotation law, matched to
$|C_\text{odd}(\mathbf k)|$ in value or not. F384's own conserved current is purely longitudinal by
construction (R9.5), so sourcing $\mathbf E$ with it and rotating with no transverse/longitudinal
distinction necessarily rotates a purely-longitudinal $\mathbf E$ into a nonzero longitudinal $\mathbf B$:
$i\hat{\mathbf C}\cdot\mathbf B\ne0$, growing every tick — a genuine violation of the model's own no-monopole
invariant, measured at $2.41$ by tick 6 under the roadmap's own literal recipe.

**The fix: a sector split, not a propagator swap.** Because the $\Omega_\text{pair}$ rotation and the
$\hat{\mathbf C}(\mathbf k)$-transverse/longitudinal projector act on different tensor factors of the
6-dimensional per-mode $(\mathbf E,\mathbf B)$ space, they commute exactly (measured $\|\Delta\|\approx
2.9\times10^{-14}$ on random fields of norm $\approx72$ — relative $\approx4\times10^{-16}$, machine
round-off). $\Omega_\text{pair}$ stays the propagator for the genuine radiative (transverse) sector exactly
as decision 5 established; the $\hat{\mathbf C}(\mathbf k)$-based Gauss/current machinery stays the sourcing
law for the non-propagating (longitudinal, Coulomb) sector, carried forward algebraically each tick from
F384's own continuity law with $\mathbf B_L$ never populated at all. Measured on the same scenario:
$\|i\hat{\mathbf C}\cdot\mathbf B\|$ at tick 6 drops from $2.41$ (naive) to $2.76\times10^{-16}$ (split) —
by construction, not cancellation, since $\mathbf B_L$ is structurally never assigned a value — while the
charge's own Coulomb field still correctly grows ($\|\mathbf E_L\|=0.298$).

$$\boxed{\;\hat{\mathbf C}(\mathbf k)\to(k_x,-k_y,k_z)/|\mathbf k|\text{ exact, }L\text{-stable; the }\Omega_\text{pair}/|C_\text{odd}|\text{ mismatch is real but ruled out (by elimination) as the no-monopole defect's cause; the actual cause is any scalar rotation law's lack of a }\hat{\mathbf C}(\mathbf k)\text{-projection; fixed by an exact-commuting transverse/longitudinal sector split, }2.76\times10^{-16}\text{ residual vs. }2.41\text{ naive}\;}\tag{R10.1}$$

(F387, 12/12 legs PASS, one control verified red on exactly the two declared legs; reviewed
CONFIRMED-NARROWER, the review's own attribution correction now the finding's own §2 text; test record
`F387-curl-anisotropy-omega-pair-mismatch`, gate tier.) No claim card — D12 scope, an engine-capability
design fix, not an assertion against established physics.

### 10.3.2 F388 — the coupled channels wire up correctly, and immediately prove they cannot radiate

`EmPhotonChannel`/`FermionEmChannel` wire F384's current, F385's per-link step, F386's $\mathbf A$-solve and
F387's sector-split sourcing into a genuine two-way coupled loop, mirroring the pre-existing fermion↔W loop.
The wiring itself is confirmed correct — registration order, the pre-tick/post-tick contract, the topology
fix letting a photon channel share a lattice with BCC fermion channels for the first time — 7/7 gate legs
PASS. **The load-bearing result is not the wiring; it is what the independent review found by measuring,
not assuming, what the wired loop actually does.**

**The current cannot radiate, and this is forced, not incidental.** F384's `conserved_current` is *defined*
as the unique minimal purely-$\hat{\mathbf C}(\mathbf k)$-longitudinal solution to discrete continuity — its
own docstring says so. Measured directly across five fermion configurations (widths 1–4, various $k_0$,
centred and off-centre): the current's own transverse fraction $\|\mathbf J_T\|/\|\mathbf J\|$ is
$2.1$–$2.4\times10^{-16}$ in *every* case — floating-point noise, not a small physical effect, and not a
property of any one packet. Since `em_photon`'s only source term is $g_\text{lat}\cdot\mathbf J_T$, this
means **the fermion's own current cannot make the photon channel's radiative sector nonzero, ever, at any
coupling strength or run length**, under this current's construction. Verified directly on the real
channels, current-only (no seeded photon) scenario, 20 ticks: $\|\mathbf E\|$ and $\|\mathbf B\|$ both stay
at the noise floor ($1.0$–$1.6\times10^{-17}$) for the entire run.

**Consequence: total momentum is not conserved, at all, by this construction.** On the seeded-photon
scenario ($L=16$, $g_\text{lat}=0.5$, $q=1$, $\text{photon\_amp}=0.15$), tracking both legs of the momentum
observer tick by tick: $\Delta P_\text{field}$ stays at $\sim10^{-20}$–$10^{-21}$ (machine noise) for the
full run, while $\Delta P_\text{matter}$ grows to $\sim1.9\times10^{-5}$ by tick 20. Extended to 100 ticks
(found in review, not gated): $\|\Delta p\|$ keeps rising past tick 20, **peaks at $\sim5.6\times10^{-5}$
around tick 54, then declines back to $\sim2.7\times10^{-5}$ by tick 100** — a slow envelope oscillation set
by the seeded mode's own $\Omega_\text{pair}$, not a stable plateau and not unbounded secular growth
either. **The field pushes the fermion (through $\mathbf A$, which does carry genuine transverse content
when seeded); the fermion never pushes back, because the only channel available for that — the current's
transverse part — is structurally zero.** This is not an implementation bug; it is a direct, load-bearing
consequence of F384's own current definition, made concrete for the first time in a live coupled loop, and
the review states plainly: "whoever picks up Stage 5 needs to know this before attempting claim 1."

$$\boxed{\;\text{the coupled channels are correctly wired (7/7 PASS), but F384's current's own transverse fraction is }2\text{--}2.4\times10^{-16}\text{ on every configuration tested — structurally zero, not small — so this loop cannot radiate; }\Delta P_\text{field}\sim10^{-20}\text{ while }\Delta P_\text{matter}\text{ grows to }\sim1.9\times10^{-5}\text{ (20 ticks), peaking }\sim5.6\times10^{-5}\text{ at tick 54, declining to }\sim2.7\times10^{-5}\text{ by tick 100 — total momentum not conserved, at any precision, by construction}\;}\tag{R10.2}$$

(F388, 7/7 legs PASS, two controls each verified red on exactly one leg; reviewed CONFIRMED-NARROWER — 6
PASS/5 WEAKENS/2 FAIL of a 13-point attack; the blind subagent independently surfaced this exact gap from
F384's own docstring, and the referee measured its consequence directly; test record
`F388-fermion-photon-coupled-channels`, gate tier.) No claim card — D12 scope.

### 10.3.3 F389 — a physically motivated transverse current lets the loop radiate, but the two channels are not order-matched

Discrete continuity is *one* linear constraint per Fourier mode on $\tilde{\mathbf J}(\mathbf k)$ — its
projection along $\hat{\mathbf C}(\mathbf k)$ — and is provably blind to anything perpendicular to it
(verified bit-identical, not merely small: adding any $\hat{\mathbf C}(\mathbf k)$-transverse field to
F384's current cannot perturb the continuity residual at all). **This is forced.** What is *not* forced,
and is disclosed as a constitutive choice rather than a derivation: *which* transverse field to add. F389
takes the naive continuum Weyl Noether bilinear $\mathbf J_\text{naive}=q\,\psi^\dagger\boldsymbol\sigma\psi$
— the same bilinear the SU(2)/SU(3) currents already use, and the one F384 itself rejected as the *whole*
current because its longitudinal projection only closes continuity to $O(a)$ — restricted to exactly the
transverse projection continuity never constrained, and adds it to F384's exact longitudinal solution:
$\mathbf J_\text{full}=\mathbf J_\text{exact}^L+\mathbf J_\text{naive}^T$.

**Verified, gauge sector (3/3 PASS):** continuity residual bit-identical between $\mathbf J_\text{full}$ and
$\mathbf J_\text{exact}^L$ (diff $0.0$); the transverse fraction is now genuinely nonzero,
$\|\mathbf J_\text{full}^T\|/\|\mathbf J_\text{full}\|=0.687$ on an evolved (non-degenerate) test packet, not
the $\sim2\times10^{-16}$ noise floor.

**Consequence for the coupled loop, self-sourced-only scenario, $g_\text{lat}=0.3$ (4/4 PASS):** field
momentum, machine-zero under F388's current on every configuration tested, is now genuinely nonzero
($2.25\times10^{-4}$, was $5.1\times10^{-36}$) and recovers a real, non-vanishing fraction ($\sim11\%$ at
this coupling) of the matter's momentum loss ($\|\Delta P_\text{field}\|/\|\Delta P_\text{matter}\|=0.111$).
**The loop can now radiate and recoil.**

**But exact conservation is not achieved, and the reason is structural, not a tuning defect.** Measured at
every coupling doubling tested: $\|\Delta P_\text{matter}\|$ scales *linearly* in $g_\text{lat}$ (ratio
$1.986$–$2.00$); $\|\Delta P_\text{field}\|$ scales *quadratically* (ratio $3.99$–$4.01$). The recovered
fraction is therefore itself $O(g_\text{lat})$, growing to $\sim70\%$ by tick 300 at $g_\text{lat}=0.5$ in an
extended, non-gated run, but reaching exact cancellation at **no** coupling or run length tested, and there
is no regime in which the two mechanisms' orders match. **Why the orders don't match, stated precisely:**
in continuum electrodynamics with a linear self-consistent Lorentz-force coupling, momentum conservation is
exact because the matter and field equations of motion are two halves of *one* covariant action, and the
Noether identity $\partial_\mu T^{\mu\nu}=0$ does the actual work — it is not a perturbative accident. This
model's two channels were **not** built that way: F385's per-link recoil and F389's current construction are
two separately-derived, separately-audited numerical prescriptions bridged together in `core.coupled`, not
two halves of one gauge-invariant lattice action. The fermion's recoil is $O(g_\text{lat})$ because it
responds linearly to the self-sourced $\mathbf A$; the field's momentum is $O(g_\text{lat}^2)$ because
$\mathbf E\times\mathbf B$ needs both factors sourced, and only $\mathbf E$ is directly sourced each tick.
**Deriving both channels from one single gauge-invariant lattice action, so a genuine discrete Noether
identity forces order-by-order conservation, is a strictly bigger undertaking than either construction
individually, and is not attempted anywhere in this chapter's investigation.**

$$\boxed{\;\text{a }\hat{\mathbf C}(\mathbf k)\text{-transverse current (disclosed constitutive choice, forced only in its continuity-safety) lets the loop radiate — field momentum }2.25\times10^{-4}\text{ (was }5.1\times10^{-36}\text{), }11\%\text{ recovery at }g_\text{lat}=0.3\text{ — but }\|\Delta P_\text{matter}\|\propto g_\text{lat}\text{ while }\|\Delta P_\text{field}\|\propto g_\text{lat}^2\text{ at every doubling tested: exact conservation unreachable at any coupling because the two channels are two independently-derived prescriptions, not one covariant action with a forced Noether identity}\;}\tag{R10.3}$$

(F389, 7/7 legs PASS across two records, three controls each verified red on the declared legs; reviewed
CONFIRMED-NARROWER — 11 PASS/2 WEAKENS/0 FAIL/1 NOT RUN, the blind agent independently reconstructed the
same construction by the same route; two prose overclaims fixed — "derives, rather than guesses" softened,
a single-tick-vs-trajectory ambiguity scoped; test records `F389-radiative-transverse-current` (gauge),
`F389-radiative-current-backreaction` (core), gate tier.) No claim card — D12 scope.

### 10.3.4 F390 — the push scenario: direction confirmed on-axis only, conservation not achieved, magnitude not well-posed

Stage 5 builds the actual scenario the roadmap named: a genuine $\hat{\mathbf C}(\mathbf k)$-transverse beam
packet pushes a localized Weyl fermion at rest, with F389's radiative current letting the fermion's own
recoil source real field momentum back. **This finding's own first version overclaimed its results, and the
independent review found this directly, using data it produced itself in the same review cycle** — this is
recorded here as part of the investigation's honest record, not smoothed over.

**Claim 2 (direction).** Confirmed, but on-axis and small-carrier-wavenumber only. At the default
configuration ($m_\text{index}=2$, beam along the lattice's x-axis): $\cos(\Delta P_\text{matter},
\hat{\mathbf k}_\text{beam})=0.995$. The first version's finding text read "Direction — CONFIRMED," with no
qualifier; **the review tested the one dimension the disclosed sweep never varied — the beam's propagation
axis — and going to $m_\text{index}=4$ (simply double the default wavenumber, an entirely ordinary
configuration) reverses the sign**: $\cos=-0.988$. A beam along the y- or z-axis decorrelates the direction
entirely: $\cos\approx-0.0019$ (y), $\cos\approx-0.0093$ (z).

$$
\begin{array}{|l|c|c|}
\hline
\text{Beam config} & \cos(\Delta P_\text{matter},\hat{\mathbf k}_\text{beam}) & \cos(\Delta P_\text{matter},\Delta P_\text{field}) \\
\hline
m_\text{index}=1,\ \text{axis}=x & 0.991 & \text{—} \\
m_\text{index}=2,\ \text{axis}=x\ (\text{default}) & 0.995 & -0.989 \\
m_\text{index}=3,\ \text{axis}=x & 0.983 & \text{—} \\
m_\text{index}=4,\ \text{axis}=x & \mathbf{-0.988} & -0.978 \\
m_\text{index}=2,\ \text{axis}=y & \mathbf{-0.0019} & \mathbf{+0.99995} \\
m_\text{index}=2,\ \text{axis}=z & -0.0093 & \text{—} \\
\hline
\end{array}
$$

**Claim 1 (momentum conservation).** Not achieved exactly at any coupling tested, confirming F389's
structural prediction extends to a beam-driven scenario. On-axis, a genuine partial positive result: field
and matter momentum changes are nearly anti-parallel, $\cos=-0.989$ at default — but this **inverts to
near-exactly parallel, $\cos=+0.99995$, for an off-axis beam** (the same $y$-axis config above), the
opposite of a momentum exchange. The conservation residual $\|\Delta P_\text{matter}+\Delta
P_\text{field}\|/\|\Delta P_\text{matter}\|$ is $0.174$ at the default (best-measured) coupling
$g_\text{lat}=0.6$, and has a reproducible local minimum there ($0.78$ at $g=0.3$ → $0.17$ at $g=0.6$ →
$0.86$ at $g=1.2$) — **shown, not merely disclaimed, to be a structurally guaranteed crossing point, not a
physical resonance**: with $\cos(\Delta P_\text{matter},\Delta P_\text{field})$ nearly constant and
$\|\Delta P_\text{matter}\|$ nearly flat while $\|\Delta P_\text{field}\|$ grows monotonically (linearly) in
$g_\text{lat}$, the law of cosines forces a convex residual curve with an interior minimum for *any*
configuration sharing these three qualitative properties, independent of whether the underlying physics is
close to conservation. $g_\text{lat}$ is also not "the coupling" for the scenario as a whole:
$\|\Delta P_\text{matter}\|$ changes by less than $0.4\%$ over $g_\text{lat}\in[0,3]$ (an eightfold range)
while scaling exactly linearly in $q\cdot\text{amp}$ at $g_\text{lat}=0$ — the matter push is set almost
entirely by the unconditional per-link push (F388 §2's mechanism), and $g_\text{lat}$ only ever governs how
much the field's own bookkeeping catches up to a push already fully determined by $q$ and the beam
amplitude.

**Claim 3 ($\Delta p=\Delta E/c$) — not gated, no physical basis found, reported as a precisely
characterized negative/inapplicable result.** $\|\Delta P_\text{matter}\|$ is $0.0410$ at $g_\text{lat}=0$
and stays within $0.4\%$ of that value across the whole tested range — set almost entirely by the
coupling-independent per-link push. Meanwhile $\Delta E_\text{field}$ is exactly zero at $g_\text{lat}=0$
and grows with $g_\text{lat}$, entirely a property of the separate radiative-sourcing mechanism. **These
two quantities are governed by different mechanisms with no shared coupling constant, so there is no
physical basis for expecting $\|\Delta P_\text{matter}\|\cdot c\approx\Delta E_\text{field}$, and they
manifestly do not track each other**: the ratio $\Delta p/(\Delta E_\text{field}/c)$ spans $29.8$
($g_\text{lat}=0.1$) down to $1.3$ ($g_\text{lat}=0.8$), formally undefined at $g_\text{lat}=0$ where the
push is cleanest. A cleaner alternative check — does the field's own radiated content satisfy $\Delta
E_\text{field}\approx c\|\Delta P_\text{field}\|$, independent of the fermion's accounting? — gives a ratio
rising from $0.26$ to $0.89$ over the tested range without reaching $1$, and can go negative at one
perturbation (width $3.0$) — not a stable, coupling-independent relation either.

**Claim 4 (Thomson cross-section) — deferred, and why.** Extracting a cross-section needs a genuine
far-field (this lattice is periodic/spectral — the beam wraps around and re-interacts within tens of ticks,
no asymptotic outgoing wave to a solid angle), a clean incident flux ($\sim27\%$ of the raw beam's norm is
discarded as $\hat{\mathbf C}(\mathbf k)$-longitudinal leakage after the necessary projection), and a
closing energy/momentum budget (neither exists, per claim 3's channel-decoupling). Deferred, not attempted.

$$\boxed{\;\text{claim 2 CONFIRMED on-axis, }m_\text{index}\le3\text{ only (}\cos=0.995\text{), REVERSES SIGN at }m_\text{index}=4\text{ (}\cos=-0.988\text{), DECORRELATES off-axis (}\cos\approx0\text{); claim 1's anti-alignment (}\cos=-0.989\text{ on-axis) INVERTS to near-parallel (}\cos=+0.99995\text{) off-axis, conservation residual }17.4\%\text{ at its own structurally-guaranteed minimum; claim 3 (}\Delta p=\Delta E/c\text{) NOT GATED — ratio spans }29.8\text{ to }1.3\text{, no physical basis; claim 4 deferred}\;}\tag{R10.4}$$

(F390, 8/8 legs PASS post-review — two legs added by the review specifically to permanently monitor the
axis breakdown — two controls each verified sound; reviewed CONFIRMED-NARROWER, 10 PASS/0 WEAKENS/3 FAIL of
13 attacks, the review finding the first-version headline claims factually wrong as written and
`docs/claims/CL307`'s own stated falsifier already triggered by data the same review cycle produced; test
record `F390-photon-fermion-push`, gate tier, `expect.exactness: quantitative`.) **This is the finding that
issues the chapter's claim card** — see §10.8.

### 10.3.5 F391 — the named mechanism is ruled out; the actual candidate is the fermion's own spin state, not derived

F390's own §3 and its review named a "likely, not derived" mechanism for the axis breakdown: F387's
$\hat{\mathbf C}(\mathbf k)$ axis anisotropy combined with `build_beam_packet`'s Euclidean-$\hat{\mathbf k}$
(not $\hat{\mathbf C}(\mathbf k)$) polarization convention, which leaks $27.5\%$ of the beam's own norm as
$\hat{\mathbf C}(\mathbf k)$-longitudinal content. F391 builds the fix this story predicts should matter — a
beam construction that projects the reference polarization onto each Fourier mode's own
$\hat{\mathbf C}(\mathbf k)$-transverse plane directly, not by projecting-and-discarding after the fact —
verified genuinely transverse to machine precision ($\|i\hat{\mathbf C}\cdot\mathbf B\|=7.6\times10^{-14}$,
longitudinal leak $3.1\%$, vs. the original's $27.5\%$).

**Result: the fix changes nothing.**

| Config | $\cos(\Delta P_\text{matter},\hat{\mathbf k})$ — new ($\hat{\mathbf C}(\mathbf k)$-transverse) | — old (F390 original) |
|---|---|---|
| on-axis default | $0.9926$ | $0.9948$ |
| $m_\text{index}=4$ (sign flip) | $-0.9874$ | $-0.9884$ |
| off-axis | $-0.0020$ | $-0.0019$ |

Every number agrees to 3 significant figures. **This directly falsifies the "likely mechanism" named by
F390 and its own review — ruled out, not merely unconfirmed.** `docs/claims/CL307`'s stated route back
toward `live` — "a derivation... that recovers the broad, axis-independent form" — is now known not to run
through this route.

**A sharper $\hat{\mathbf C}(\mathbf k)$ structural fact, found along the way.** F387's own table never
tested the y- or z-axis in isolation. Measured: $\hat{\mathbf C}(\mathbf k)$ is exactly *anti-parallel* to
$\hat{\mathbf k}$ on the lattice's own y-axis — $180.000000°$, not merely "some anisotropic angle" —
stable from $L=64$ to $L=128$, while z stays exactly aligned ($0°$), like x. This is exactly what F387's own
small-$k$ formula $\hat{\mathbf C}(\mathbf k)\to(k_x,-k_y,k_z)/|\mathbf k|$ predicts — the reflection
$R=\text{diag}(1,-1,1)$ applied to $\hat{\mathbf k}=\hat y$ gives $-\hat y$ exactly — simply never evaluated
at that specific direction before.

**What actually varies the push direction — a candidate, not a derivation.** A six-point diagnostic sweep
(beam axis × polarization axis, independently) found the recoil confined to the x–y plane in *every*
combination tested (never dominantly along z), and found that F390's own hand-picked default (axis=x,
pol=y) is the *only* one of six where the recoil tracks the beam's own direction — every other combination,
including the off-axis default F390's review used, pushes the fermion along a direction unrelated to either
the beam's $\hat{\mathbf k}$ or its polarization axis. **F390's on-axis success was not a representative
sample of a generally-working mechanism weakening at the edges; it was the one configuration, of six
tested, where an unidentified underlying bias happens to coincide with the beam's own direction.**

A genuinely new candidate: `FermionEmChannel.init_state` seeds a definite, fixed chirality eigenstate
($g\equiv0$) unconditionally, never varied before this finding. Replacing it with an equal superposition
($f,g\leftarrow f/\sqrt2,f/\sqrt2$), holding the beam configuration fixed (using the genuinely
$\hat{\mathbf C}(\mathbf k)$-transverse beam so §1's ruled-out mechanism cannot be responsible for any
difference): the recoil vector changes from $[-0.0330,-0.0001,-0.0000]$ to $[-0.0313,-0.0519,-0.0037]$ —
$\cos=0.517$ between the two, a large, unambiguous direction change, not a small perturbation. **This
finding does not derive the closed-form relationship between the fermion's spin state, the beam's
axis/polarization, and the resulting push direction** — the systematic scan or the derivation is left for a
future session, and is stated explicitly as such (§10.7).

$$\boxed{\;\text{a genuinely }\hat{\mathbf C}(\mathbf k)\text{-transverse beam (}3.1\%\text{ leak, was }27.5\%\text{) reproduces the on-axis correlation, the }m_\text{index}=4\text{ flip, and the off-axis decorrelation to 3–4 significant figures — the named mechanism is RULED OUT; }\hat{\mathbf C}(\mathbf k)\text{ is exactly anti-parallel to }\hat{\mathbf k}\text{ on the y-axis (}180°\text{, new exact fact); the recoil is confined to the x–y plane in all 6 (axis,pol) combinations tested, tracks the beam in exactly 1 of 6; varying the fermion's fixed spin state changes the recoil direction substantially (}\cos=0.517\text{) — the leading candidate mechanism, NOT DERIVED}\;}\tag{R10.5}$$

(F391, 9/9 legs PASS, one control verified red on exactly two legs; reviewed CONFIRMED-NARROWER — 7
PASS/1 WEAKENS/2 FAIL(fixed, tooling only)/3 NOT RUN of 13 attacks; a blind subagent independently
reproduced every headline number with a differently-coded construction; the one real defect found was a
mislabeled registry control block (F391's control declared a phantom leg belonging to F387's entry point),
fixed and re-verified; a separate, pre-existing, out-of-scope control defect on F387's own record was found
incidentally and spawned as a background task, not fixed in this pass; test record
`F391-ck-transverse-beam-mechanism`, gate tier, `expect.exactness: quantitative`.) No claim card — updates
CL307's evidence and falsifier reasoning directly rather than issuing a new one, per D12's bar for a
negative/redirecting result about an existing claim's domain restriction.

### 10.3.6 F392 — a second, independent beam defect: the original beam carried zero field momentum at all

Orthogonal to F391's transversality-convention fix, a 2026-09-16 audit
(`docs/audits/2026-09-16-photon-fermion-momentum-investigation.md`) found a second, independent defect in
`build_beam_packet` itself, re-verified against the real modules before any code was touched: $\mathbf E$
and $\mathbf B$ are placed in the *same* Cartesian component ($E[\text{pol\_axis}]=\text{Re}(F)$,
$B[\text{pol\_axis}]=\text{Im}(F)$), so $\mathbf E\parallel\mathbf B$ pointwise and the Poynting momentum
$\Sigma\,\mathbf E\times\mathbf B$ vanishes **identically**, not approximately, at every axis and carrier
mode. **F390's entire momentum-conservation test ran against a field with no field momentum to give in the
first place, by construction, independent of anything F387/F388/F389/F391 investigated.**

The fix: the model's photon *is* the Riemann–Silberstein field ($\mathbf F=\mathbf E+i\mathbf B$, decision
5); a genuine radiation field is null, $\mathbf F\cdot\mathbf F=0$ ($|\mathbf E|=|\mathbf B|$,
$\mathbf E\perp\mathbf B$). A new `polarization="circular"` option builds a genuine null field via a complex
circular polarization vector $\hat{\mathbf e}=(\hat{\mathbf e}_{a1}+i\hat{\mathbf e}_{a2})/\sqrt2$, giving
$\mathbf F\cdot\mathbf F=0$ exactly by construction. Verified: $|\mathbf E\cdot\mathbf B|/(\|\mathbf E\|
\|\mathbf B\|)=2.4\times10^{-17}$ (worst case), $|\|\mathbf E\|-\|\mathbf B\||/\|\mathbf E\|=2.0\times
10^{-16}$, momentum genuinely nonzero and aligned ($\cos(\mathbf P,\hat{\mathbf k})=1.000000$ at every
config, matching the audit's own $|\Sigma\mathbf E\times\mathbf B|=75.126$ number to six figures), and
conserved under free propagation over 40 ticks to $3.6\times10^{-15}$ relative drift. The default
(`"linear"`) mode is left bit-identical to git HEAD — every existing gate record built on it moves by zero
bits.

$$\boxed{\;\texttt{build\_beam\_packet}\text{'s default construction has }\mathbf E\parallel\mathbf B\text{ pointwise: }\Sigma\,\mathbf E\times\mathbf B\equiv0\text{ identically — F390's entire momentum test ran against a field with zero field momentum by construction; fixed with a genuine null Riemann–Silberstein construction, }\cos(\mathbf P,\hat{\mathbf k})=1.000000\text{, drift }3.6\times10^{-15}\text{ over 40 ticks}\;}\tag{R10.6}$$

(F392, 6/6 legs PASS, one control verified red on exactly 4 of 6 legs; reviewed CONFIRMED; test record
`F392-beam-polarization-null-fix`, gate tier.) No claim card — D12 scope, a test-helper defect and its
repair.

### 10.3.7 F393 — the missing half of the curl identity, gated honestly as a known, unrepaired defect

Discrete exterior calculus gives two identities from $d\circ d=0$. Only one, $\text{div}(\text{curl}\,
\mathbf A)=0$ (i.e. $\mathbf C\cdot(\mathbf C\times\mathbf x)\equiv0$), was ever gated — and it is
**vacuous**: true for *any* vector field $\mathbf C$ whatsoever, a property of the cross product, not of
$\mathbf C$. This is exactly the model's existing no-monopole gate, and why it stayed green throughout
F387–F392 while carrying no information about whether `bcc_curl_symbol` is a genuine curl. The other,
$\text{curl}(\text{grad}\,\varphi)=0$ (i.e. $\mathbf C\times\mathbf G=0$, requiring $\mathbf C\parallel
\mathbf G$), **actually constrains** $\mathbf C$ and was never tested anywhere in the codebase before this
finding — despite roughly 300 prior findings using `bcc_curl_symbol` as their curl generator.

`bcc_curl_symbol` **fails this identity maximally**: $|\mathbf C\times\mathbf G|/(|\mathbf C||\mathbf G|)$
averages $0.7417$ against the spectral gradient $\mathbf G=\mathbf k$ and $0.7072$ against the forward-
difference gradient — on average, "the curl of a gradient" is $74\%$ of its maximum possible magnitude, not
the $0$ a genuine curl generator gives identically. This finding adds the missing gate leg and leaves
`bcc_curl_symbol` itself completely unchanged — every existing consumer (F384/F386/F387/F388/F389/F390/F391)
is untouched, bit-for-bit. **Why not caught in $\sim300$ prior findings:** `bcc_curl_symbol` is not built
from a genuine discrete-exterior-calculus complex where both identities hold by construction; it is built
from the fermion walk's own spin-quantisation axis, reused as a Maxwell curl generator (F387 §1). Reuse does
not inherit either identity automatically. The vacuous one gave a false sense of verification for 300+
findings; the real one was simply never written down.

$$\boxed{\;\texttt{bcc\_curl\_symbol}\text{ fails }\text{curl}(\text{grad}\,\varphi)=0\text{ maximally: mean }|\mathbf C\times\mathbf G|/(|\mathbf C||\mathbf G|)=0.7417\text{ (spectral gradient), }0.7072\text{ (forward-difference) — not the }0\text{ a genuine curl generator gives identically; the previously-existing gate leg (}\text{div}(\text{curl})=0\text{) is vacuous, true for any vector field; gated as a known, monitored, UNREPAIRED defect, not fixed}\;}\tag{R10.7}$$

(F393, 7/7 legs PASS — all 7 report the *measured defective value*, not a target — one control verified red
on exactly 5 of 7 legs; reviewed CONFIRMED, one real (tooling-only) bug found and fixed in a CLI parameter
coercion, not the physics; test record `F393-curl-grad-identity-diagnostic`, gate tier, `expect.exactness:
quantitative`.) No claim card — D12 scope, a test-infrastructure addition.

### 10.3.8 F394 — the DEC curl complex is deferred, explicitly, not attempted

Whether to build a genuine discrete-exterior-calculus curl on the 3D BCC lattice — as a new object
alongside, not replacing, `bcc_curl_symbol` — was explicitly named as this session's own decision point, and
the rerun prompt's own text pre-authorized stopping here: *"If the BCC DEC complex turns out to be more than
this session can carry, stop after Part B and say so."* **The decision: not attempted this session**, for
three converging reasons stated in full: (1) the construction is genuinely novel, not a mechanical
extension — the BCC lattice's 8 fractional-shift hop directions are not axis-aligned integer bonds, so
defining "the plaquette" requires an independent choice of which loops of fractional-shift bonds bound a
2-cell, with a proof that $d_1\circ d_0=0$/$d_2\circ d_1=0$ hold for the *specific* complex chosen — a
genuine open research question, not a lookup; (2) downstream verification (gating both identities to machine
precision, then measuring the blast radius against every existing consumer before switching anything) is a
multi-step program in its own right, competing for the same session's budget against Part D's re-run, which
is "the point of the exercise"; (3) nothing in Part D actually requires Part C to have landed — verified
true, not merely assumed, by the same session's own F395.

**This is not a claim the DEC route is wrong or unlikely to work** — an inventory of what already exists to
build on is recorded (F385's Peierls phases, the Wilson plaquette action, `build_pair_mode`'s already-correct
$\mathbf E\perp\mathbf B$ construction, the verified-sound momentum observer), and a concrete four-step order
of operations is recorded for whoever picks this up: settle the Weyl-vs-Dirac question first (Nielsen–
Ninomiya bites the Weyl-only scope this whole chapter's chain declares), define the BCC 2-cell geometry,
gate $d\circ d=0$ to machine precision on the new complex before doing anything else with it, and only then
measure the blast radius.

$$\boxed{\;\text{the 3D BCC discrete-exterior-calculus curl complex is explicitly DEFERRED, not attempted — a reasoned scoping decision with a four-step order-of-operations left for a future session, not a physics result}\;}\tag{R10.8}$$

(F394, no test record — analysis-only, no module written, nothing to test; reviewed CONFIRMED, including
the riskiest claim — "nothing in Part D depends on Part C" — independently verified true by F395's own
re-run.) No claim card — no assertion against established physics is made or withdrawn.

### 10.3.9 F395 — Stage 5 re-run against the fixed beam: the anomaly survives a third independent fix, the off-axis picture genuinely changes, and claim 1 is retired

Every one of Stages 0–4 was re-run directly (not assumed unaffected) after this session's changes and found
bit-identical or unchanged: F384 (4/4 PASS, identical numbers), F385 (10/10 PASS, identical), F386/F387
(7/7 and 12/12 PASS, identical — the curl defect F393 gates is unrepaired and still present in every
$\mathbf A$ this scenario's fermion reads), F388 (7/7 PASS — F388 never used the defective
`build_beam_packet` in the first place, so there was nothing to re-run for it specifically), F389 (3/3 and
4/4 PASS, identical — self-sourced-only, no seeded beam).

**The $m_\text{index}=4$ anomaly, re-measured under F392's circular-polarization fix: persists.**
$\cos(\Delta P_\text{matter},\hat{\mathbf k}_\text{beam})=-0.949$ (was $-0.988$ under the original linear
beam) — the sign reversal survives a *third* independent beam-construction fix (circular vs. linear
polarization, orthogonal to F391's own $\hat{\mathbf C}(\mathbf k)$-transversality fix). This is consistent
with, and independently re-confirms from a third angle, F391's own conclusion: the mechanism is on the
**matter side** (the fermion's fixed internal spin state), not the photon sector — and it is still not
derived.

**The off-axis breakdown, re-measured: genuinely changes, for the first time.** F390 (linear,
$\hat{\mathbf k}$-transverse) and F391 (linear, $\hat{\mathbf C}(\mathbf k)$-transverse) both measured
near-total decorrelation off-axis, $\cos\approx-0.002$ in both cases — two independent beam-construction
fixes left this number essentially unchanged. **The genuinely circular (null-field) beam does not reproduce
that**: at a 20-tick snapshot, axis=1 moves to $\cos\approx+0.328$ (matter direction) with
$\cos(\Delta P_\text{matter},\Delta P_\text{field})=+0.248$; axis=2 moves to $\cos\approx-0.101$ with
$\cos(\Delta P_\text{matter},\Delta P_\text{field})=-0.819$. **Two things are true at once:** polarization
convention (linear vs. circular), not only transversality convention, is genuinely part of the off-axis
picture — a new, unpredicted result; and the change does not restore a clean "direction tracks the beam"
rule (axis=1 gives a modest positive correlation, axis=2 a small negative one, neither near the on-axis
$+0.99$).

**Correction, found by the independent review, and reported here precisely rather than smoothed over: the
specific off-axis point values above are not converged in tick count.** A tick-count sweep
($10,20,30,40$, otherwise default) gives, for axis=1: $+0.260$ (tick 10) → $+0.324$ (tick 20, the finding's
own default, slightly differing from the $+0.328$ first quoted due to a snapshot re-measurement) →
$+0.225$ (tick 30) → $+0.160$ (tick 40) — drifting non-monotonically **down below the gate leg's own
$>0.2$ reproducibility threshold by tick 40.** For axis=2: $-0.184$ (tick 10) → $-0.096$ (tick 20) →
$-0.085$ (tick 30) → $+0.102$ (tick 40) — **changing sign between tick 30 and tick 40.** Neither series
shows any sign of settling within the window tested. **The qualitative claim survives** — at every tick
count tested, both axes measure a nonzero, non-$\approx0$ correlation, genuinely different from F390/F391's
own near-machine-zero numbers at every tick count they reported, so "circular polarization changes the
off-axis result relative to either linear-type fix" remains true. **The specific numbers do not** — they are
one snapshot of a still-evolving quantity, and this finding and `docs/claims/CL307` were both corrected to
stop citing them as settled.

**Claim 1, restated per the audit's crystal-momentum argument — withdrawn as originally stated, replaced
with three measured targets:**

- **(A) exact charge conservation — not delivered.** The fermion's own norm drifts $0.54\%$ over the
  scenario's 20 ticks under the actual per-link step (F385 fork a) — bounded, but genuinely nonzero. The
  audit's "delivered outright" language described its own separate single-action *prototype* (a genuine
  lattice Ward identity from $\partial H/\partial A$), which casim's actual bridged construction does not
  implement — not anything running in this repository today.
- **(B) exact crystal-momentum translation covariance, $\Phi\circ T=T\circ\Phi$ — delivered.** Measured to
  $1.5\times10^{-15}$ (relative), because none of the per-tick update rules reference an absolute lattice
  coordinate; each is built from convolutions/shifts that commute with translation by construction. Genuinely
  delivered, gated for the first time here — the one unambiguously positive result in this chapter's whole
  investigation.
- **(C) matched-order approach to the continuum — still mismatched, for a sharper reason.** Doubling
  $g_\text{lat}$: $\|\Delta P_\text{matter}\|$ scales by $\times0.994$ (essentially flat) while
  $\|\Delta P_\text{field}\|$ scales by $\times2.036$ (roughly linear, not F389's own quadratic in the
  self-sourced case). The flat matter-push ratio is **not** evidence of a matched order — it is F390's own
  already-disclosed fact that the matter push in a beam-driven scenario is dominated by the
  coupling-*independent* unconditional per-link push, so its flat doubling ratio reflects a term with no
  coupling dependence at all, not agreement with the field channel's genuinely $g_\text{lat}$-driven order.

$$\boxed{\;\text{the }m_\text{index}=4\text{ anomaly PERSISTS under a third independent beam fix (}\cos=-0.949\text{), reinforcing the matter-side (spin-state) candidate; the off-axis picture GENUINELY CHANGES under circular polarization (}\cos\approx+0.33,-0.10\text{ at 20 ticks) but is NOT CONVERGED in tick count (axis=1 falls to }0.160\text{ by tick 40, below its own gate threshold; axis=2 changes sign tick 30}\to40\text{); claim 1 WITHDRAWN, restated as (A) charge conservation not delivered, (B) crystal-momentum covariance delivered exactly (}1.5\times10^{-15}\text{), (C) matched-order still mismatched, for a sharper reason than F389's}\;}\tag{R10.9}$$

(F395, 6/6 legs PASS, one control verified red on exactly 1 of 6 legs; reviewed CONFIRMED-NARROWER — the
off-axis non-convergence is the review's one substantive finding, both the reviewer and this session's own
re-derivation confirming it independently; test record `F395-stage5-circular-beam-rerun`, gate tier,
`expect.exactness: quantitative`.) Updates `docs/claims/CL307` directly; no new card issued.

## 10.4 Results table

| # | Statement | Status | Exactness / residual | Source |
|---|---|---|---|---|
| R10.1 | $\hat{\mathbf C}(\mathbf k)$ direction anisotropic off-axis (exact, $L$-stable); $\Omega_\text{pair}/\lvert C_\text{odd}\rvert$ mismatch real but ruled out as the no-monopole defect's cause; sector-split fix | confirmed, mechanism corrected in review | exact (direction facts) / machine $2.76\times10^{-16}$ (fix) | F387; no claim card |
| R10.2 | Coupled channels wired correctly; current's transverse fraction $2$–$2.4\times10^{-16}$ on every config — structurally zero; total momentum not conserved by construction | **negative — cannot radiate** | machine (transverse-fraction, wiring legs) / quantitative (momentum, 20–100 tick run) | F388; no claim card |
| R10.3 | Physically motivated transverse current lets the loop radiate ($11\%$ recovery at $g{=}0.3$); $O(g)$ vs. $O(g^2)$ scaling — exact conservation unreachable at any coupling | **partial fix — order mismatch structural, not fixable by tuning** | exact (continuity-blindness identity) / quantitative (scaling, doubling ratios $1.99$–$2.00$ vs. $3.99$–$4.01$) | F389; no claim card |
| R10.4 | Push direction confirmed on-axis, $m_\text{index}\le3$ ($\cos=0.995$); REVERSES at $m_\text{index}=4$ ($\cos=-0.988$); decorrelates off-axis; anti-alignment ($\cos=-0.989$) INVERTS off-axis ($\cos=+0.99995$); $\Delta p=\Delta E/c$ NOT GATED | **confirmed on-axis only / not gated / inverts off-axis** | quantitative (all legs; 8/8 gate legs incl. 2 added to monitor the breakdown) | F390; CL307 (`narrowed`, `low`) |
| R10.5 | Named beam-transversality mechanism RULED OUT (fix changes nothing to 3–4 s.f.); $\hat{\mathbf C}(\mathbf k)$ exactly anti-parallel to $\hat k$ on y-axis (new exact fact, $180°$); spin-state candidate found ($\cos=0.517$), NOT DERIVED | **mechanism ruled out; candidate open** | exact (new $\hat{\mathbf C}$ facts) / quantitative (candidate-mechanism legs) | F391; updates CL307, no new card |
| R10.6 | Original beam had $\mathbf E\parallel\mathbf B$ pointwise — zero field momentum by construction, independent of R10.5; fixed with a null Riemann–Silberstein construction | **defect found and fixed** | machine ($\le2.4\times10^{-17}$ null legs; $3.6\times10^{-15}$ drift) | F392; no claim card |
| R10.7 | `bcc_curl_symbol` fails $\text{curl}(\text{grad})=0$ maximally (mean ratio $0.74$/$0.71$, not $0$); gated, NOT REPAIRED | **known, monitored, unrepaired defect** | quantitative (defect-monitoring legs, by design) | F393; no claim card |
| R10.8 | 3D BCC discrete-exterior-calculus curl complex: DEFERRED, not attempted, reasoned order-of-operations recorded | **explicit deferral, not a result** | — (no test record; analysis-only) | F394; no claim card |
| R10.9 | $m_\text{index}=4$ anomaly PERSISTS under a third independent beam fix; off-axis picture genuinely changes but NOT CONVERGED in tick count (axis=1 falls below its own threshold by tick 40; axis=2 changes sign); claim 1 restated as (A) not delivered, (B) delivered exactly, (C) still mismatched | **anomaly confirmed persistent; convergence failure disclosed; claim 1 retired** | machine (B, $1.5\times10^{-15}$) / quantitative (A, C, off-axis — explicitly non-converged) | F395; updates CL307, no new card |

## 10.5 Comparison with measurement

**No direct comparison against a measured electromagnetic-recoil observable is made or attempted anywhere
in this chapter, and none could be honestly made given §10.3's own findings.** Every number reported above
is a measurement of the model's own internal, lattice-scale coupled-channel dynamics against itself —
momentum observed on the model's own `core.observers.Momentum`, correlations between the model's own
computed vectors, drift measured against the model's own norm — not against any experimental photon-recoil
or Compton-scattering data point. This is not a scoping choice this chapter makes; it is a direct
consequence of Claim 4 (Thomson cross-section) being explicitly deferred at F390 and remaining deferred
through F391–F395: the one calculation that would connect this chapter's machinery to an actual measured
cross-section is, as of the latest finding in this chain, not attempted, for reasons (no genuine far-field
on a periodic/spectral lattice, no closing energy/momentum budget, and — per F391 — dependence on an
uncontrolled internal spin-state choice) that are themselves substantive open results of this
investigation, not merely a missing step. A reader wanting this model's electromagnetism connected to a
measured number should read Chapter 23 (QED precision), which runs the model's *perturbative* QED machinery
at the measured value of $\alpha_\text{em}$ — a completely different, already-settled calculational route
that does not depend on anything in this chapter closing.

## 10.6 What was excluded, and why

**The named beam-polarization/$\hat{\mathbf C}(\mathbf k)$-transversality mismatch as the direction/
anti-alignment breakdown mechanism.** Named as "likely" by F390 and its own review (the beam-construction
helper's Euclidean-$\hat{\mathbf k}$ polarization convention mismatched against $\hat{\mathbf C}(\mathbf
k)$'s own axis-asymmetric direction). **Tested directly and ruled out by F391** (§10.3.5): a beam built to
be genuinely $\hat{\mathbf C}(\mathbf k)$-transverse (near-zero longitudinal leak, vs. the original's
$27.5\%$) reproduces the identical breakdown pattern to 3–4 significant figures. The underlying fact this
mechanism cited — $\hat{\mathbf C}(\mathbf k)$'s real, axis-asymmetric anisotropy — remains true and is even
sharpened (the new exact y-axis anti-parallel fact), but it is not causal for the breakdown this chapter's
investigation is chasing. This is the chapter's clearest example of a well-motivated, precisely-tested
candidate mechanism being cleanly and quantitatively excluded, not merely left unconfirmed — genuine
progress, reported as such.

**The roadmap's own literal `E += g·J` sourcing sketch, applied without any sector split.** Excluded by
F387 (§10.3.1): it violates the model's own no-monopole invariant, measured $\|i\hat{\mathbf C}\cdot
\mathbf B\|=2.41$ by tick 6, a genuine defect, not a numerical artifact. The transverse/longitudinal sector
split is adopted instead.

**Treating $\Delta p=\Delta E/c$ as a threshold-gated test.** Considered and explicitly declined by F390
(§10.3.4): forcing a numerical tolerance onto a ratio that spans $29.8$ to $1.3$ across the tested range,
with no shared coupling constant between the two quantities compared and no principled value to compare the
ratio to, "would manufacture a false impression of a test that was actually run." Reported instead as a
precisely characterized negative/inapplicable result.

**Attempting the 3D BCC discrete-exterior-calculus curl complex this session.** Considered as Part C of the
rerun program and explicitly deferred by F394 (§10.3.8), per that program's own pre-authorization to stop
after Part B. Not excluded as wrong or unlikely to succeed — excluded from this session's scope specifically,
with a concrete reasoned order-of-operations left for whoever attempts it.

**Repairing `bcc_curl_symbol` itself, once its $\text{curl}(\text{grad})=0$ failure was found.** F393
(§10.3.7) explicitly declines to repair the symbol — "deciding whether/how to repair it (Part C)... is
decided separately" — choosing instead to gate the defect as a permanently monitored, known quantity. Every
consumer of the symbol (F384/F386/F387/F388/F389/F390/F391) is left unmodified, bit-for-bit.

## 10.7 What is still open

This section is unusually long by this monograph's own standards, and functions partly as a to-do list —
consistent with the build instructions' framing of this chapter as a live research report.

**The leading candidate, stated first because it is the single most promising unresolved lead.** F391
(§10.3.5) found that the recoil direction depends substantially on the fermion's own fixed internal spin
state ($\cos=0.517$ between two spin choices at one fixed beam configuration) — a genuine, load-bearing
dependence on a degree of freedom `FermionEmChannel.init_state` sets once, unconditionally, and never
varies. F395 (§10.3.9) independently reinforces this from a third angle: the $m_\text{index}=4$ sign flip
survives a third, orthogonal beam-construction fix (circular polarization), ruling the photon sector out yet
again and leaving the matter-side spin dependence as the only candidate not yet tested and ruled out. **No
closed-form relationship between the fermion's spin state, the beam's axis/polarization, and the resulting
push direction has been derived.** A future session's most direct next step, per F391's own caveats: either
derive the closed-form relationship directly from `minimal_coupling.u1_link_weyl_step_3d_bcc`'s
hop-direction-dependent spinor rotations ($M_\mathbf{d}$, the object F391 names as implicated), or run a
systematic scan over spin states crossed with beam configurations broader than F391's own six-point
$(\text{axis},\text{pol\_axis})$ grid and two-point spin-state test.

**The off-axis result under circular polarization is not converged, and no future citation of F395's own
point numbers should treat them as settled** (§10.3.9). Both the reviewer and F395's own corrected text are
explicit: axis=1's correlation falls below its own gate leg's reproducibility threshold by tick 40; axis=2's
correlation changes sign between ticks 30 and 40. Whether either series settles to a steady value, oscillates
indefinitely, or genuinely diverges is not established by anything in this chain — a future session wanting
a defensible off-axis number needs a longer, converged run, not a 20-tick snapshot.

**The two channels are not derived from one covariant lattice action, and nothing in this chapter's chain
attempts that unification.** F389 (§10.3.3) states the honest reason exact momentum conservation is
unreachable at any coupling: F385's per-link recoil and F389's current construction are independently
derived and independently audited, bridged in `core.coupled`, not two halves of one gauge-invariant action
whose Noether identity would force order-by-order agreement. Deriving both channels from one action —
"a strictly bigger undertaking than either fix individually" per F389's own text — is not attempted anywhere
in F387–F395, and is the structural prerequisite for claim 1 (momentum conservation) ever being achievable
in the form the roadmap originally envisioned, rather than the three-part replacement F395 lands on.

**Claim 4 (Thomson cross-section) stays out of reach, now blocked by a compounding set of obstacles, not a
single fixable one.** F390 named three: no genuine far-field on this periodic/spectral lattice, norm loss
on the projected beam, no closing energy/momentum budget. F391 removed the norm-loss obstacle as stated but
disclosed a fourth, more fundamental one in its place: the recoil this cross-section would normalize
against depends on the uncontrolled spin-state choice §10.7's leading candidate names. F390's far-field and
energy-budget gaps are unchanged by anything in F391–F395.

**The `bcc_curl_symbol` $\text{curl}(\text{grad})=0$ defect is gated, not fixed, and every $\mathbf A$ this
chapter's entire chain reads is built on it.** F393/F394 (§10.3.7–10.3.8) leave the symbol itself
unrepaired; F394's four-step order of operations (settle Weyl-vs-Dirac first, define the BCC 2-cell
geometry, gate $d\circ d=0$ to machine precision on the new complex, then measure the blast radius) is a
genuine, unstarted research program, not a routine follow-up.

**The exchange-bus registration-order blind spot, inherited from Chapter 9's own boundary and confirmed
still present.** F388/F389's own caveats (cited in §10.3.2–10.3.3, not re-derived here) found that
`core.graph.build_graph`'s dependency-edge mechanism structurally cannot flag a wrong registration order for
a true two-node mutual-dependency cycle — the `em_photon`/`fermion_em` pair's own documented pre-tick/
post-tick contract is a convention this bus design does not, and cannot, verify on its own. A partial fix
(recognizing the relevant config keys in `Channel.consumes()`) was applied in review but does not close the
actual gap; a genuine fix needs an explicit declared-order assertion on the coupled-channel classes
themselves, not attempted anywhere in this chain.

**The 300-tick field-energy growth observed in F389's own extended run is disclosed but not characterized.**
Field energy keeps growing without an obvious saturation over that window at $g_\text{lat}=0.5$ (fermion norm
drift stays small and bounded throughout), and whether it eventually saturates, oscillates, or is a genuine
runaway at stronger coupling or longer runtimes is not established by anything in F389–F395.

**Chapter 9's own two flagged seams (§9.7), both now directly confirmed as hit, not merely anticipated.**
The curl-carrying-vs-curl-free scope limit of F385's per-link step (R9.7) is exactly the boundary every
scenario in this chapter's chain operates at — every field used is genuinely curl-carrying, and the
$O(|qA|\cdot a)$ unitarity/momentum-transfer tension it names is the mechanism behind F385's own accepted
norm drift (measured $0.54\%$ over 20 ticks in F395's target (A)). The $\Omega_\text{pair}(\mathbf k)$-vs-
$|C_\text{odd}(\mathbf k)|$ propagator mismatch Chapter 9's review traced is exactly what F387 (§10.3.1)
investigated first and found real but non-causal for the specific defect it was chasing — a precise,
measured answer to a question Chapter 9 could only flag as likely relevant.

## 10.8 Falsifiers

**`docs/claims/CL307-photon-fermion-push-partial-recoil-not-conservation.md`** (status `narrowed`,
confidence `low`, issued by F390, updated in place by F391 and F395, no new card superseding it) is this
chapter's one claim card, cited precisely rather than paraphrased into something stronger.

**CL307's falsifier was already triggered once, in the direction the card now reflects — an unusual and
important detail, represented here precisely.** The card's first version (issued the same day as F390)
claimed the direction and anti-alignment results held broadly, with a stated falsifier of "a wider parameter
sweep finding the anti-alignment breaks down badly." **The independent review of F390 ran exactly that
sweep, in the same review cycle that produced the card, and found not just a breakdown but a sign
inversion** — the card was narrowed to its current, domain-restricted form in the same pass, rather than
left standing on a premise its own review had already falsified. This is not a falsifier waiting to be
tested by a future session; it is a falsifier this project's own review process triggered against itself,
within hours of the claim being issued, and the response (narrowing the card immediately, in the same pass)
is the correct one per this project's own standing rule that a finding's review-driven fixes are applied
before the record is treated as settled.

**One proposed route back toward `live` has since been tried and closed.** CL307 originally named "a
derivation identifying and correcting the specific mechanism (the beam-polarization/$\hat{\mathbf C}(\mathbf
k)$-anisotropy mismatch...) that recovers the broad, axis-independent form" as the way to strengthen the
card. F391 (§10.3.5) built and tested exactly that fix and found it changes nothing — the mismatch was real
but not causal.

**The card's current, forward-looking falsifier, stated in its own words:** finding that the direction/
anti-alignment results *also* fail within the stated domain (on-axis, $m_\text{index}\le3$, at other
lattice sizes $L$) would remove even the narrow positive claim; conversely, a derivation of the spin-
dependence candidate (§10.7's leading open lead) that both explains the on-axis success and recovers a
broader domain would strengthen the card back toward `live`. **No such derivation exists yet, as of any
finding read for this chapter.**

**F384–F389, F392–F394 carry no claim cards and therefore no stated falsifiers of their own**, by design,
per D12's bar (engine-capability additions and a test-infrastructure/scoping decision, not assertions
against established physics). Their own internal falsifiers are the declared negative controls each
finding's own test record carries — each independently verified, measured, to turn exactly its declared
legs red and no others, the same `can-fail` protocol Chapters 8–9 already established as the substitute
where no claim card is issued.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–9's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\mathbf J_\text{full}=\mathbf J_\text{exact}^L+\mathbf J_\text{naive}^T$ | The physically motivated current sourcing the radiative sector: F384's exact longitudinal solution plus the naive Weyl Noether bilinear's $\hat{\mathbf C}(\mathbf k)$-transverse projection — the specific transverse field is a disclosed constitutive choice, not a derivation; only its continuity-safety is forced. | §10.3.3 |
| $g_\text{lat}$ | The field-sourcing coupling constant governing how strongly the fermion's current sources $\mathbf E$; shown (F390) to control only the field-sourcing half of the loop, not the matter push, which is set almost entirely by $q$ and the beam amplitude independent of $g_\text{lat}$. | §10.3.4 |
| $R=\text{diag}(1,-1,1)$ | The exact reflection relating $\hat{\mathbf C}(\mathbf k)$'s small-$k$ limiting direction to $\hat{\mathbf k}$: $\hat{\mathbf C}(\mathbf k)\to R\hat{\mathbf k}$, giving the y-axis's exact $180°$ anti-alignment as $R\hat y=-\hat y$. | §10.3.5 (sharpening §10.3.1) |

---

*No new gap logged this chapter. The nine findings read here are already maximally disclosed about their
own failures, by design and by their own mandatory review process — every negative, partial, or
non-converged result reported above is one the source findings themselves name explicitly, not one this
chapter's authoring uncovered independently. The one place a documentation gap might plausibly have been
found — whether `docs/claims/CL307`'s "falsifier already triggered" framing overstates or understates what
happened — was checked directly against the card's own "Status & history" section and F390's review, and
found to match precisely (§10.8): the card itself states the falsifier was triggered by its own review
cycle, and this chapter's account matches that statement rather than adding to or softening it. No finding,
claim card, module, or test record was created or modified in the writing of this chapter.*
