# F24 — Weyl SL(2,ℂ) Boost: Lorentz 4-Current Covariance

**Date:** 2026-05-23  
**File:** `casim.engine.gauge.bilinear` — `sl2c_boost`, `sl2c_rotation`, `weyl_sl2c_4current_covariance`, `sl2c_covariance_full`. Record: `F24-sl2c-covariance-full` (gate). Result: `test-results/F24_sl2c_covariance_full.json`.  
**Test tag:** C7  
**Residual:** 3.71 × 10⁻¹⁶ (machine precision)  
**Reviewed:** 2026-08-04 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F24-review-2026-08-04.md))  
**Remediated:** 2026-08-04 — 8 applied · 1 deferred ([remediation](../docs/reviews/F24-remediation-2026-08-04.md))

---

## Statement

The SL(2,ℂ) pure-boost matrix

$$A = \exp\!\left(-\tfrac{\zeta}{2}\,\boldsymbol\sigma\cdot\hat{v}\right)
    = \cosh\tfrac{\zeta}{2}\,I_2 - \sinh\tfrac{\zeta}{2}\,(\boldsymbol\sigma\cdot\hat{v})$$

correctly induces the defining SL(2,ℂ) → SO(1,3) homomorphism on the
Weyl 4-current.  For any Weyl spinor $\psi$ and boost $({\hat v},\zeta)$:

$$j'^\mu \;\equiv\; (A\psi)^\dagger\,\bar\sigma^\mu\,(A\psi)
  \;=\; \Lambda^\mu{}_\nu\,j^\nu, \qquad
  j^\mu = \psi^\dagger\bar\sigma^\mu\psi$$

where $\bar\sigma^0 = I_2$, $\bar\sigma^i = \sigma^i$, and $\Lambda$ is the 4×4
Lorentz boost matrix with rapidity $\zeta$ along $\hat{v}$.

**Sign convention (added 2026-08-04, review attack 10).** $\Lambda$ here is the boost with
$\Lambda^{0i} = \Lambda^{i0} = -\sinh\zeta\,\hat v^i$ — as the module docstring has always
stated, and as the `## Key identity` section below requires. Against the *standard active*
convention ($+\sinh\zeta\,\hat v^i$) this pairing realises $\Lambda(-\zeta)$, i.e. the inverse
boost: measured relative residual **4.963$\times10^{+1}$** against $\Lambda(+\zeta)$ versus
**2.090$\times10^{-15}$** against $\Lambda(-\zeta)$. A reader implementing from the statement
without this line gets the inverse boost.

Verified across 12 random $(\hat k, \hat v)$ pairs at $|k|=0.3$, $v/c=0.6$ using
BCC eigenmodes; max relative residual $|j' - \Lambda j|/|\Lambda j| = 3.71\times 10^{-16}$.
**That number is a benign sample, not a floor** — see `## Corrections`. The worst case over 2000
draws is $1.11\times10^{-13}$ at $\zeta \approx -6.9$, and the limit is *conditioning*, not
machine epsilon.

---

## Representation-theory context

The bilinear $G^i = \psi^T\sigma^i\psi$ of Paper 1 Eq. 33 uses a **transpose**,
not a dagger.  Under $\psi\to A\psi$ it transforms as

$$G'^i = \psi^T A^T\sigma^i A\,\psi
  \;=\; \Lambda_{(1,0)}^{ij}\,G^j - \sinh\zeta\,\hat v^i\,(\psi^T\psi)$$

The second term is a **(0,0) scalar contamination** pointing along $\hat v$.
It is non-zero for generic BCC eigenmodes (typical $|\psi^T\psi|\approx 0.67$)
and survives transverse projection onto $\hat k'$ whenever $\hat v\not\perp\hat k'$.

Therefore $G^i = \psi^T\sigma^i\psi$ lies in the **self-dual (1,0)** Lorentz
irrep — distinct from the **(½,½)** Maxwell-field irrep on which Mohr's V6
boost operates.  Direct comparison of the (1,0) bilinear to the V6 result is
ill-posed in general.

The correct (½,½) object at the spinor level is the Weyl 4-current
$j^\mu = (\psi^\dagger\psi,\,\psi^\dagger\boldsymbol\sigma\psi)$,
which IS directly comparable to V6 through the 4-vector boost $\Lambda$,
and is verified here to machine precision.

---

## Key identity (verified)

For a z-boost $A = \operatorname{diag}(e^{-\zeta/2}, e^{\zeta/2})$:

