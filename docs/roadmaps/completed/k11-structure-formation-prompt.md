# K11 — Structure formation and $\sigma_8$: the investigation prompt

**Written:** 2026-08-05 - 09:40
**Source:** `docs/status/completeness-2026-08-04.md`, ABSENT table and the K block.
**Row attacked:** **K11 — Structure formation / $\sigma_8$**, graded `ABSENT`:

> *"Zero hits, on four separate keyword sweeps. Downstream of a row that is now `OPEN` again (K3),
> so the cause has changed even though the grade has not."*

K11 is one of only two cosmology rows with **no entry point at all** (the other is K2, BBN).
Unlike the four quantum-foundations absences (A8, A9, A10, G10), K11 is absent in the *ordinary*
sense: the machinery to attack it already exists in the tree and nobody has connected it.

---

## 1. What the row actually asks

Linear structure formation has exactly three inputs, and the model's standing on each is
already decided by other rows:

| Ingredient | Model's standing | Row |
|---|---|---|
| Background $H(a)$ | **Have it.** Full-tensor source reproduces ΛCDM: $z_\text{eq}\approx3430$, $z_\text{acc}=0.63$, age 13.8 Gyr | K1 (`QUANT`, F182/F188) |
| Growth of $\delta_m$ under the model's own gravity | **Nothing.** This is the gap | K11 |
| Primordial $P(k)$ | **Provably a free initial condition.** $A_s$ has no route | K5 (`EXCLUDED`, F282/F284/F285) |

So the honest target is **not** "predict $\sigma_8$ from nothing" — K5 forecloses that, and a
finding that pretended otherwise would be exactly the kind of overstatement the 2026-08-03/04
review series caught ten times out of ten. The target is the middle row:

> **Does the model's own gravity law fix the growth of matter perturbations, and does it fix it
> with any freedom left over?**

That question is answerable, and the answer is worth more than a $\sigma_8$ number, because
**growth is the one place a gravity theory can differ from GR without differing in the background.**

---

## 2. The specific attack

### 2.1 The structural core — is $\mu=\Sigma=1$ forced?

The standard parametrization of any deviation from GR in linear growth is two free functions:

$$k^2\Psi=-4\pi G a^2\mu(a,k)\,\bar\rho\,\Delta,\qquad
k^2(\Phi+\Psi)=-8\pi G a^2\Sigma(a,k)\,\bar\rho\,\Delta .$$

Every modified-gravity model in the S8 literature lives in $(\mu,\Sigma)$. Derive what the model
puts there, from machinery it already owns:

- **$\mu$** from F106's $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ — live as the *static weak-field
  reduction* of F178, which is exactly the quasi-static sub-horizon regime growth needs. With
  $\ln K=2\Phi/c^2$ this must collapse to $\nabla^2\Phi=4\pi G\bar\rho a^2\delta$ with **no $k$**.
- **Slip** from the impedance-match $AB\equiv1$ ($A=1/K$, $B=K$, F64 / decision 4 in `CLAUDE.md`),
  which is the same condition as PPN $\gamma=1$ (F64 D-EM9). Compute the slip $\eta=\Phi/\Psi$
  **exactly**, not to leading order, and report the order at which $AB\equiv1$ stops enforcing it.
- **Time dependence** from F284: $G$ structural (F79) on a rigid substrate ⇒ $\dot G/G\equiv0$
  ⇒ $\partial_a\mu\equiv0$ for the same structural reason, not as a separate assumption.

**State the result as a constraint count.** If all three land, the model has **zero free functions**
in its structure-formation sector where the EFT of dark energy has two — i.e. the model is *more*
constrained than GR-as-an-EFT, and every one of those three closures is named and independently
sourced. That is the finding's headline, and it is falsifiable.

### 2.2 The derived numbers

With $\mu\equiv1$ established, these follow and must be **derived, not asserted**:

1. **The growth index $\gamma_g=6/11$, exactly.** Substitute $f=\Omega_m^{\gamma_g}$ into the
   model's own growth equation and expand about $\Omega_m=1$. Do it in sympy and require a literal
   zero. Then compute $\gamma_g$ numerically on the F188 background at $z=0$.
2. **The Meszáros solution $D(y)=1+\tfrac32 y$, exactly**, $y=a/a_\text{eq}$. This is the one place
   the transfer-function *shape* is genuinely derived rather than imported: sub-horizon CDM in the
   radiation era. Require a sympy zero residual.
