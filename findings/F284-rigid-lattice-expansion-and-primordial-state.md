# F284 — On a rigid lattice, cosmic expansion is the conformal mode of $K$, not the substrate stretching: this predicts $\dot G/G\equiv0$ **exactly** (vs $2H_0$ for a comoving lattice), removes the trans-Planckian problem by construction, dissolves the horizon problem into the automaton's initial state, and replaces the initial singularity with a first resolvable epoch at $H_\text{max}=3^{-3/4}M_\text{Pl}$, $t_\text{min}=\sqrt3$ ticks

**Date:** 2026-08-02 - 14:20
**Status:** **Interpretive closure with one sharp prediction** — 6/6 checks PASS. The epoch scales ($H_\text{max}=3^{-3/4}M_\text{Pl}$, $t_\text{min}=1/c_\text{lat}=\sqrt3$ ticks) are **exact-algebraic**; the SI values and cell budget are **computed**; the identification of expansion with $K$'s homogeneous mode is **structural** (forced by F283's rigidity plus F64/F106/F178); the horizon/flatness discussion is **interpretive and labelled as such** in §6.
**Module:** `src/casim/engine/interactions/cosmology_lattice_elasticity.py` (shared with F283)
**Registry record:** `F283-elastic-lattice-excluded` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`) — one record covers both findings, they are one computation
**Results:** `test-results/F283_F284_lattice_elasticity.json`
**Theory doc:** `docs/theory/primordial-sector.md`
**Cross-references:** [[F283-elastic-lattice-excluded-and-f282-invariance]] (the premise: the lattice is rigid to $\sim0.1\%$), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (no inflaton — this explains *why that is survivable* and what pays for it), [[F64-em-connection-gravity]] / [[F106-psi-K-sourcing-derivation]] / [[F178-gravity-full-tensor-adoption]] (the dielectric $K$ that carries the expansion), [[F180-gravitational-wave-speed]] ($\ln K$'s wave equation), [[F182-friedmann-pressure-cosmology]] / [[F188-multicomponent-lcdm-cosmology]] (the FRW solutions this re-reads — **their numbers are unchanged**), [[F79-structural-newton-constant]] ($G$ structural, hence $\dot G/G\equiv0$ on a rigid lattice), [[F238-geon-relic-abundance]] (the free $\beta$ this recasts as one component of the initial state), [[F193-ontic-vacuum-gravitates-as-zero]] / [[F196-dilution-exponent-derived]] (the $\Lambda$ picture, which uses proper Hubble lengths and is untouched), [[F130-blockspin-rg-gauge-gravity]] (block-spin coarse-grains the *description*; the substrate does not move — the distinction this finding needs), [[F183-blackhole-under-full-tensor]] (the singularity that *is* inherited, in the emergent metric, contrasted with the substrate's). External: Planck 2018; Hofmann & Müller 2018; Brandenberger & Martin 2013 (trans-Planckian problem); Wetterich 2013 (the conformally-equivalent "shrinking matter" frame).

Raised by Ben, 2026-08-02: *"If F282 is the case, how does the model interpret the primordial universe and current universal expansion?"*

---

## 1. The question F282 and F283 force

F282 says the model has no inflaton. F283 says the lattice is rigid — elasticity is bounded at $q\lesssim10^{-3}$ by LLR and BBN, and the volume mode is not a new field but the dielectric $\ln K$ the model already owns. Together they leave a question that can no longer be deferred: **if the substrate does not stretch and there is no inflaton, what is the expanding universe?**

The answer is available and forced. It is not new physics; it is the only consistent reading of machinery already adopted. What is new is that it makes a **falsifiable prediction the model was not previously known to make**.

## 2. Expansion is the conformal mode of $K$ on a fixed substrate

The emergent metric is built from the lattice dielectric $K$ (F64, F106, promoted to the full induced Einstein equation by F178). $K$ is a **field on the lattice**; $a$ is a **property of the lattice**. F283 shows these cannot be conflated, and that only $K$ is dynamical.

So the FRW scale factor is $K$'s homogeneous mode. "Space expanding" means the emergent metric assigns growing proper distance to a **fixed** number of cells. Nothing about the substrate changes — not its spacing, not its cell count, not its coordination.

**This does not move a single number in F182/F188.** Those findings solve the Friedmann equations with the model's own source and reproduce ΛCDM ($z_\text{eq}\approx3430$, $z_\text{acc}\approx0.63$, age $\approx13.8$ Gyr). That is a statement about the emergent metric, which is exactly what is being re-read here. What changes is the *ontology*, and with it one observable.

### The prediction

$$\boxed{\ \dot G/G\equiv0\ \text{exactly},\qquad\text{where a comoving lattice gives }\dot G/G=2H_0=1.379\times10^{-10}\,\text{yr}^{-1}.\ }$$

Because F79 makes $G=a^2c^3/(8\pi\sqrt3\hbar)$ *structural*, a rigid $a$ means a rigid $G$ — not "small drift", but **exactly zero**, with no tuning and no free parameter. Most varying-constant frameworks predict a small nonzero drift whose size is a fitted parameter; this predicts the value zero for a structural reason. LLR already sits 3 orders inside it (Hofmann–Müller 2018: $\lvert\dot G/G\rvert<1.5\times10^{-13}\,\text{yr}^{-1}$), so **the data has already selected the rigid reading** — and any future detection of a nonzero $\dot G$ falsifies the model's gravity sector outright rather than merely constraining it.

## 3. Redshift, and where the energy goes

A comoving mode has a **fixed wavenumber in lattice units**, forever. Its rotation rate per tick, $\Omega=\lvert k\rvert/\sqrt3$ (F26, F105), therefore never changes. What changes is the conversion from lattice ticks to *proper* time, which is $K$. Cosmological redshift is thus a **gravitational/dielectric redshift accumulated along the path**, not a stretching of the wave against a stretching ruler.

This is the conformally-equivalent restatement of standard cosmology (cf. Wetterich's "shrinking matter" frame), so it is observationally identical to FRW by construction — which is the point: **the model does not need to pay anything for this reading.** It is the same physics with the substrate held still, and the only place the two readings differ is $\dot G$, §2.

## 4. No trans-Planckian problem — and the same fact forbids generating $P(k)$

On a rigid lattice a comoving mode's wavelength **in cells** is constant. Two consequences, and they are the same fact seen from two sides:

- **The good side.** No mode ever had a wavelength below $a$. The trans-Planckian problem — that modes observed today were sub-cutoff at early times, so inflationary predictions depend on unknown UV physics — **does not arise**. The model gets this for free where inflationary cosmology has to argue about it.
- **The price.** Expansion never *creates* modes either. Inflation's mechanism is to stretch sub-horizon quantum fluctuations out to super-horizon scales, populating $P(k)$ from the vacuum. On a rigid lattice the **mode set is fixed at $t=0$**. There is nothing to stretch modes *out of*, so there is no dynamical origin for the spectrum.

That is F282's conclusion reached from the opposite direction, and it is why F282's verdict is not an evasion: **the primordial $P(k)$ must be in the initial state, because the substrate offers no process that could put it there later.**

## 5. No initial singularity in the substrate — the first resolvable epoch

The lattice is eternal and unchanging; the Big Bang is a hot, dense **state** of the automaton, not a creation event for the substrate. The singularity the model does have is F183's Schwarzschild one, and it lives in the *emergent* metric.

The earliest epoch the lattice can resolve is the one whose Hubble radius is a single cell. With $a=3^{1/4}/M_\text{Pl}$ (F282 leg A, reduced units) and $R_H=c_\text{lat}/H$, setting $R_H=a$ gives

$$H_\text{max}=\frac{c_\text{lat}}{a}=3^{-3/4}M_\text{Pl}=0.43869\,M_\text{Pl},\qquad t_\text{min}=\frac1{H_\text{max}}=\frac{a}{c_\text{lat}}=3^{3/4}M_\text{Pl}^{-1}.$$

The same quantity in **lattice units**, where $a=1$ cell by definition, is
$$t_\text{min}=\frac1{c_\text{lat}}=\sqrt3\ \text{ticks},$$
i.e. exactly **one cell-crossing time** — light crosses one cell in $1/c_\text{lat}=\sqrt3$ ticks. (Both expressions are the same time in different units; the test asserts both.) In SI, $a=1.0664\times10^{-34}$ m and $t_\text{min}=6.161\times10^{-43}$ s $=11.43\,t_\text{Planck}$ — *larger* than $t_\text{P}$, because $a$ is $6.598$ **non-reduced** Planck lengths.

"Earlier" than that is not before the beginning of time — it is a sub-cell configuration the lattice does not resolve, in the same way that a wavelength below $a$ is not a short wave but a non-existent one. **The cutoff does the work usually handed to quantum gravity**, with no singularity and no new ingredient.

This completes a clean ladder of quarter-powers of 3, all from $d=3$:

| Quantity | Closed form | Value |
|---|---|---|
| Lattice light speed $c_\text{lat}$ | $3^{-1/2}$ | $0.57735$ |
| Cutoff $\Lambda_\text{UV}/M_\text{Pl}$ | $3^{-1/4}$ | $0.75984$ |
| First resolvable $H_\text{max}/M_\text{Pl}$ | $3^{-3/4}$ | $0.43869$ |
| Inflation obstruction $r=M_\text{Pl}^2/\Lambda^2$ | $3^{+1/2}$ | $1.73205$ |

The present Hubble radius is $1.287\times10^{60}$ cells, so the observable universe holds $\sim2.1\times10^{180}$ cells. The substrate is vast but the count is finite and fixed.

## 6. The horizon and flatness problems — dissolved, not solved (stated honestly)

A cellular automaton's initial state is specified **across the whole lattice at once**. It can therefore carry correlations at any separation without any causal process having established them. That is precisely the property inflation was invented to supply.

So the model **dissolves** the horizon problem: homogeneity across causally disconnected patches at recombination is not mysterious, because the state was set globally at $t=0$. The same applies to flatness.

**This is not a free win, and it should not be presented as one.** Dissolving a problem by assumption is exactly the criticism levelled at initial-condition "solutions" in standard cosmology, and it applies here in full. The honest accounting is:

| | Inflation | This model |
|---|---|---|
| Horizon problem | *explained* by a dynamical mechanism | **assumed** in the initial state |
| Flatness | explained | assumed |
| Trans-Planckian modes | a genuine open worry | **absent by construction** (§4) |
| $P(k)$ amplitude, tilt | **predicted** (given a potential) | **assumed** — a free function |
| $\Omega_\text{DM}$ via $\beta$ | predicted from $P(k)$ | free (F238) |
| Initial singularity | present, deferred to quantum gravity | **absent** in the substrate (§5) |
| $\dot G/G$ | model-dependent | $\equiv0$ **exactly**, falsifiable (§2) |

The model trades *predictive* power over the primordial spectrum for *structural* cleanliness at the beginning. That is a real trade, not obviously a good one, and naming it is more useful than winning it.

## 7. Verdict

> **The lattice is the stage, not the play.** $a$ is a constant of the substrate; cosmic expansion is the evolution of the emergent metric's conformal factor $K$ over a fixed, eternal BCC array. FRW is reproduced exactly (F182/F188 unchanged), redshift is dielectric rather than metric-stretching, and the one observable that distinguishes this reading from "space itself expands" is $\dot G/G$ — predicted to be **exactly zero**, already favoured by LLR at 3 orders. There is no initial singularity in the substrate: the first resolvable epoch is $H_\text{max}=3^{-3/4}M_\text{Pl}$ at $t_\text{min}=\sqrt3$ ticks, one cell-crossing. The trans-Planckian problem is absent by construction — and the same rigidity that removes it is what forbids generating $P(k)$, so F282's "the spectrum is an initial condition" is **forced**, not chosen.

## 8. Falsifiers

1. **Any detection of $\dot G\ne0$.** The prediction is exactly zero for a structural reason; there is no parameter to absorb a detection.
2. **Evidence for a genuine trans-Planckian imprint in the CMB.** Would indicate modes were created by expansion, contradicting a fixed mode set.
3. **A demonstration that $K$'s homogeneous mode cannot reproduce FRW with the model's source.** Would break §2. F182/F188 are the standing evidence that it can.
4. **A first-principles derivation of $P(k)$ from lattice dynamics.** Would falsify §4's "no process could put it there", and would be very welcome.
5. **A finite lattice too small for $2.1\times10^{180}$ cells.** The cell budget is computed, not assumed; a substrate bounded below that is excluded.

## 9. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $H_\text{max}=c_\text{lat}/a=3^{-3/4}M_\text{Pl}$; $t_\text{min}=1/c_\text{lat}=\sqrt3$ ticks | **exact-algebraic** |
| The $3^{-1/2},3^{-1/4},3^{-3/4},3^{+1/2}$ ladder | **exact** |
| $a=1.0664\times10^{-34}$ m, $t_\text{min}=6.161\times10^{-43}$ s $=11.43\,t_\text{P}$ | **computed** (F107 SI anchor) |
| $R_H=1.287\times10^{60}$ cells; $2.1\times10^{180}$ cells in the Hubble volume | **computed** |
| $\dot G/G\equiv0$ exactly | **derived** (F79 structural $G$ + F283 rigidity) |
| Expansion $=$ $K$'s homogeneous mode | **structural** (forced by F283 + F64/F106/F178) |
| Fixed mode set ⇒ no trans-Planckian problem **and** no spectrum generation | **structural** |
| No substrate singularity | **structural** |
| Horizon/flatness dissolved into the initial state | **interpretive** — explicitly labelled as assumption-shifting in §6 |
| An initial-condition account of $n_s=0.965$ and $A_s=2.1\times10^{-9}$ | **open** — the live question F282 handed on, and this finding does not close it |

## 10. Honest scope

The exact content here is small and clean: the epoch scales and the $\dot G/G\equiv0$ prediction. The structural content — expansion as $K$'s conformal mode — is not a new derivation but a forced reading of F64/F106/F178 once F283 removes the alternative; its value is that it was previously tacit, and tacit readings are where contradictions hide. The interpretive content in §6 is the weakest and is flagged: dissolving the horizon problem by initial condition is a *relocation* of the explanatory burden, and the table in §6 exists so that relocation is visible rather than quietly banked as a success. What this finding does **not** do is supply the initial-condition physics; §9's last row is the same open item F282 left, and it remains open.

## 11. Files
- Module: `src/casim/engine/interactions/cosmology_lattice_elasticity.py`
- Test: `tests/findings/test_F283_F284_lattice_elasticity.py`
- Results: `test-results/F283_F284_lattice_elasticity.json`
- Theory doc: `docs/theory/primordial-sector.md`