$$A^\dagger\,\sigma_z\,A = \cosh\zeta\;\sigma_z - \sinh\zeta\;I_2$$

Contracting with $\psi^\dagger(\cdots)\psi$:

$$j'^z = \cosh\zeta\;j^z - \sinh\zeta\;j^0 \qquad \checkmark$$

which is exactly the $z$-component of a Lorentz 4-vector boost.

---

## Implementation

```python
def sl2c_boost(v_hat_c, zeta):
    v = np.asarray(v_hat_c, dtype=float)
    sigma_v = v[0]*_S_X + v[1]*_S_Y + v[2]*_S_Z
    ch = np.cosh(float(zeta)/2); sh = np.sinh(float(zeta)/2)
    return ch*np.eye(2, dtype=complex) - sh*sigma_v

def weyl_sl2c_4current_covariance(k_mag=0.3, v_mag=0.6, n_dirs=12, seed=7):
    # For each (k̂, v̂): compute j = (ψ†ψ, ψ†σψ), boost with Λ,
    # compare to j' = ((Aψ)†(Aψ), (Aψ)†σ(Aψ)).
    # Returns max |j' - Λj| / |Λj|.
```

---

## Significance

**CORRECTED 2026-08-04.** This is a **convention and regression check**, not a physics
result, and it does *not* close the Lorentz-covariance loop.

$\psi^\dagger\bar\sigma^\mu\psi = \operatorname{tr}(\bar\sigma^\mu\,\psi\psi^\dagger)$, and
$\psi\psi^\dagger$ is rank-1 positive Hermitian; under $\psi\to A\psi$ it goes to
$A(\psi\psi^\dagger)A^\dagger$. But $H\mapsto AHA^\dagger$ on $\mathrm{Herm}(2)\cong\mathbb R^{1,3}$
**is the definition** of the SL(2,ℂ)→SO⁺(1,3) covering map. So the claim reduces to *"the covering
map, restricted to the null cone, is the covering map"* — it could not have come out false.
(Rank-1 $\Rightarrow \det = 0 \Rightarrow j$ null; measured nullity $8.7\times10^{-16}$.)

It is not vacuous: a Lorentz transformation is determined by its action on the null cone, so the
check does pin $\Lambda$ uniquely, and it legitimately guards a wrong exponent sign, $\zeta$ vs
$\zeta/2$, a $\bar\sigma$ spatial sign mismatched to the chirality, a transpose where a dagger
belongs, a mis-assembled $\Lambda$, and a dropped imaginary component in a chiral transform (the
standing `CLAUDE.md` hazard). **That is code correctness.** The residual confirms no implementation
errors in `sl2c_boost`; it says nothing about the lattice.

**No lattice content enters.** This is continuum $2\times2$ spinor algebra: no $a$, no
$c_\text{lat}$, no BCC geometry, no dispersion, no CA tick. The $\psi$ are drawn from BCC
eigenmodes but the identity holds for any two-component complex vector. **The load-bearing question
for this project — whether the lattice *evolution* commutes with a boost at finite $a$, i.e.
emergent Lorentz invariance — is untouched by this identity and would generically not be exact.**
That is the finding that should exist next.

The (1,0) bilinear structure of the composite photon is a separate open question:
the correct Lorentz covariance of $G = \psi^T\sigma\psi$ under boosts involves
the (1,0) representation and its scalar contamination term, which is the subject
of future study.

---

## Prior art

