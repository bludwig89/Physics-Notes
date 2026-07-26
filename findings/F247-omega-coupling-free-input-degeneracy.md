# F247 — The absolute ω-NN coupling is a genuine free input: universality overshoot + deuteron core/ω degeneracy (Q3)

**Date:** 2026-07-15 - 19:25
**Status:** Confirmed — closes open-derivation **Q3** (`open-derivations-prompts-v2.md` Part 3) on the **documented-free-input** branch of its acceptance. The absolute $g_{\omega NN}$ is **not** derivable at the static-OBE level, for two independent, quantified reasons: (1) the vector-universality chain overshoots by the known empirical $g_{\rho NN}$-universality violation, and (2) the deuteron constrains only the *total* short-range repulsion, so $g_{\omega NN}$ is degenerate with the F113 quark-Pauli core strength along a near-linear valley. Both are demonstrated numerically. Also **corrects** F240's "$0.43\approx0.45$ common-dressing" remark: the physical (derived-core) quench is $0.21$, and the $0.43$ figure was a core-off (route B) artifact.
**Modules:** `ca-simulation/ca_nuclear.py` (reused, not modified); `ca-simulation/run_Q3_omega_degeneracy.py` (new runner)
**Results:** `test-results/Q3_omega_degeneracy.json`
**Cross-refs:** [[F240-omega-coupling-from-vector-sector]] (derived the ω sign/mass/×3 ratio + the $25.9$ universality ceiling; this finding resolves its open "absolute $g_\omega$" item as a free input and corrects its D1 quench remark), [[F128-nn-short-range-omega-repulsion]] (ω channel + sign), [[F126-nn-intermediate-range-sigma-attraction]] (bare σ, the "0.45 quench"), [[F113-nn-short-range-repulsive-core]] (the quark-Pauli core, $g_{cm}$ from N–Δ), [[F104-p4-deuteron-tensor-bound-nucleus]] (the deuteron solver)

---

## What was open

F240 derived the ω channel's **sign** (repulsive), **mass** ($m_\omega=m_\rho$), and **ratio** $g_{\omega NN}=3g_{\rho NN}$ (all Tier-1), and the vector-dominance chain

$$g_{\rho\pi\pi}=\frac{m_\rho}{\sqrt2 f_\pi}=6.01\ \xrightarrow{\text{univ.}}\ g_{\rho NN}=g_{\rho\pi\pi}\ \xrightarrow{\times3}\ \frac{g_{\omega NN}^2}{4\pi}\bigg|_\text{univ}=25.9$$

**overshoots** — fed to the deuteron solver it unbinds the deuteron. The NN-required value was left a Tier-B bracket $[5.4,11.1]$. Q3 asked to derive the $\approx0.43$ channel-dressing factor and pin $g_{\omega NN}$, **or** document why it is a genuine free input.

## Result — free input, for two independent reasons

### 1. The overshoot IS the empirical $g_{\rho NN}$-universality violation

The whole overshoot lives in the one flagged posit $g_{\rho NN}=g_{\rho\pi\pi}$. Undoing the $\times3$ coherence, the deuteron-consistent value (route A, below) is

$$\frac{g_{\rho NN}^2}{4\pi}=\frac{5.39}{9}=0.60,$$

which sits **squarely in the empirical band** $g_{\rho NN}^2/4\pi\approx0.5\text{–}0.95$ (CD-Bonn/Bonn OBE), while strict universality's $g_{\rho\pi\pi}^2/4\pi=2.88$ is $\sim3\times$ too large. This is exactly the long-standing, unresolved **$\rho$-universality violation** of real nuclear physics: the ρ (and hence ω) couples to the *nucleon* far more weakly than universality predicts. The model faithfully **reproduces the known overshoot**; pinning the reduction is equivalent to computing the meson–nucleon vertex renormalization $g_{\rho qq}\to g_{\rho NN}$ (a wavefunction/form-factor overlap distinguishing the quark-current vertex from the pion-current $g_{\rho\pi\pi}$), which a **static point-OBE structurally cannot contain**.

### 2. The deuteron cannot separate ω from the F113 core (degeneracy)

