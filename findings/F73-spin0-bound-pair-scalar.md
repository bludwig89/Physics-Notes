# F73 — The spin-0 bound-pair scalar: the "Cooper-pair" Higgs candidate, and the exact lattice mass it predicts

**Date:** 2026-06-01 - 17:42
**Status:** Partial — the **kinematics are exact and derived** (BP1/BP2/BP4 algebraic; BP3/BP5 quantitative; 6/6 checks PASS, residuals ≤ $4\times10^{-51}$). The **mass value is not yet predicted**: the missing input is the binding dynamics (the SM quartic $\lambda$ in disguise). The model predicts only the kinematic ceiling and a sharp falsifiable structure; a candidate scale match ($m_H\!\approx\!v/2$) is **flagged, not derived**.
**Script:** `model-tests/test_F73_spin0_bound_pair.py` (<1 s)
**Results:** `test-results/F73_spin0_bound_pair.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the spin-1 partner of this pairing), [[F46-pythagorean-lattice-mass]] ($\Omega_\text{rest}=\arcsin m$), [[F27-complex-mass-chiral-su2]] (the chiral mass rotation), [[F44-higgs-free-mA-zero-from-rank1-stueckelberg]] (Stueckelberg scale $f=v/2$), [[F34b-wmu-mass-stueckelberg]]; McPhee notebook `reference-research/physics-notes-complete.md` pp.5–6 (items 2/3/6: "the Higgs is the Cooper pair, we presume"), p.62 ("Weinberg–Salam w/o Higgs").

---

## The question

The model is Higgs-free in the **Stueckelberg / non-linear-σ sense** (F27/F34b/F44): the field $U(x)$ supplies the Goldstone/VEV direction (pure gauge, scale $f=v/2$), the would-be Goldstones are eaten to make $W$/$Z$ massive, and the **radial (breathing) mode** — the physical 125 GeV scalar — is removed. So *as built the model contains no particle matching the Higgs boson.* That is a standing obligation, not a neutral fact: the LHC observed a 125 GeV scalar.

The notebook already proposes the resolution route (pp.5–6, items 2/3/6): symmetry breaking is superconductor-like, *"two electrons pair up to create a single Cooper pair, a spin-0 state… The Higgs is the Cooper pair, we presume."* This finding builds that out and asks the sharp question: **does the model's own pairing kinematics predict the scalar's mass?**

## The construction — the spin-0 partner of the F69 photon

Two spin-½ constituents combine as $\tfrac12\otimes\tfrac12=0\oplus1$. F69 built the **symmetric spin-1** combination as the electromagnetic photon (a bound $(+,-)$ pair, "only occurs as a pair," phase per tick = constituent sum). The **antisymmetric spin-0 singlet** of the *same* pairing is the natural Higgs/Cooper-pair channel — spin-singlet, symmetric $s$-wave spatial, exactly the BCS Cooper-pair quantum numbers.

The mass then follows from two results already in the model, with **no new dynamical assumption**:

- **F46:** a state of dimensionless lattice mass $m$ rotates at rest-frame rate $\Omega_\text{rest}(m)=\arcsin m$, i.e. $m=\sin\Omega_\text{rest}$.
- **F69:** a bound pair's phase per tick is the **sum** of the constituent phases.

So a spin-0 bound pair of constituents with lattice masses $m_1,m_2$ has rest rotation

$$\Omega_H=\arcsin m_1+\arcsin m_2,$$

and therefore composite lattice mass (sine addition, **exact**)

$$\boxed{\,m_H=\sin\!\big(\arcsin m_1+\arcsin m_2\big)=m_1\sqrt{1-m_2^{2}}+m_2\sqrt{1-m_1^{2}}\,}$$

Equal constituents $m_1=m_2=m_c$:

$$m_H=\sin\!\big(2\arcsin m_c\big)=2\,m_c\sqrt{1-m_c^{2}}.$$

Verified to $\le 4\times10^{-51}$ over a grid of constituent masses (BP1, BP2 — exact-algebraic).

## What the kinematics predict

**1. A built-in binding deficit (lattice is sub-additive).** The Euclidean "free" sum of two rest masses would be $m_1+m_2$. The lattice (spherical) composite is strictly **below** it:

$$m_H=\sin(\arcsin m_1+\arcsin m_2)\le m_1+m_2,$$

with equal-mass deficit fraction $1-\sqrt{1-m_c^{2}}\approx m_c^{2}/2$ (BP3). This is McPhee's "negative binding energy" (notebook #5) made quantitative: the binding is automatic and geometric, not put in by hand.

**2. A stability/saturation bound.** $\Omega_H=2\arcsin m_c$ reaches $\pi/2$ (maximum lattice mass $m_H=1$) at $m_c=1/\sqrt2$; beyond that the rotation over-wraps. A stable composite therefore requires $m_c\le 1/\sqrt2$, and the composite mass saturates at $m_H=1$ (BP4, exact). Trivially satisfied at electroweak scales.

**3. At the G-matched cell size the deficit is unobservable.** With $a\approx6.2\times10^{-35}$ m (F64/D-EM10) every EW-scale mass has $m_\text{lat}=m_\text{phys}ca/\hbar\ll1$: $m_\text{lat}(\text{top})\approx5.4\times10^{-17}$, $m_\text{lat}(125\text{ GeV})\approx3.9\times10^{-17}$, so the deficit fraction is $\sim m_\text{lat}^2/2\approx1.5\times10^{-33}$ (BP5). **The SI prediction therefore collapses to the free sum:**

$$m_H\simeq m_1+m_2\quad(\text{to }\sim33\text{ decimals at EW scale}).$$

## Confrontation with the observed 125.25 GeV — honest verdict

The free-sum kinematics alone **cannot** reproduce 125.25 GeV (BP6):

| identification | constituents | predicted $m_H$ | verdict |
|---|---|---|---|
| equal at threshold | $m_c=m_H/2$ | input $\Rightarrow m_c=62.6$ GeV | **no SM fermion** at this mass (between $b$ and $W$) |
| top-condensate (Nambu) $t\bar t$ | $m_c=m_t=172.6$ GeV | $2m_t=345.1$ GeV | **overshoots**; needs $219.9$ GeV ($63.7\%$) binding |

So a near-threshold "molecule" of known fermions does not land on 125 GeV. **The conclusion is structural: the missing input is genuine binding dynamics** — the depth $E_b=(m_1+m_2)-m_H$ that the kinematic deficit (negligible here) does not supply. That binding depth is precisely the role the SM Higgs quartic $\lambda$ plays. The model, in its current minimal form, predicts the **kinematic ceiling** ($m_H\le m_1+m_2$, strictly below on the lattice) and the **channel** (spin-0 singlet of the same pairing as the photon, tied to the condensate scale), but **not the value** of $m_H$.

## Flagged, NOT derived — the $m_H\approx v/2$ coincidence

The model's natural scale for a scalar in the symmetry-breaking channel is the Stueckelberg scale $f=v/2=123.1$ GeV (F44). Numerically,

$$\frac{m_H^\text{obs}}{v/2}=\frac{125.25}{123.11}=1.017\quad(1.7\%),$$

equivalently, $m_H=v/2$ is the statement that the quartic is $\lambda=\tfrac18=0.125$, versus the observed $\lambda=m_H^2/2v^2=0.1294$ (a $3\%$ gap). This is **recorded as a numerical coincidence, not a derivation** — there is no argument in the model yet that fixes the coefficient to exactly 1 (it is the strong-coupling/techni-dilaton expectation that the scalar sits at the condensate scale). It is logged here as the obvious target a binding-scale derivation must hit or miss.

## What this buys, and what remains

- **Buys:** Ludwig's conjecture is now a defined, falsifiable object with exact kinematics — the spin-0 singlet partner of the F69 photon, with an exact composite-mass law, a built-in geometric binding deficit, and a stability bound. The 125 GeV scalar is no longer simply absent from the theory; it has a candidate identity and a sharp confrontation.
- **Remains (the real physics):** a two-constituent **bound-state simulation** with an actual interaction (the deep follow-up flagged in F69) to produce the binding depth $E_b$ and hence $m_H$ — i.e. to derive $\lambda$. Until then the value is an input, and the $m_H\approx v/2$ / $\lambda\approx1/8$ match is unproven.

## Files
- Script: `model-tests/test_F73_spin0_bound_pair.py`
- Results: `test-results/F73_spin0_bound_pair.json`
