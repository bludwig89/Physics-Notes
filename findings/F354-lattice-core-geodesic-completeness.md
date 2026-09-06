# F354 — The lattice-regulated black-hole core is geodesically complete, and the curvature bound alone forces it: the Kretschmann scalar is a sum of squares, so $K\le a^{-4}$ makes the centre a $C^{1,1}$ manifold interior point — while the attractive "$-1\in O_h$ forces the parity" route is a **no-go**, false in both directions

**Date:** 2026-09-03 - 14:20
**Numbering:** `casim index` printed **NEXT FREE NUMBER F354** (max was F353, 0 duplicates, 19 declared gaps); taken in the same edit that created this file.
**Status:** Confirmed — 7/7 counted checks PASS (plus one uncounted structural declaration). The sum-of-squares theorem (B1), the no-go (B2), the polynomial parity statement (B3), the geodesic regimes (B4) and the screen calibration (B5) are **exact-algebraic**; the scales (B6) are **exact-algebraic but contingent** on three named inputs, each quantified in §7; the SI numbers (B7) are **computed**.
**Reviewed:** 2026-09-03 — **REFUTED-then-rebuilt** ([review](../docs/reviews/F354-review-2026-09-03.md)). The first draft of this finding claimed the $O_h$ parity theorem as its mechanism. The session's own attack pass killed it with an explicit counterexample; this file is the rebuild, and §5 records the dead route deliberately rather than deleting it.
**Module:** `src/casim/engine/interactions/gravity_core_completeness.py`
**Test record:** `F354-core-geodesic-completeness` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, 7/7 PASS in ~7 s; two declared controls, both perturbing computed quantities, both verified to redden exactly one named leg)
**Results:** `test-results/F354_core_geodesic_completeness.json`
**Claim:** `docs/claims/CL295-bounded-curvature-forces-a-regular-core-centre.md` (CL295, supporting, `contingent`)
**Cross-references:** [[F183-blackhole-under-full-tensor]] (§L1 — the saturation estimate this builds on; **not** re-attacked, and see §7 for the one place its proxy is superseded), [[F284-rigid-lattice-expansion-and-primordial-state]] (§5 — closed; but §8 raises a **ceiling-convention conflict** with F183 that this finding cannot settle), [[F178-gravity-full-tensor-adoption]] / [[F181-covariant-interior-kernel-battery]] (the **two-function** interior, which B1 respects and the first draft did not), [[F106-psi-K-sourcing-derivation]] (how $\psi$ sources the metric — the density whose smoothness is the real hypothesis), [[F107-canonical-a-adoption-L4-grb-gate]] (the canonical cell $a$; and see §8 for a tick-duration conflict with F284). External: Zhou & Modesto, PRD **107** 044016 (2023), arXiv:2208.02557; **Antonelli & Sebastianutti, arXiv:2509.15477, PRD 10.1103/hf4r-19xh** (prior art for the regularity criterion — stronger, and an *iff*); Grant, Kunzinger & Sämann, arXiv:1804.10423; Chruściel & Grant (geodesics at $C^{1,1}$); Whitney, Duke Math. J. **10** (1943) 159; Bonanno & Reuter, PRD **62** 043008 (2000); Ashtekar, Olmedo & Singh, PRL **121** 241301 (2018); Eichhorn, Gamito & Stokes, arXiv:2605.06813.

---

## 1. The residual, and why it is not rhetorical

F183 §L1 showed curvature **saturates** at the cell scale rather than diverging. That is a statement about an invariant, not about worldlines:

> **Bounded curvature does not imply geodesic completeness.** Zhou & Modesto (2023) exhibit regular black holes with everywhere-bounded curvature that are geodesically **incomplete** — the analytically extended Hayward metric among them.

So E10 was genuinely open. It is now closed, but by a different and more robust argument than this finding first proposed.

## 2. What "geodesic completeness" means on a discrete substrate

The continuum notion has no literal discrete counterpart — there is no affine parameter, and as Eichhorn et al. put it for causal sets, "in a discrete setting, there are no smooth geodesics." We adopt Grant–Kunzinger–Sämann property **(TC)**: *every inextendible timelike geodesic has infinite length*, length being the time-separation function — on the automaton, the maximal causal chain length in ticks. (TC) needs no differentiable structure, which is why it survives the transition to a lattice.

This gives two tiers.

## 3. Tier A — the substrate is tick-complete (necessary, not sufficient)

Three structural premises: the BCC update rule is **total** (defined at every cell for every neighbourhood), the lattice is **boundaryless** (infinite, rigid, eternal — F283/F284), and the update is **norm-preserving**. Every causal chain therefore admits a successor at every tick, so chain length is unbounded.

