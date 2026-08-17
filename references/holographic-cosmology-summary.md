# Holographic cosmology — research summary

**Created:** 2026-08-02 - 21:10
**Why it is here:** F295 derived, from this model's own structure, that the primordial tilt is an **anomalous dimension** needing no inflaton and no second scale. Holographic cosmology is the established framework with exactly that structure, and it has been fitted to Planck. This summary is the external material [[F296-holographic-cosmology-names-the-operator-and-validates-T1]] rests on.

## Primary sources

| Ref | What it supplies |
|---|---|
| McFadden & Skenderis, PRD **81** 021301 (2010), [arXiv:0907.5542](https://arxiv.org/abs/0907.5542) | The original holographic-cosmology construction: cosmological observables from a 3D QFT |
| Afshordi, Corianò, Delle Rose, Gould & Skenderis, PRL **118** 041301 (2017), [arXiv:1607.04878](https://arxiv.org/abs/1607.04878) | The Planck fit, the 2-loop coefficients, the $r$ formula, and the model-selection results. **The paper F296 uses.** |
| Afshordi, Gould & Skenderis, PRD **95** 123505 (2017), [arXiv:1703.05385](https://arxiv.org/abs/1703.05385) | The longer companion analysis |

## The construction

The dual is an $SU(N)$ gauge theory in **three** dimensions coupled to scalars $\Phi^M$ and fermions $\psi^L$:

$$S=\frac1{g^2_{YM}}\int d^3x\,\mathrm{tr}\Big[\tfrac12F_{ij}F^{ij}+(D\Phi)^2+2\bar\psi\!\!\not\!D\psi+2\sqrt2\,\mu\cdot(\Phi\bar\psi\psi)+\tfrac16\lambda\cdot\Phi^4\Big]$$

The holographic dictionary maps the primordial spectrum to the **two-point function of the trace of the stress tensor**:

$$\Delta^2_R(q)=-\frac{q^3}{4\pi^2}\frac1{\operatorname{Im}\langle\langle T(q)T(-q)\rangle\rangle}=\frac1{4\pi^2N^2f(g^2_\text{eff})},\qquad g^2_\text{eff}(q)\equiv\frac{g^2_{YM}N}{q}$$

with, perturbatively,

$$f(g^2_\text{eff})=f_0\big[1-f_1g^2_\text{eff}\ln g^2_\text{eff}+f_2g^2_\text{eff}+O(g^4_\text{eff})\big]$$

giving the universal spectrum

$$\Delta^2_R(q)=\frac{\Delta^2_0}{1+(gq_*/q)\ln|q/\beta gq_*|+O((gq_*/q)^2)}.$$

**The key structural fact for this project:** in 3D a super-renormalizable gauge coupling has **mass dimension 1**, so $g^2_\text{eff}\propto1/q$ — the effective coupling is a *power* in $q$, not a log. That is what puts HC in F286's excluded shape class (see below).

## Numbers used by F296

| Quantity | Value | Source |
|---|---|---|
| Fitted $g$ (all $\ell$) | $-0.00703^{+0.00105}_{-0.00167}$ | Table I |
| Fitted $\ln\beta$ (all $\ell$) | $0.877^{+0.186}_{-0.239}$ | Table I |
| Fitted $g$ ($\ell\ge30$) | $-0.01305$ | Table I |
| $\chi^2$ penalty vs ΛCDM-with-running, all $\ell$ | HC disfavoured **2.2σ** | text |
| $\chi^2$, $\ell\ge30$ | all three models within 1σ | Table I |
| Tensor-to-scalar ratio | $r=\dfrac{32\left(1+\sum_M(1-8\xi_M)^2\right)}{1+2N_\psi+N_\Phi}$ | Eq. (10) |
| Their $r$ bound | $r\le0.125$ (2σ, their fit) | text |
| Current external bound | $r_{0.05}<0.036$ (95% CL, BK18) | BICEP/Keck |

## The three statements F296 leans on

1. **The spectrum comes from $\langle TT\rangle$** — this is what names the operator F295 could not.
2. **Footnote 2, verbatim:** *"This assumes $f_1\ne0$. A separate analysis is required, where $f_1=0$."* The $f_1=0$ case is the **conformal / dimensionless-coupling** branch, which is where a *constant* anomalous dimension lives — i.e. this model's branch, and it is unanalysed.
3. **Model selection:** *"the data rules out the dual theory being Yang-Mills theory coupled to fermions only, but allows for Yang-Mills theory coupled to non-minimal scalars with quartic interactions."* Their viable example needs $N=2995$, $N_\Phi=23255$.

## What this framework already excludes, that matters here

- **Fermion-dominated duals.** With $N_\Phi\to0$, $r\to32/(1+2N_\psi)$, which needs $N_\psi\gtrsim128$ merely to reach their $r<0.125$, and $\gtrsim444$ to reach BK18's $0.036$. A Higgs-free, fermion-dominated content — which is what this model is (F27) — fails. F296 L5 computes this on the model's own 48 Weyl fermions and 2 $E_g$ scalars: $r=0.32$–$0.97$, over by 9–27×.
- **Low multipoles.** Below $\ell\sim30$ the dual is non-perturbative and the 2-loop prediction cannot be trusted; below $\ell\sim10$ the 2-loop term equals the 1-loop one. Any comparison must be restricted to $\ell\gtrsim35$.

## The convergence worth flagging

The PRL's closing sentence: *"non-perturbative methods (such as putting the dual QFT on a lattice) can be used to reliably model the very low multipoles, which may potentially explain the apparent large angle anomalies in the CMB sky."*

This model **is** a 3D lattice, and F284 established that its $t=0$ state is specified on that 3D lattice globally. Whether the model's spatial initial state could *be* the 3D Euclidean theory such a lattice computation would target is speculative and is recorded here as a direction, **not** as a claim — F296 L5 already shows the naive field-content map fails.

## How this relates to the register

| Register item | Relation |
|---|---|
| F282 (no inflaton) | HC shares the property; it is not a defect unique to this model |
| F285 D3 (line of fixed points) | the exponent as a free marginal label = the anomalous dimension |
| F286 T1 (shape bound) | **validated** by retrodicting HC's tension: $0.675$ vs $0.32$, $2.9\sigma$ running |
| F295 (constant $\gamma$) | the $f_1=0$ branch; unanalysed in the literature |
| F296 | this summary's finding |
