# F276 — The variable-$c$ Weyl stepper had global order **zero**; Weyl ordering plus the $h^2W^2/2$ term makes it second order and unitary

`2026-08-01 - 01:40`

**Status:** Confirmed — algebraic derivation + machine-precision numerical verification. Both corrections are *derived*, neither is fitted.

**Module:** `casim.engine.lattice.curved` (`_half_step_dH`, new `_W_dH` / `_sigma_grad_2d` / `_kgrid_2d`)

**Cross-references:** [[F271-k-resolved-dielectric-photon-propagator]] (the same two corrections, derived there for the 3-D $(\mathbf E,\mathbf B)$ sector and **handed back** for this module), [[F64-em-connection-gravity]], [[F270-total-energy-stress-energy-gravity-loop]].

**Supersedes:** the pre-F276 `weyl_step_2d_varc_strang` convergence claim ("Trotter error drops like $1/n_\text{sub}^2$, norm drift drops like $1/n_\text{sub}$") and the `scenarios/refraction_2d.yaml` header claim "exact-unitary (Strang)".

---

## Why this finding exists

F271 fixed two defects in the 3-D photon dielectric propagator and recorded, explicitly, that **both were still present in `lattice.curved._half_step_dH`** — the 2-D variable-$c$ construction F271 was itself lifted from — *and therefore in every F64-fork variable-$c$ result*. It did not fix them. Physics Audit V confirmed the handback and quantified the cost; Ben then directed the port.

The audit's measurement was the trigger: the stepper's norm drift **plateaued at $6.08\times10^{-2}$ and a $32\times$ refinement moved it by 0.23%**. A discretisation error that does not fall with refinement is not a discretisation error.

## The two corrections

Write $H(x)=c(x)\,\sigma\cdot\hat p$, split $c=c_0+\delta c(x)$, and Strang-compose the inhomogeneous part about the exact FFT step for $c_0$. With $\sigma\cdot\hat p=-i\,\sigma\cdot\nabla$ the half-step generator is $-i\,\delta H = -W$, so the half-step is $e^{-hW}$.

### (i) Ordering — the generator was not anti-Hermitian

$\delta c(x)\,\sigma\cdot\hat p$ is a product of a position operator and a momentum operator, so *"the"* operator is undefined until an ordering is chosen. The code used the asymmetric $W_\text{asym}=\delta c\,(\sigma\cdot\nabla)$.

$\delta c$ is Hermitian and $\sigma\cdot\nabla$ is anti-Hermitian, so their **product is neither**, while their **anticommutator is anti-Hermitian**. The Weyl-symmetric choice

$$W=\tfrac12\{\delta c,\ \sigma\cdot\nabla\}$$

is anti-Hermitian by construction, hence $e^{-hW}$ is exactly unitary. The asymmetric product is not, so its norm error is present *in the generator* and **no step size removes it** — which is exactly the plateau.

### (ii) Truncation order — Strang was being wasted

$$e^{-hW}=\mathbb 1-hW+\tfrac{h^2}{2}W^2+O(h^3)$$

The code kept only $\mathbb 1-hW$. That leaves an $O(h^2)$ *local* error which the symmetric Strang composition does **not** cancel, so the scheme was globally first order at best. The $\tfrac{h^2}{2}W^2$ term costs one more application of the same operator and restores the second order the composition was always supposed to deliver.

### (iii) A third, smaller correction the port forced

The spectral first derivative $ik$ is **not anti-Hermitian at the Nyquist bin** for even $L$: the FFT frequency set contains $-\pi$ with no $+\pi$ partner, so the symbol is not odd there. Left alone it reintroduces precisely the non-unitarity (i) exists to remove. `_kgrid_2d` zeroes the Nyquist multiplier — the standard spectral remedy, and what the centred-difference path does automatically. Measured impact: $1.9\times10^{-11}$ on a smooth Gaussian packet (which carries essentially no Nyquist content) and $1.4\times10^{-2}$ on a white-noise field.

## Result 1 — norm drift: plateau → $1/n_\text{sub}^3$

$L=64$, 20 ticks, $\delta c=0.05\tanh(x/8)$, isolating each correction:

| $n_\text{sub}$ | asymmetric, 1st order (**pre-F276**) | ratio | Weyl, 1st order | ratio | **Weyl, 2nd order (F276)** | ratio |
|---:|---|---:|---|---:|---|---:|
| 1 | 4.314e-2 | — | 1.732e-3 | — | 4.263e-8 | — |
| 2 | 4.228e-2 | 1.02 | 8.653e-4 | 2.00 | 5.327e-9 | 8.00 |
| 4 | 4.184e-2 | 1.01 | 4.325e-4 | 2.00 | 6.659e-10 | 8.00 |
| 8 | 4.163e-2 | 1.01 | 2.162e-4 | 2.00 | 8.324e-11 | 8.00 |
| 16 | 4.152e-2 | 1.00 | 1.081e-4 | 2.00 | 1.043e-11 | 7.98 |
| 32 | 4.146e-2 | **1.00** | 5.404e-5 | 2.00 | **1.335e-12** | 7.81 |