**This is a declaration, not a computation, and it is deliberately excluded from the pass count.** (The first draft counted it, inflating a six-leg battery to "7/7".) It does not forbid the *emergent* affine parameter saturating while ticks run on — which is exactly the failure mode a naive "the automaton just keeps ticking" argument misses. Tier B rules that out.

## 4. Tier B — the result: the Kretschmann scalar is a sum of squares

Take the **general two-function** static spherically symmetric metric — the class F178/F181 say the interior actually requires, since the impedance-locked single scalar forces anisotropic stress:

$$ds^2=-A(r)\,dt^2+\frac{dr^2}{B(r)}+r^2d\Omega^2 .$$

Computing the Riemann tensor in an orthonormal frame gives an exact identity (check B1, verified against the full contraction):

$$K \;=\; 4R_{\hat t\hat r\hat t\hat r}^2+8R_{\hat t\hat\theta\hat t\hat\theta}^2+8R_{\hat r\hat\theta\hat r\hat\theta}^2+4R_{\hat\theta\hat\phi\hat\theta\hat\phi}^2$$

$$R_{\hat\theta\hat\phi\hat\theta\hat\phi}=\frac{1-B}{r^2},\qquad R_{\hat r\hat\theta\hat r\hat\theta}=-\frac{B'}{2r},\qquad R_{\hat t\hat\theta\hat t\hat\theta}=\frac{BA'}{2rA}.$$

**$K$ is a sum of squares, so a global bound $K\le a^{-4}$ bounds every term separately.** Reading them off:

| bounded term | forces |
|---|---|
| $\lvert 1-B\rvert/r^2$ | $B(0)=1$ — **no mass defect, no solid-angle deficit** |
| $\lvert B'\rvert/2r$ | $B'(0)=0$ |
| $B\lvert A'\rvert/2rA$ | $A(0)$ finite and nonzero, $A'(0)=0$ |

So $g_{\mu\nu}=\eta_{\mu\nu}+O(r^2)$ in Cartesian coordinates with bounded derivatives: **$C^{1,1}$, Lorentzian, no defect — the centre is an interior point of the manifold, not a boundary.** At $C^{1,1}$ geodesics exist and are unique (Chruściel–Grant), so the extension through the centre is unique and there is nothing to choose.

**This uses only the curvature bound.** No parity, no point group, no saturation, no $AB=1$. That is what makes it the E10 result.

