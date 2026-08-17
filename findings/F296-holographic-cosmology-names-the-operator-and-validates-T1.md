# F296 — F295's structure has a published home: **holographic cosmology** computes $n_s-1$ from a 3D QFT with no inflaton, and it delivers four things — (i) **F286 T1 is validated by retrodiction**, flagging HC's own fitted spectrum at $0.675$ against its $0.32$ bound (2.1× over) and implying $dn_s/d\ln k=+0.015$, a **2.9σ** tension that matches the published 2.2σ disfavour, from a bound built with no knowledge of HC; (ii) the model sits in the $f_1=0$ **conformal** branch the PRL's own footnote 2 says is **unanalysed**; (iii) the operator F295 could not name **is named** — the trace of the 3D stress tensor $T^i{}_i$; (iv) but the model's own field content read as that dual gives $r=0.32$–$0.97$ against BK18's $r<0.036$, **excluded by 9–27×**

**Date:** 2026-08-02 - 21:00
**Status:** **Literature placement + a validated instrument + a named operator + a decisive negative on the naive reading.** 7/7 checks PASS. L2 (the retrodiction) is **computed** from the published fit and is the load-bearing result; L3 is a **citation**; L4 is an **external identification**; L5 is **computed** from the model's own field content against BK18.
**Module:** `src/casim/engine/interactions/cosmology_holographic.py`
**Registry record:** `F296-holographic-anomalous-dimension` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F296_holographic.json`
**Reference summary:** `references/holographic-cosmology-summary.md`
**Answers:** [[F295-tilt-is-an-anomalous-dimension-not-a-second-scale]] §7's last row — *"which operator carries $\gamma$"* — with a candidate from an established framework, and then shows the naive application of it to this model fails.
**Validates:** [[F286-second-scale-must-be-a-log-not-a-length]] T1, on an independent published case it was not constructed from.
**Cross-references:** [[F295-tilt-is-an-anomalous-dimension-not-a-second-scale]] (the structure being placed), [[F286-second-scale-must-be-a-log-not-a-length]] (T1, the instrument under test), [[F285-initial-condition-measure-cannot-tilt]] (the Poisson bridge and the fixed-mode-set argument), [[F284-rigid-lattice-expansion-and-primordial-state]] (the rigid 3D substrate that makes a 3D-dual reading natural at all), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (no inflaton — the property HC shares), [[F47-majorana-seesaw-higgs-free]] ($\nu_R$, which sets $N_\psi=48$), [[F27-complex-mass-chiral-su2]] (Higgs-free, which is why $N_\Phi$ is only the $E_g$ doublet), [[F130-blockspin-rg-gauge-gravity]] (the lattice RG the PRL's closing suggestion would need). External: McFadden & Skenderis, PRD **81** 021301 (2010), arXiv:0907.5542; Afshordi, Corianò, Delle Rose, Gould & Skenderis, PRL **118** 041301 (2017), arXiv:1607.04878; Afshordi, Gould & Skenderis, PRD **95** 123505 (2017), arXiv:1703.05385; Planck 2018 X; BICEP/Keck BK18 ($r_{0.05}<0.036$, 95% CL).

Raised by Ben, 2026-08-02: *"do some research online about the problem and attempt to determine its source."*

---

## 1. The structure is not idiosyncratic

F295 concluded, from the model's own internals, that the primordial tilt is an **anomalous dimension** — a scale-free number attached to an operator, needing no inflaton and no second scale. That is precisely the defining structure of **holographic cosmology**, a programme running since 2009 and fitted to Planck in 2017:

$$\Delta^2_R(q)=-\frac{q^3}{4\pi^2}\,\frac{1}{\operatorname{Im}\langle\langle T(q)T(-q)\rangle\rangle},\qquad \Delta^2_R(q)=\frac{\Delta^2_0}{1+(gq_*/q)\ln|q/\beta gq_*|+O((gq_*/q)^2)}$$

computed from a **three-dimensional QFT with no gravity and no inflaton**. Afshordi et al find it *competitive* with ΛCDM: disfavoured 2.2σ globally, but within 1σ once $\ell<30$ is dropped, where the dual goes non-perturbative.

This matters for the register in a specific way: F282–F295 built, step by step, a position that sounded exotic — no inflaton, a spectrum fixed in the initial state, a tilt that is a pure scaling dimension. **It is a position with a decade of published literature and a Planck fit.** That does not make it right; it makes it *the kind of thing that can be tested*, and it supplies vocabulary the register did not have.

## 2. L2 — F286 T1 retrodicts holographic cosmology's published problem

This is the load-bearing result, and it is a test of *our* instrument rather than of HC.

HC's dual is **super-renormalizable**, so its 't Hooft coupling $g^2_\text{eff}=g^2_{YM}N/q$ is **dimensionful** and runs as $1/q$ — a power, $p=-1$. F286 T1 bounds the tilt's log-derivative at $0.32$ using Planck's *running*. Evaluating T1's diagnostic on HC's **own fitted spectrum** ($g=-0.00703$, $\ln\beta=0.877$, Table I, all-$\ell$):

| Quantity | Value |
|---|---:|
| $n_s-1$ from HC at its fitted point | $-0.0223$ |
| $\lvert d\ln F/d\ln x\rvert$ (T1's diagnostic) | $\mathbf{0.675}$ |
| T1's bound | $0.32$ |
| Over the bound by | $\mathbf{2.11\times}$ |
| Implied $dn_s/d\ln k$ | $+0.0151$ |
| vs Planck $-0.0045\pm0.0067$ | $\mathbf{2.92\sigma}$ |
| Published global disfavour (Afshordi et al) | $2.2\sigma$ |

**T1 flags HC, quantitatively, and lands on the published number.** T1 was built in F286 from Planck's running alone, with no knowledge of holographic cosmology; recovering an independent group's $\chi^2$ result from it is the difference between a private construction and a usable instrument. Every downstream use of T1 in this register — including the length-scale exclusion that closed F285 falsifier 1 — inherits that credibility.

## 3. L3 — the model sits in the branch the literature explicitly leaves open

A constant $\gamma$ (F295) requires $p=0$, i.e. a **dimensionless** coupling — a **conformal** dual, not a super-renormalizable one. In HC's own notation that is the case $f_1=0$, and the PRL's footnote 2 reads verbatim:

> *"This assumes $f_1\ne0$. A separate analysis is required, where $f_1=0$."*

So the branch the model's structure points at is an **acknowledged gap in the published work**, not a re-tread of it. That is a genuinely useful place to be: the two sub-classes F295 §3 identified — constant-$\gamma$ vs log-type — map exactly onto CFT-dual vs super-renormalizable-dual, and the data currently prefers the first (Planck's running is consistent with zero; HC's $+0.015$ is 2.9σ off).

## 4. L4 — the operator F295 could not name

F295 §7's last row was *"which operator sets the initial amplitude, and what is its anomalous dimension"*. Holographic cosmology answers it:

> **The trace of the three-dimensional stress tensor, $T^i{}_i$.** Its two-point function *is* the primordial spectrum, and $\gamma$ is its anomalous dimension. The required value is $\gamma=\tfrac12(1-n_s)=0.01755$.

This is an *external* identification: it says what kind of object would carry $\gamma$ in a framework where this structure is worked out. It does **not** establish that this model has such a dual — and §5 shows the obvious way of asserting it fails.

## 5. L5 — but the model's own field content, read as the dual, is excluded by $r$

HC gives the tensor-to-scalar ratio in closed form from the dual's field content:

$$r=\frac{32\left(1+\sum_M(1-8\xi_M)^2\right)}{1+2N_\psi+N_\Phi}.$$

Feeding in **the model's own content** — $N_\psi=48$ Weyl fermions (3 generations × 16, including $\nu_R$ per F47) and $N_\Phi=2$ real scalars (the $E_g$ doublet; the model is Higgs-free by F27):

| Scalar coupling | $r$ | vs BK18 $r<0.036$ |
|---|---:|---:|
| Conformal, $\xi=1/8$ | $0.323$ | **9.0× over** |
| Minimal, $\xi=0$ | $0.970$ | **26.9× over** |

Reaching the bound would need $N_\Phi>792$ scalars. **The model has 2.**

This is the same failure the PRL reports independently — *"the data rules out the dual theory being Yang-Mills theory coupled to fermions only, but allows for Yang-Mills theory coupled to non-minimal scalars with quartic interactions"* — and this model is fermion-dominated by construction, precisely because it is Higgs-free.

> **The naive holographic reading of this model is excluded, and it is excluded by the model's own field content rather than by a fit.** That is worth as much as the placement in §1: it means the correspondence, if there is one, cannot be the obvious "the model's fields *are* the dual's fields".

## 6. Verdict

> **The source of the structure is holographic cosmology**, where $n_s-1$ has been computed as a QFT anomalous dimension with no inflaton for over a decade and fitted to Planck. Four things follow. **F286 T1 is validated**: applied to HC's own fitted spectrum it returns $0.675$ against its $0.32$ bound and a $2.9\sigma$ running tension, recovering the published $2.2\sigma$ disfavour from a bound built without reference to it. **The model's branch is the $f_1=0$ conformal one**, which the PRL's footnote 2 states is unanalysed — an opening, not a re-tread. **The operator is named**: the trace of the 3D stress tensor. **And the naive reading is dead**: the model's own 48 Weyl fermions and 2 scalars give $r=0.32$–$0.97$ against $r<0.036$, over by 9–27×, matching the PRL's independent exclusion of fermion-only duals.

**What this does to the open question.** F295 left *"which operator?"* as a search. It is now a named candidate with a named obstruction: the operator is $T^i{}_i$ of a 3D CFT, the branch is unanalysed in the literature, and any correspondence cannot map the model's fields onto the dual's fields directly. That is three constraints where there were none.

## 7. Falsifiers

1. **A worked $f_1=0$ (CFT-dual) holographic analysis giving $\gamma\ne0.01755$.** Would close the branch §3 opened. This is the single highest-value external calculation.
2. **A demonstration that this model admits no 3D dual at all.** Would make §4's identification irrelevant and return F295's question to a search.
3. **A dual field content for this model that is not its own field content.** §5 excludes the naive map; a non-naive one (composite operators, a coarse-grained effective content) would need to be exhibited, not asserted.
4. **A measured $dn_s/d\ln k\approx+0.015$.** Would favour HC's super-renormalizable branch over the model's constant-$\gamma$ one, inverting §3.
5. **$r$ detected above $0.036$.** Would relax §5's exclusion — though BK18 is already at $r_{0.05}<0.036$ and BICEP Array targets $\sigma(r)\lesssim0.003$.

## 8. What is exact vs computed vs open

| Piece | Status |
|---|---|
| HC computes $n_s-1$ from a 3D QFT with no inflaton; fitted to Planck | **external, cited** |
| T1 diagnostic on HC's fitted spectrum $=0.675$ vs bound $0.32$ | **computed** from the published $g$, $\ln\beta$ |
| Implied $dn_s/d\ln k=+0.0151$; $2.92\sigma$ from Planck | **computed** |
| Agreement with the published $2.2\sigma$ global disfavour | **retrodiction** |
| Model's branch is $f_1=0$; literature does not analyse it | **citation** (PRL footnote 2) |
| Operator $=T^i{}_i$, 3D stress-tensor trace | **external identification**, not a derivation here |
| $r=0.323$ (conformal) / $0.970$ (minimal) on the model's content | **computed** |
| Excluded by BK18 at 9.0×/26.9×; needs $N_\Phi>792$ | **computed** |
| **Whether this model has a 3D dual at all** | **open** |
| **The $f_1=0$ anomalous dimension** | **open — and now a named external calculation** |

## 9. Honest scope

L2 is the result worth keeping and the only one that is properly *ours*: it tests F286's instrument against a case it was not built from, and it passes. Its one soft spot is that HC's tilt is evaluated at the pivot with a two-parameter fit rather than re-run through CosmoMC, so the $2.92\sigma$ should be read as "the right size and sign", not as a replacement for the published likelihood — which is why the published $2.2\sigma$ is quoted beside it rather than instead of it. L3 and L4 are citation and identification, not physics done here, and are labelled as such throughout; it would be easy and wrong to present a named operator as a derived one. L5 is computed and decisive but rests on reading the model's field content as the dual's, which is the *naive* map — its exclusion constrains that map, not every conceivable correspondence. What this finding does **not** do is establish that the model is holographic; §8's last two rows are the whole remaining problem, and the second of them is now a specific calculation someone could do.

## 10. Files
- Module: `src/casim/engine/interactions/cosmology_holographic.py`
- Test: `tests/findings/test_F296_holographic.py`
- Results: `test-results/F296_holographic.json`
- Reference summary: `references/holographic-cosmology-summary.md`