The short-range repulsion is supplied by **both** the F113 quark-Pauli core (strength $g_{cm}$, calibrated to the N–Δ splitting) **and** the ω, with overlapping radial shapes. The deuteron fixes only their **sum**. Mapping the coupling $g_{\omega NN}^2/4\pi$ that binds the deuteron to $E_b=2.224$ MeV as a function of the core strength gives a **near-linear valley** (`run_Q3_omega_degeneracy.py`, $N=500$):

| $g_{cm}$ (MeV) | core / derived | $g_{\omega NN}^2/4\pi$ that binds | quench vs 25.9 |
|---|---|---|---|
| 0.00 | 0.00 | 11.15 | 0.431 |
| 9.15 | 0.50 | 8.26 | 0.319 |
| **18.31** | **1.00 (N–Δ derived)** | **5.39** | **0.208** |
| 27.47 | 1.50 | 2.56 | 0.099 |

$$g_{\omega NN}^2/4\pi\big|_\text{bind}=11.13-0.313\,g_{cm}\quad(\text{linear, residual }0.02).$$

So $g_{\omega NN}$ and $g_{cm}$ are **degenerate**: any core strength gives a deuteron-binding ω, tracing the F240 bracket $[5.4,11.1]$ (core-on → core-off) as a *slice of the valley*, not a genuine uncertainty on ω alone. **The ω coupling is not separately deuteron-observable.**

### 3. Route A prediction and correction to F240

At the physical, N–Δ-derived core ($g_{cm}=18.31$ MeV), the full derived OBE binds the deuteron cleanly, no tuned wall:

$$g_{\omega NN}^2/4\pi=5.39,\quad E_b=2.224\ \text{MeV},\quad r_d=1.96\ \text{fm},\quad P_D=6.3\%.$$

The quench here is $5.39/25.9=\mathbf{0.208}$ — **not** the $0.43$ F240's check D1 advertised. The $0.43$ arises only with the F113 core switched **off** (route B), where ω must carry the *entire* short-range repulsion; that is not the physical configuration. Hence F240's "vector quench $0.43\approx$ scalar quench $0.45$ common dressing" is a **core-off artifact** — at the physical point the vector quench ($0.21$) and F126's scalar quench ($0.45$) are *not* equal, so there is no evidence for a single common dressing factor.

## Verification

`run_Q3_omega_degeneracy.py` (real-space coupled ${}^3S_1$–${}^3D_1$ solver, all-real arithmetic — no chiral/complex transforms, so the CLAUDE.md numpy caveat does not bite) reproduces F240's route A ($g_\omega^2/4\pi=5.39\to E_b=2.224$, $r_d=1.96$), maps the degeneracy valley, and dumps `test-results/Q3_omega_degeneracy.json`. Runtime ~1–2 min; the runner is the user-runnable fallback if the sandbox times out.

## Exactness tier

- Tier-1 (unchanged, F240): ω sign, $m_\omega=m_\rho$, $g_{\omega NN}=3g_{\rho NN}$, universality ceiling $25.9$.
- **Free input (this finding):** absolute $g_{\omega NN}$ — degenerate with the F113 core (linear valley, residual $0.02$) and set by an OBE-inaccessible vertex renormalization. Deuteron-consistent $g_{\rho NN}^2/4\pi=0.60\in$ empirical $[0.5,0.95]$.

## What this closes / leaves open

- **Closes Q3** on the documented-free-input branch: $g_{\omega NN}$ is a genuine free parameter at the static-OBE level (two independent reasons), parallel to the way real OBE potentials *fit* $g_{\omega NN}$. The ω channel's derivable content (sign, mass, ×3 ratio) stands.
- **Corrects F240 D1**: no single $\approx0.43$ common scalar/vector dressing; the physical vector quench is $0.21$.
- **Open (unchanged, deeper):** a dynamical meson–nucleon vertex (the $g_{\rho qq}$ vs $g_{\rho\pi\pi}$ overlap) from the model's nucleon structure would pin the reduction — the same computation that would resolve the empirical ρ-universality violation. Not attemptable in the static OBE.