In the one-function case it collapses to the identity the module uses for speed, $K=(f'')^2+4(f'/r)^2+4((1-f)/r^2)^2$ — validated against Schwarzschild ($48M^2/r^6$) and de Sitter ($24/L^4$).

**The control has teeth.** Give the metric a genuine solid-angle deficit $B(0)=1-\delta$ (a global monopole — the classic bounded-*some*-invariants-but-incomplete case). The $(1-B)/r^2$ term then makes $K\sim4\delta^2/r^4$, unbounded. Measured: $Kr^4\to0.0400$ at $\delta=0.1$, i.e. exactly $4\delta^2$, the decomposition's own prediction. Excluding defects is precisely what the bound has to do.

## 5. The no-go: $-1\in O_h$ does **not** force the parity condition

The first draft of this finding claimed something more attractive: that because the BCC site group contains inversion, every $O_h$-invariant has even degree, so the density is even, $m$ is odd, $f$ is even, and the parity condition Hayward-class metrics must be handed by fiat is *forced by the substrate*. **That claim is false in both directions.** It is recorded here rather than deleted, because a closed elegant route is a result.

**(i) Not sufficient.** Hayward's own density is

$$\rho_{\rm Hay}(r)=\frac{3ML^3}{4\pi(L^3+r^3)^2}=\frac{3M}{4\pi L^3}-\frac{3M}{2\pi L^6}r^3+O(r^6).$$

It is a function of $r$ alone — hence invariant under all of $O(3)$, hence under $O_h$, hence under $-1$ — yet it carries an **odd $r^3$ term**, $m(-r)+m(r)=2Mr^6/(r^6-L^6)\ne0$, $f$ is not even, and Zhou–Modesto show the spacetime is incomplete. The reason: $r^{2k+1}=(x^2+y^2+z^2)^{(2k+1)/2}$ is an $O_h$ invariant that is odd in $r$ and **not a polynomial**. The Reynolds projection (B3) proves the parity statement for *polynomials* only, and that word is the whole loophole.

**(ii) Not necessary.** The $T_d$ invariant ring is $\mathbb{R}[r^2,\,xyz,\,x^4{+}y^4{+}z^4]$, so every odd-degree $T_d$ invariant carries the factor $xyz$ — whose spherical average vanishes identically (verified for $xyz$, $xyz\,r^2$, $xyz(x^4{+}y^4{+}z^4)$). The Misner–Sharp $m(r)$ is therefore unchanged, and a **non-centrosymmetric** (diamond/zincblende) lattice gives the *same* regular centre in the monopole channel.

> **The load-bearing hypothesis is smoothness (analyticity) of the coarse-grained core density at the centre in Cartesian coordinates** — which is exactly what is unavailable over a $\sim2.2$-cell core. Once granted, Whitney gives evenness from spherical symmetry alone and $O_h$ is redundant in the isotropic channel.

**What $O_h$ does still buy**, at its true and much smaller strength: for a density already known to be smooth in $x$, $O_h$-invariance kills every odd-degree Cartesian term — which sphericity is not available to do when the density is anisotropic, as a lattice density is. That is downstream of the smoothness hypothesis, not a replacement for it.

## 6. Geodesics (check B4)

For a regular centre $f=1-r^2/L^2+O(r^4)$:

| regime | behaviour | complete? |
|---|---|---|
| $E<1$ | turning point at $f=E^2$, strictly outside the centre; bounded oscillation | ✔ trivially |
| **$E>1$** | $(\dot r)^2\to E^2-1>0$ with zero slope: **crosses transversally and continues** | ✔ — *needs B1* |
| **null radial** | $dr/d\lambda=\pm E$: reaches and **crosses** at finite affine parameter | ✔ — *needs B1* |
| $E=1$ | $r(\tau)=r_0e^{\tau/L}$: approaches asymptotically, never arrives | ✔, but see below |
| non-radial | $L_z^2/r^2$ barrier diverges ($f(0)=1>0$): never reaches the centre | ✔ trivially |

**Completeness rests on the $E>1$ and null rows**, which reach $r=0$ and must pass through — which is exactly what B1's $C^{1,1}$ interior point licenses. The first draft leaned on the $E=1$ row as though it were the strong case; it is not. Its "infinite proper time, never arrives" reading is physically hollow: the infaller is inside the *central cell* after $\tau=L\ln(L/a)\approx3.0$ ticks, beyond which the exponential law is extrapolation into a domain the model itself says it does not resolve.

**Scope.** This is a **local $r\to0$ analysis**, not a completeness proof for the **maximal extension** — which is what Zhou–Modesto actually construct, and which for a two-horizon core requires the full conformal diagram. That gap is real and is listed in §10.

## 7. The scales, and the three inputs they are contingent on (check B6)

| scale | value | status |
|---|---|---|
| $L$ (de Sitter radius at the centre, $=$ inner horizon to 6 figures) | $24^{1/4}a=2.21336\,a$ | exact; **profile-independent** — it depends only on $\rho(0)$ |
| $L$ in ticks (the $E=1$ e-folding) | $6^{3/4}=3.83366$ | exact |
| core radius | $96^{1/6}M^{1/3}a^{2/3}$ | **Bardeen-specific** |
| ratio to F183 §L1's proxy | $2^{1/6}=1.12246$ | **Bardeen-specific** |
| $M_{\rm ext}$ (horizon disappears) | $\tfrac{3\sqrt3}{4}L\approx19\,m_{\rm Pl}$ | new; see §9 |

Three inputs are consumed that the first draft did not declare. Each is quantified rather than hidden:

1. **Saturation as an equality.** F183 licenses "the lattice *bounds* curvature at $1/a^4$". *Bounded* is not *saturated*. Without $K(0)=a^{-4}$ every scale is a one-sided bound: $L\ge24^{1/4}a$, e-folding $\ge6^{3/4}$ ticks, and so on. Nothing in F178/F183/F284 forces the collapse endpoint to sit *at* the bound; deriving it needs a dynamical CA calculation, not algebra.
2. **The ceiling convention** — see §8.
3. **The profile.** $L$ is profile-independent, but the mass-to-core-radius relation is not. Swapping Bardeen for an even Gaussian moves the ratio against F183's proxy from $2^{1/6}=1.1225$ to $0.7218$ (measured; this is control 2). **So "F183's estimate is sharpened by exactly $2^{1/6}$" is a Bardeen statement, not a model statement.** The first draft asserted it as though it were exact.

The **quarter-power-of-3 ladder** tie to F284 is withdrawn as pattern-matching: the 24 is the de Sitter Kretschmann coefficient (pure GR), the $\sqrt3$ is $1/c_{\rm lat}$; unrelated origins, and the ladder vanishes under the alternative ceiling below.

## 8. Two conflicts in the prerequisites, flagged not settled

Both were found by this session's blind re-derivation and both are outside this finding's claim.

**(a) The curvature-ceiling fork.** F183 uses $K_{\max}=1/a^4$. F284's $H_{\max}=1/a$ implies $K_{\max}=24/a^4$ for a de Sitter ceiling ($K=24H^4$). They differ by $24^{1/4}$ in length and **only one can be fundamental**:

| | F183, $K\le a^{-4}$ (used here) | F284-consistent, $H\le1/a$ |
|---|---|---|
| $L$ | $24^{1/4}a=2.2134\,a$ | $a$ **exactly** |
| $E=1$ e-folding | $6^{3/4}=3.834$ ticks | $\sqrt3$ ticks — **exactly one cell crossing, $=$ F284's own $t_{\min}$** |
| $M_{\rm crit}$ | $a/\sqrt{96}=0.673\,m_{\rm Pl}$ | $a/2=3.30\,m_{\rm Pl}$ |

The second column is markedly more elegant — the core radius *is* one cell and the e-folding *is* the model's own minimum resolvable time — and may well be right. This finding uses F183's convention because F183 is the gate-tested prerequisite, and flags the fork as **an open decision deserving its own session**.

**(b) A $\sqrt3$ in the tick duration.** F107 gives $\tau_{\rm tick}=a/(c\sqrt3)=2.054\times10^{-43}$ s. F284 §5's SI $t_{\min}=6.161\times10^{-43}$ s with $t_{\min}=\sqrt3$ ticks implies $\tau_{\rm tick}=a/c=3.557\times10^{-43}$ s. These differ by $\sqrt3$; one is wrong. F354's $6^{3/4}$ uses only F284's *dimensionless* statement and is unaffected.

## 9. Resolvability, the corrected offset bound, and $M_{\rm ext}$ (check B7)

**The regular centre is $\sim2.2$ cells across.** A continuum metric is marginal exactly where the completeness question is sharpest. This is why both tiers matter: B1's conclusion follows from a *global* bound rather than a gradient expansion, and Tier A covers the sub-cell regime where no metric applies.

**Corrected offset bound.** BCC ($Im\bar3m$) inversion centres are all points with coordinates in $\{0,\tfrac12\}a$ — a simple-cubic array of spacing $a/2$, so corner and body-centre sites are equivalent. Its **covering radius is $(\sqrt3/2)(a/2)=\sqrt3\,a/4=0.433\,a$**, not the $a/4$ the first draft claimed — wrong by $\sqrt3$. Worse, the worst-case point $(\tfrac14,\tfrac14,\tfrac14)$ is Wyckoff **8c**, site symmetry $\bar43m=T_d$ — the very group §5(ii) shows is inversion-free. (Wyckoff 12d at $(\tfrac14,0,\tfrac12)$ is $\bar4m2=D_{2d}$, also non-centrosymmetric.) With the no-go of §5 this bound is in any case no longer load-bearing; it is corrected for the record.

**$M_{\rm crit}$ is a misnomer, and the real threshold is 28× higher.** $M_{\rm crit}=a/\sqrt{96}=0.673\,m_{\rm Pl}$ is where the core is one cell across. But the horizon disappears at $M_{\rm ext}=\tfrac{3\sqrt3}{4}L\approx19\,m_{\rm Pl}$, so an object at $M_{\rm crit}$ has **no horizon at all**. The physically meaningful statement, and a new one:

> **Sub-$19\,m_{\rm Pl}$ black holes do not exist in this model** — below $M_{\rm ext}$ the object is a horizonless lump. (The $3\sqrt3/4$ coefficient is interpolant-dependent; the scale $M_{\rm ext}\sim L\sim a$ is not.)

## 10. What is NOT claimed

1. **Not the maximal extension.** §6 is a local $r\to0$ analysis. Completeness of the full two-horizon conformal diagram is not established.
2. **The inner-horizon (mass-inflation) instability is untouched** — a dynamical question about perturbations. That the inner horizon sits at $\sim2.2$ cells means the continuum instability analysis does not straightforwardly apply either. **The strongest live threat, and the natural next session.**
3. **Saturation, the ceiling convention and the profile are inputs**, not derivations (§7, §8).
4. **Rotation is not covered.** Kerr's ring singularity is a different object; the F183 open item stands.
5. **No priority is claimed for the regularity criterion.** Antonelli & Sebastianutti (arXiv:2509.15477) publish it in stronger *iff* form in the two-function class, with differentiability classes. This finding's contribution is the substrate reading, the no-go, and the scales.
6. **The Bonanno–Reuter row is a screen output, not a literature claim.** BR carries an odd $r^3$ from the linear $\alpha r$ in its denominator and so sits in ZM's incomplete class; we have found no paper stating or disputing this and claim no priority.

## 11. Falsifiers

1. **The computable one.** Measure the $r^3$ coefficient of the coarse-grained core density from an actual CA run. If it is nonzero at leading order, the core is in Hayward's class and geodesically **incomplete**. §5 removed the symmetry argument that would have forbidden this, so it is now an open empirical question about the substrate — and a cheap one. *This is the finding's real test and it is currently unrun.*
2. **A demonstration that the coarse-grained metric is not $C^{1,1}$ at the centre** — e.g. that no continuum metric exists over a $\sim2$-cell region in a sense that makes B1 applicable. This would not break the algebra but would make it inapplicable.
3. **A proof that the BCC update rule is not total or not norm-preserving** in some reachable configuration. Breaks Tier A and the sub-cell regime.
4. **A mass-inflation result showing the inner horizon at $r\sim L$ destroys the static core.** Would not falsify the theorem but would make it irrelevant.
5. **Adjudication of the ceiling fork against F183's convention** would move every number in §7 by the §8 table — a recalibration, not a refutation.

## 12. Verdict

> **Bounded curvature does imply a regular centre here — but for a reason quite different from the one this finding first proposed.** Because the Kretschmann scalar is an exact *sum of squares* of orthonormal-frame Riemann components, the single global bound $K\le a^{-4}$ constrains each term independently and forces $B(0)=1$, $A'(0)=B'(0)=0$: a $C^{1,1}$ Lorentzian regular centre with no solid-angle defect, in the full two-function class, with no parity, no point group and no saturation assumed. Geodesics are unique there, so the $E>1$ and null rays that reach $r=0$ pass through it, and beneath the metric the automaton is tick-complete. The attractive claim that the BCC point group *forces* the parity condition is **false in both directions** — Hayward's own $O(3)$-invariant density carries an odd $r^3$ term, and $T_d$'s odd invariants have vanishing monopole — and the real hypothesis is smoothness of the coarse-grained density at the centre, which is exactly what a 2.2-cell core does not obviously supply. **E10: PARTIAL → a completeness result at the centre**, narrower and better-founded than the first draft, with the dead route recorded, three contingencies named, two prerequisite conflicts flagged, and one cheap computable falsifier left standing.

## 13. Exact vs computed vs open

| Piece | Status |
|---|---|
| $K$ is a sum of squares (two-function) | **exact** (verified against full Riemann contraction) |
| $K\le a^{-4}\Rightarrow B(0)=1$, $A'(0)=B'(0)=0$, $C^{1,1}$ | **exact-algebraic** |
| solid-angle deficit gives $Kr^4\to4\delta^2$ | **exact** (control, measured 0.0400 at $\delta=0.1$) |
| no-go leg (i): Hayward's odd $r^3$ | **exact-algebraic counterexample** |
| no-go leg (ii): $T_d$ odd invariants have zero monopole | **exact** |
| $O_h$-invariant *polynomials* have even degree | **exact** (Reynolds projection) — scope-limited to polynomials |
| geodesic regimes $E<1$, $E=1$, $E>1$, null, non-radial | **exact-algebraic**, local $r\to0$ |
| ZM calibration (Hayward $r^5$, coeff $2M/L^6$) | **exact**, reproduces a published coefficient |
| $L=24^{1/4}a$; $6^{3/4}$ ticks | **exact-algebraic**, contingent on saturation + ceiling |
| core radius, $2^{1/6}$ ratio to F183 | **exact-algebraic but Bardeen-specific** (Gaussian: 0.7218) |
| covering radius $\sqrt3a/4$; $M_{\rm ext}\approx19\,m_{\rm Pl}$ | **computed** |
| maximal-extension completeness | **OPEN** |
| inner-horizon stability | **OPEN** — next session |
| saturation as an equality | **OPEN** — needs dynamical CA collapse |
| ceiling-convention fork; F107/F284 tick $\sqrt3$ | **OPEN** — flagged, own sessions |
| rotating (Kerr) core | **OPEN** — inherits F183 |

## Files
- Module: `src/casim/engine/interactions/gravity_core_completeness.py`
- Test record: `F354-core-geodesic-completeness` in `tests/registry/interactions.yaml`
- Results: `test-results/F354_core_geodesic_completeness.json`
- Review: `docs/reviews/F354-review-2026-09-03.md`
- Claim card: `docs/claims/CL295-bounded-curvature-forces-a-regular-core-centre.md`
