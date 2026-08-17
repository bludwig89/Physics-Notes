# F278 — The BCC lattice constant is $a=2/\sqrt3$: F267's cube/BZ ratio **is** a primitive-cell volume, and F273's "$\sqrt3\cdot$fcc" **is** its reciprocal lattice

**Date:** 2026-08-02 - 10:15
**Status:** Exact algebraic derivation. Nine identities; five are symbolic (`sympy`, residual identically zero) and four evaluate to **exactly 0.0** in floating point. No physics number changes, no baseline moves, no module is touched. Promotes two previously *measured* constants to closed form.
**Origin:** Audit V item V4.3(a) (`docs/audits/physics-audit-report-2026-08-01.md`), which established the result but recorded it inside an audit rather than as a finding.
**Test status:** **no registry record yet** — a record is specified in §9 and has not been added (this finding's claim on the board is documentation-only).
**Cross-references:** [[F267-walk-bz-measure-not-the-fft-cube]] (whose measured $4/(3\sqrt3)$ this derives), [[F273-mode-sum-vs-bz-integral-audit]] (whose measured "$\sqrt3\cdot$fcc" period lattice this derives), [[F250-allk-gauge-pole-paired-photon]] (GP7, the no-doubler check §6 qualifies — it already scopes itself to $[-\pi,\pi]^3$), [[F277-qed-gluon-refold-period]] and [[F272-bgfield-loop-refold-period]] (the refold defect §5 explains structurally), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}$, which is $a/2$), [[F30-photon-dispersion-order-anisotropy-birefringence]], [[F69-paired-spinor-photon]].

---

## 1. Result