The three columns separate the two corrections cleanly:

- **Ordering alone** converts a plateau (ratio 1.00) into $1/n_\text{sub}$ convergence. That is correction (i) doing exactly what the algebra says: the generator becomes anti-Hermitian, so the only residual is truncation.
- **Adding the $h^2$ term** converts $1/n$ into $1/n^3$, reaching **$1.3\times10^{-12}$ — the machine gate — at $n_\text{sub}=32$.**
- At the shipped default $n_\text{sub}=4$: **$4.18\times10^{-2}\to6.66\times10^{-10}$, a factor of $6.3\times10^{7}$.**

## Result 2 — global order: **0.00 → 2.00**

Self-convergence against $n_\text{sub}=512$:

| scheme | errors at $n_\text{sub}=2,4,8,16$ | measured orders |
|---|---|---|
| pre-F276 (asymmetric, 1st) | 2.42e-2, 2.41e-2, 2.41e-2, 2.41e-2 | **0.00, 0.00, 0.00** |
| **F276 (Weyl, 2nd)** | 9.93e-6, 2.48e-6, 6.20e-7, 1.55e-7 | **2.00, 2.00, 2.00** |

**This is the more serious half of the finding.** The pre-F276 scheme has global order **zero**: sub-stepping did not reduce its solution error *at all*. It converged, but to the wrong operator — a fixed $\approx2.4\times10^{-2}$ (in this configuration) offset that no refinement removes. A user increasing `n_sub` to "improve accuracy" was paying linearly in cost for nothing.

## Result 3 — what moved, and what did not

- **`casim.verify.run_all()` — 14/14 PASS, unchanged.** The `refraction_2d` kernel-fidelity check is `residual = 0.0` **exactly**: the engine channel (`core.tier3`) and the kernel both call `weyl_step_2d_varc_strang`, so they moved together and their bit-for-bit agreement is preserved.
- **Zero committed baselines move.** The only test records reaching this stepper are three `legacy_script` records (`fork-B-fresnel`, `run-L192-tests`, `run-phase-tests`), none of which declares a result artifact; `scenarios/refraction_2d.yaml`'s output is not committed. `F244-emqg-1overb-scan` uses `CayleyVarcSolver2D`, not this path, and reproduced HEAD exactly.
- **`scenarios/refraction_2d` norm drift: $9.15\times10^{-2}\to6.80\times10^{-7}$** at its shipped settings.
- The superseded scheme stays measurable: `ordering='asymmetric'`, `order=1` reproduce it (to $1.9\times10^{-11}$ on smooth fields — the Nyquist zeroing of (iii) is not switchable, by design). This is the project's standing practice of keeping a falsified alternative computable next to the adopted one.

## Result 4 — a defect in the *measurement*, found on the way

`curved.measure_refraction`'s outgoing-angle diagnostic returns $\theta_\text{out}\approx165°$ against $\theta_\text{out}^\text{pred}\approx13°$ — **and does so under every stepper, including `method='cayley'`, which is exactly unitary by construction** ($\approx172°$). A quantity equally wrong under an exact stepper is not measuring the stepper.

The cause is geometric: the lattice is **periodic**, the packet wraps and re-enters, and the late-time right-region centroid mixes transmitted, reflected and wrapped amplitude, so `arctan2` of a backward-drifting centroid lands near $180°$.

**Consequence for the record.** Nothing in the test registry asserts these angles — the only callers are two `legacy_script` runners — so no published claim *rests* on it. **But no published claim is *supported* by it either.** The statement "the construction that already reproduces Snell's law in this codebase" (F271, and now several docstrings) is **not backed by a measurement in the tree**. A quantitative Snell confrontation needs open/absorbing boundaries and a transmitted-component projection, and is unbuilt. Recorded as an open item, not repaired here.

## What this does and does not change

**Does:** every future F64-fork variable-$c$ run is unitary to $O(h^3)$ with a convergent error and a genuinely second-order scheme.

**Does not:** it does not retroactively correct any published F64-fork number, because none was re-run here and none has a committed baseline. What it does establish is the size of the doubt that hung over them — a fixed $\sim2\times10^{-2}$ solution error and a $\sim6\times10^{-2}$ norm violation, neither removable by refinement, neither reported by any F64-fork result. **Any F64-fork variable-$c$ number quoted from before 2026-08-01 should be re-run before it is used quantitatively.**

## Falsification handle

If the Weyl-symmetric generator is the right one, its norm error must fall as $1/n_\text{sub}^3$ *and* the global order must be exactly 2 — both are sharp, and both are measured above. A measured order of 1, or a norm error that plateaus at any level above the machine gate, falsifies the construction.

## Artifacts

- `src/casim/engine/lattice/curved.py` — `_kgrid_2d`, `_sigma_grad_2d`, `_W_dH`, `_half_step_dH`, `weyl_step_2d_varc_strang`
- `docs/audits/physics-audit-report-2026-08-01.md` §V-014, §F276