3. **$D(a)$, $f(a)$, $f\sigma_8(z)$** integrated on the F188 background, compared to a stated RSD
   compilation including the 2025 DESI DR1 peculiar-velocity point.
4. **$\sigma_8$** from $A_s$, with the import budget stated in the same sentence as the number.

### 2.3 The two bounds nobody has computed

5. **Discreteness.** Growth is computed in the continuum. What licenses that? Bound the leading
   $O((ka)^2)$ correction at the $8\,h^{-1}$ Mpc scale using F284's $a=1.0664\times10^{-34}$ m and
   F130's block-spin irrelevance $\lambda_n=b^{-n}$. Do it at the Lyman-α scale too — that is the
   smallest scale structure formation ever probes.
6. **Dark-matter free streaming.** K7 carries two candidates: the Planck-mass geon remnant
   ($M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$, F223/F228) and the F266 sterile neutrino at
   $\sim5.6$ keV. Compute the half-mode scale and the $\sigma_8$ suppression for each.
   **Expect $\sigma_8$ to be blind to the difference** — say so if it is, and name the observable
   that is not.

### 2.4 The falsifier, and it must be able to fire

The S8 landscape as of 2026 is *split*, not resolved:

| Probe | $S_8$ | vs combined CMB |
|---|---|---|
| Combined CMB (Planck18+ACT DR6+SPT-3G) | $0.836^{+0.012}_{-0.013}$ | baseline |
| DES Y6 $3\times2$pt | $0.789\pm0.012$ | **2.7σ low** |
| KiDS-Legacy | $0.815^{+0.016}_{-0.021}$ | consistent (up $0.056$ from KiDS-1000) |
| eROSITA eRASS1 clusters | $0.86\pm0.01$ | 1.5σ **high** |

A model with $\mu\equiv1$ and **no screening mechanism** has no way to lower late-time growth.
The 2026 review notes that MG relief of S8 generally requires effects "confined to nonlinear
scales through efficient screening" — a hatch the lattice does not have, because $\mu=1$ is
$k$-independent by derivation. So:

> **State the falsifier in the form that can fire.** If the DES Y6 direction consolidates as
> physical rather than as photo-$z$/feedback systematics, the model's gravity sector is falsified
> outright — it cannot be accommodated by tuning, because there is nothing to tune.

Per completeness gap #2 (H2 falsifier soundness): the registry record must carry a **control leg**
that goes red under `casim test --param`. Perturbing $\mu$ off 1 must actually break a check.

---

## 3. Discipline constraints on this session

1. **Do not claim $\sigma_8$ is predicted.** K5 is `EXCLUDED` with the cause named. $\sigma_8$ is
   $A_s$-linear; report it with $A_s$, $n_s$ and the transfer-function fit coefficients listed as
   imports in the same table as the result.
2. **Do not claim a discriminating test where there is a consistency test.** Reproducing ΛCDM
   growth is a *consistency* result. What is new is the constraint count, not the curve.
3. **Name the regime.** F178 demoted the energy-only law to the static weak-field reduction.
   Growth uses it in the quasi-static sub-horizon regime, where that reduction is exactly valid.
   Say where it stops being valid (super-horizon, radiation era relativistic modes).
4. **The RSD $\chi^2$ is indicative, not a likelihood** — BOSS DR12's three points are correlated
   and a diagonal $\chi^2$ ignores it. Say so next to the number.
5. Every check must have a failure mode (D9 `validate()`), and at least one must be demonstrated
   red under a perturbation.

## 4. Deliverables

- `src/casim/engine/interactions/cosmology_growth.py` — new engine module, `_SPINE` record.
- A **gate-tier** `kind: assertion` record in `tests/registry/interactions.yaml` with an `entry:`
  and a demonstrated control.
- `findings/F{N}-...md` at the **lowest free number** (`casim index` → `NEXT FREE NUMBER`), taken
  at write time, with that number's `free` entry deleted from `docs/design/finding-numbers.yaml`
  in the same edit.
- A claim card in `docs/claims/`, with the S8 falsifier stated.
- Changelog entry, exactness-inventory rows, `make indexes`, gate checks.

## 5. Grade this should move

`K11: ABSENT → PARTIAL` — growth derived with zero free functions, $\sigma_8$ computed with
$A_s$ declared free. It cannot reach `QUANT` while K5 stands.