$$\boxed{\;a=\frac{2}{\sqrt3}\;\Longrightarrow\;
\underbrace{\frac{a^3}{2}=\frac{4\sqrt3}{9}=0.769800358919501}_{\text{F267's measured cube/BZ ratio}}
\;,\qquad
\underbrace{\frac{4\pi}{a}=2\pi\sqrt3}_{\text{F273's measured }\sqrt3\cdot\text{fcc}}\;}$$

The BCC walk in `casim.engine.lattice.bcc` is a faithful crystal walk on a body-centred-cubic lattice whose **conventional cube edge is $a=2/\sqrt3$**. Every number F267 and F273 reported as an empirical property of the sampling grid is a closed-form property of that crystal. The two findings stop being two measurements and become one geometric statement.

## 2. Where $a$ comes from — it is already in the code, unnamed

`bcc.py`'s `bcc_fractional_shift` applies the hop phase

$$e^{i\,\mathbf k\cdot\mathbf d/\sqrt3},\qquad \mathbf d\in\{(\pm1,\pm1,\pm1)\},$$

and its docstring explains the $1/\sqrt3$ as normalising the hop *length*: "the BCC nearest-neighbour hop in direction $\mathbf d$ has physical length $\lvert\mathbf d\rvert=\sqrt3$ in cubic-cell units". That is a statement about the phase, not about a lattice — the lattice is never named.

Name it. A phase $e^{i\mathbf k\cdot\boldsymbol\delta}$ is a hop by the real-space vector $\boldsymbol\delta$, so the walk's actual hop vector is

$$\boldsymbol\delta=\frac{\mathbf d}{\sqrt3}=\frac{1}{\sqrt3}(\pm1,\pm1,\pm1).$$

In a BCC lattice with conventional cube edge $a$ the nearest-neighbour vector is $\tfrac a2(\pm1,\pm1,\pm1)$. Matching:

$$\frac a2=\frac1{\sqrt3}\;\Longrightarrow\;\boxed{a=\frac2{\sqrt3}=2c_\text{lat}=1.1547005384}$$

and then $\lvert\boldsymbol\delta\rvert=\tfrac a2\sqrt3=1$ **exactly** — the unit hop V2.1 identified. So $a$ is not a new parameter. It is $2c_\text{lat}$: the same $1/\sqrt3$ the model already carries as the lattice speed of light, wearing its other hat as a length.

`c_lat` and $a/2$ are not merely equal to within a tolerance — they are the **same IEEE-754 double**, `0x3fe279a74590331d`, so `a/2 == c_lat` is `True` and the residual is **exactly 0.0**. That is why the constant never had to be introduced separately, and why it was never noticed. (Caveat worth recording, since it bit this write-up: evaluating $2/\sqrt3$ through `sympy`'s float path returns a double **one ulp below** `2*c_lat` — $\ldots515$ vs $\ldots517$ in `repr`. The bit-identity holds in the direction that matters, $a\equiv2c_\text{lat}$; a decimal literal transcribed from an independent evaluation does not. Do not write $a$ as a literal — derive it from `c_lat`, per D7.)

## 3. The direct lattice

| quantity | closed form | value |
|---|---|---|
| conventional cube edge $a$ | $2/\sqrt3$ | $1.1547005384$ |
| nearest-neighbour distance $\tfrac{\sqrt3}2a$ | $1$ | $1$ (exact) |
| points per conventional cell | $2$ | $2$ |
| **primitive cell volume** $a^3/2$ | $4\sqrt3/9$ | $0.7698003589$ |

## 4. F267's ratio is that primitive-cell volume, and the proof is one line

F267 measured that the cubic FFT cube covers $4/(3\sqrt3)$ of one true Brillouin zone and recorded it as an empirical ratio. It is not empirical.

The FFT grid samples $\mathbf k\in(-\pi,\pi]^3$, which is the Brillouin zone of a **simple cubic lattice of edge 1** — a lattice of primitive cell volume exactly $1$. The true zone belongs to the BCC crystal of §2, so

$$\frac{V_\text{cube}}{V_\text{BZ}}=\frac{(2\pi)^3}{(2\pi)^3/V_\text{prim}}=V_\text{prim}=\frac{a^3}{2}=\frac{4\sqrt3}{9}.$$

The ratio of the two zone volumes **equals the primitive cell volume as a pure number** precisely because the sampling lattice has unit cell volume. Numerically: $V_\text{BZ}=322.2266793829$, $V_\text{cube}=248.0502134424$, ratio $0.769800358919501$ — agreeing with $4\sqrt3/9$ to the last digit, and symbolically identical (`sympy` residual $\equiv0$).

So the cube is not an arbitrary $77\%$ of the zone. It is $77\%$ because the walk hops one unit while the grid is indexed in cube edges, and the two disagree by exactly the BCC packing factor.

## 5. F273's period lattice is the reciprocal of the same crystal

The reciprocal lattice of a BCC direct lattice with cube edge $a$ is an FCC lattice with cube edge $4\pi/a$. Here

$$\frac{4\pi}{a}=2\pi\sqrt3=10.882796185405308=\sqrt3\times2\pi.$$

F273 measured that every dispersion in the tree is periodic under a "$\sqrt3\cdot$fcc" lattice, where the implied baseline fcc has cube edge $2\pi$ — that being the period lattice the cubic FFT grid *assumes*. The measured factor $\sqrt3$ is therefore $4\pi/a$ divided by $2\pi$, i.e. the same $a$ again. F273's period lattice and F267's zone volume are the direct and reciprocal descriptions of one crystal, and neither needed to be measured.

**This also explains, structurally, why the refold defect of F272/F277 is a defect.** Applying $((k+\pi)\bmod2\pi)-\pi$ asserts a $2\pi$-per-axis period. The kernel's period lattice is FCC with cube edge $2\pi\sqrt3$, which does not contain the simple-cubic $2\pi$ lattice as a sublattice — so the wrap maps $k$ to a genuinely inequivalent momentum. F272 established this empirically; §5 gives the reason.

## 6. The $\Gamma$–H point, and the qualification it forces on "no doublers"

The BCC zone corner H sits at $\lvert\mathbf k\rvert=2\pi/a$ along a cube axis. Here

$$\frac{2\pi}{a}=\pi\sqrt3=5.441398092702654,$$

and evaluating the shipped dispersion there gives, on **both** branches,

$$\omega^\pm\!\big(\pi\sqrt3,0,0\big)-\pi=\mathbf{0.0}\quad\text{(exactly, in floating point).}$$

So the $\omega=\pi$ mode is not merely "outside the FFT cube", which is how it was first framed — it sits **exactly on the true zone boundary**. Audit V's own verification pass (V9.5) reached the same conclusion independently.

Consequently the no-doubler result must be stated with its domain:

> **On the FFT cube** ($L=24,25,33,36,48,64,96,128$, both branches) there is exactly one zero, located at $\mathbf k=0$, and no $\omega=\pi$ point; $\max\omega=3.11355278$ on the $L=48$ cube, strictly below $\pi$.

Every observable in the tree is computed on the cube, so **F250 and F69 stand as computed** and nothing operational changes. F250's own GP7 check is already written with its domain ("over the photon BZ $[-\pi,\pi]^3$"), so the finding files are not at fault; what needs the qualification is the *summary* form of the claim, which appears in prose and in the papers as "no doublers" full stop. Without a domain that is a claim about the crystal, and on the crystal there is a $\pi$-mode at H. Whether that constitutes a doubler is exactly the Reading 1 / Reading 2 question of F273 and audit V4.3, and it is **not decided here**. This finding sharpens the question by locating the mode exactly; it does not answer it. The discriminating experiment remains the constructive one: rebuild the walk on an explicit two-sublattice BCC site set with integer hops and measure $\langle\cot\omega\rangle$.

## 7. The gauge side, and the open "$\sqrt3$ question" it answers

F265 row 333 records the *gauge* link lattice: the BCC generated by the eight body-diagonal hops **at conventional cube edge 2** (integer `np.roll` hops, no fractional shift), whose reciprocal is fcc at $\pi(1,1,0)$, with $V_\text{BZ}=2\pi^3=(2\pi)^3/4$ — so the cube holds exactly **4 copies** of that zone.

That is the *same* formula. With $V_\text{prim}=a^3/2$,

$$\frac{V_\text{cube}}{V_\text{BZ}}=\frac{a^3}{2}=\begin{cases}4, & a=2\quad\text{(gauge links, integer hops)}\\[4pt] \dfrac{4\sqrt3}{9}=0.7698, & a=\dfrac2{\sqrt3}\quad\text{(fermion walk, fractional hops)}\end{cases}$$

So the gauge sector's "4 copies" and the fermion sector's "$77\%$ of one copy" are one relation evaluated at two lattice constants, and the constants differ by exactly

$$\frac{a_\text{gauge}}{a_\text{fermion}}=\frac{2}{2/\sqrt3}=\sqrt3,\qquad \frac{4}{4\sqrt3/9}=\frac{9}{\sqrt3}=3\sqrt3=(\sqrt3)^3 .$$

**This answers the standing "$\sqrt3$ question"** (`docs/roadmaps/next-steps.md`, F265 follow-on): *"the link side is the integer BCC lattice while the fermion walk uses $e^{ik\cdot d/\sqrt3}$ — does the fermion sector need the same factor-4 measure correction?"*

**No.** The two sectors are the same crystal at two units of length, and the measure factor is $a^3/2$ evaluated at each sector's own $a$ — 4 for the links, $4\sqrt3/9$ for the walk. Transplanting the gauge side's 4 onto the fermion side would over-correct by $(\sqrt3)^3=3\sqrt3\approx5.196$. What the fermion sector needs is not the gauge factor but its own, and F267's measured $0.7698$ was already it.

This does **not** decide Reading 1 vs Reading 2 (§6): it fixes *what* the correct measure would be, not *whether* the cube sum should be replaced by a zone integral in any given site. F273/V4.4's site classification stands unchanged.

## 8. What this changes, and what it does not

**Changes.** Two constants move from *measured* to *closed form*: F267's $4/(3\sqrt3)$ and F273's $\sqrt3$. Both become Tier-1 exact algebraic results (see `docs/status/exactness-inventory.md`). The refold defect acquires a structural explanation (§5). The no-doubler claim acquires a stated domain (§6).

**Does not change.** No physics number, coefficient, constant value or baseline. $a$ is not a new registered constant — it is $2c_\text{lat}$, and registering it separately would violate the D7 rule against constants that are functions of other constants. The Reading 1 / Reading 2 question is untouched, and so is its bounded blast radius: the charged-lepton spectrum depends on no $k$-space average (audit V4.3d, re-measured at $0.003\%$), so it survives either outcome.

**Not to be confused with the SI cell.** $a=2/\sqrt3$ is a *dimensionless lattice-unit* statement about the walk's geometry. It is **not** the canonical physical cell size of F107/F112 and carries no metres.

## 9. Check summary (9/9)

| # | Statement | Method | Residual |
|---|---|---|---|
| 1 | $a=2/\sqrt3$ from $\tfrac a2=1/\sqrt3$ | algebra | exact |
| 2 | $a/2$ and `c_lat` are the **same double** (`0x3fe279a74590331d`) | bit compare | $0.0$ (`==` is `True`) |
| 3 | $\lvert\tfrac a2(1,1,1)\rvert=1$ | sympy | $\equiv0$ |
| 4 | $a^3/2=4\sqrt3/9$ | sympy | $\equiv0$ |
| 5 | $4\sqrt3/9=4/(3\sqrt3)$ = F267's measured ratio | sympy | $\equiv0$ |
| 6 | $V_\text{cube}/V_\text{BZ}=a^3/2$ | sympy | $\equiv0$ |
| 7 | $4\pi/a=\sqrt3\cdot2\pi$ = F273's measured factor | sympy | $\equiv0$ |
| 8 | $2\pi/a=\pi\sqrt3$ ($\Gamma$–H) | float | $0.0$ |
| 9 | $\omega^\pm(\pi\sqrt3,0,0)=\pi$, both branches | `bcc_dispersion` | $0.0$, $0.0$ |

**Proposed test record** (not added; specified so it can be):

```yaml
- id: F278-bcc-lattice-constant
  path: tests/findings/test_F278_bcc_lattice_constant.py
  kind: assertion
  tier: gate
  sector: lattice
  findings: [F278, F267, F273]
  module: casim.engine.lattice.bcc
  entry: check_lattice_constant_identities
  expect: {exactness: exact, tol: 0}
```

It has a real failure mode: any change to `c_lat`, to the hop-phase convention in `bcc_fractional_shift`, or to `_bcc_uvec` breaks checks 2, 6 or 9. That makes it a candidate answer to audit item **V-016**, which found nothing guarding the $c_\text{lat}$ separation.

## 10. Limitations

1. §6 states where the $\pi$-mode is; it does not decide whether it is a doubler. That needs the V4.3 constructive test.
2. Checks 8 and 9 are floating-point evaluations of the shipped `bcc_dispersion`, which audit V-015 found ill-conditioned near $k\to0$. They are evaluated at $k=\pi\sqrt3$, far from that regime, so the conditioning hazard does not apply here.
3. The identification of the walk's crystal is a statement about the *phase convention* in `bcc_fractional_shift`. F267 S5's independent evidence — translating a delta by one BCC hop at $L=16$ spreads it over 2274 of 4096 cells — corroborates that the array's sites are not the walk's sites, but this finding does not re-run it.