Added 2026-08-04 (review attack 11). The identity is standard bookwork and was not
cited. The construction $X = x_\mu\sigma^\mu \to AXA^\dagger$ as the 2:1 cover, and
the corollary that $\psi^\dagger\bar\sigma^\mu\psi$ is a 4-vector, appear in Peskin
& Schroeder §3.2, Srednicki ch. 34–35, Weinberg vol. I §2.7 and Wess & Bagger
app. A. The nullity of the single-Weyl current ($\det\psi\psi^\dagger = 0$) is
equally standard. Self-contained public write-ups:
[Stange, *The spin homomorphism* $SL_2(\mathbb C)\to SO_{1,3}(\mathbb R)$](https://math.colorado.edu/~kstange/papers/notes-Spin.pdf) ·
[Feng, *The homomorphism between SL(2,ℂ) and the Lorentz group*](https://fengshi96.github.io/gleanings/homo_sl_lorentz/draft.pdf).

**"Implemented and verified here" survives. "Novel" does not**, and was never
explicitly claimed — but the finding read as one, and the exactness inventory row
50 carries it as a Tier-1 result.

## Corrections

**2026-08-04 - 14:50** — per [independent review 2026-08-04](../docs/reviews/F24-review-2026-08-04.md),
verdict **CONFIRMED-NARROWER** (3 PASS · 5 WEAKENS · 5 FAIL).

| Was | Now | Why | Attack |
|---|---|---|---|
| "This closes the Lorentz-covariance loop at the spinor level" | A convention and regression check of a textbook identity; the loop that matters (does the lattice *evolution* commute with a boost at finite $a$?) is untouched | $H\mapsto AHA^\dagger$ **is** the definition of the covering map, so the check could not have come out false | 1, 10 |
| "residual $3.71\times10^{-16}$ … at the IEEE-754 double-precision floor" | A benign 12-draw sample. Worst case over 2000 draws is $1.11\times10^{-13}$ at $\zeta\approx-6.9$; the blind agent's 50 000-draw sweep gives $1.83\times10^{-13}$ | The limit is **conditioning, not eps**: $j$ is null, so an anti-aligned boost makes $j'^0$ a near-total cancellation and the relative error grows like $e^{2\zeta}\epsilon$ | 4 |
| "$\Lambda$ is the 4×4 Lorentz boost matrix with rapidity $\zeta$ along $\hat v$" | $\Lambda^{0i} = -\sinh\zeta\,\hat v^i$ stated explicitly | Read against the standard *active* convention this pairing is $\Lambda(-\zeta)$ — measured relative residual **49.63** vs $\Lambda(+\zeta)$ | 10 |
| boosts only, 12 draws, one $v/c$ | rotations and boost∘rotation compositions added; 2000 draws | A pure boost is **Hermitian**, so $A^\dagger = A$ and the sandwich is blind to the dagger's placement — the single most likely implementation error sat in the branch never exercised. Rotations are unitary; worst rel $5.9\times10^{-16}$, compositions $4.2\times10^{-14}$ | 12 |
| test rides on a six-finding battery `result_dump` with `has_assert: false` | gate record `F24-sl2c-covariance-full`, `kind: assertion`, `expect: {exactness: machine, tol: 1e-10}` | The old record fails only by baseline diff | 7, 8 |
| no prior art | `## Prior art` | Textbook identity, uncited | 11 |
| `ca-simulation/ca_maxwell.py` | `casim.engine.gauge.bilinear` | Pre-C9 path | 9 |

**Confirmed unchanged.** The identity is exact and the implementation is correct:
`weyl_sl2c_4current_covariance()` returns **3.707420040408194e-16**, reproduced
bit-for-bit. The blind agent proved it at the **operator** level —
$A^\dagger\bar\sigma^\mu A = \Lambda^\mu{}_\nu\bar\sigma^\nu$ as $2\times2$ matrices,
so the bilinear statement follows for *every* $\psi$ and every $(\hat v,\zeta)$ with
no conditions — which is stronger than this finding states. Free inputs: none, as
claimed. No numerology, nothing stale.

**Rejected.** None.

**Escalated.** None — this finding's fixes touch no canonical decision and no
supersession. The reviewer's explicit view is that F24 does **not** belong in
`S1-F69-sigma-bilinear-photon`: the Hermitian 4-current $\psi^\dagger\bar\sigma^\mu\psi$
is not the retired transpose bilinear, and F24 is the file that says so.

## The part of this finding that was under-titled

The review's highlight, recorded here because the finding buried it: the
`## Representation-theory context` section derives that under $\psi\to A\psi$ the
**transpose** bilinear picks up a $-\sinh\zeta\,\hat v^i(\psi^T\psi)$ term — a
$(0,0)$ scalar contamination — and concludes $G^i = \psi^T\sigma^i\psi$ lies in the
**$(1,0)$** irrep rather than the $(\tfrac12,\tfrac12)$ Maxwell one, so direct
comparison is ill-posed. **F302 (2026-08-03) reached the same conclusion by an
independent route** ($U^T\epsilon U = \det(U)\,\epsilon$, SO(3) covariance measured
to miss by 1.96) and did not cite F24. This finding got there two months earlier and
its title does not mention it.

## Status

**Live**, narrowed. The identity and the implementation are correct and now carry a
gate record covering boosts, rotations and compositions with a worst-case residual.

Open: the real question — whether the lattice **evolution** commutes with a boost at
finite $a$. Nothing here bears on it, and it would generically not be exact
(Brillouin zone plus finite $a$ break boosts). Landing site:
`docs/roadmaps/next-steps.md`.
