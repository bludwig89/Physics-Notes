# F166 — The triple-gluon vertex is branch-blind (no chiral component): the gluon "even" classification is upgraded from forced-at-free-field (F91 G1) to forced-at-the-interacting-(self-coupling)-level — closing audit C3

**Date:** 2026-06-29 - 17:10
**Numbering:** a concurrent session took F165 (`F165-hypercharge-quantisation-from-anomaly-and-mass`); this finding is renumbered to **F166** to avoid the collision (per the concurrent-session caution).
**Status:** Confirmed — 4/4 checks (3 exact / structural-zero, 1 machine + contrast). Closes audit C3 (Physics Audit Report 2026-06-29): the SU(3) self-coupling has **no chiral (branch / γ⁵) component**, so the gluon even-channel forcing extends from the free propagator to the interacting theory. The result is **structural** (by-construction), not a dynamical surprise — see Scope.
**Script:** `tests/findings/test_F166_triple_gluon_branch.py`
**Results:** `test-results/F166_triple_gluon_branch.json`
**Cross-references:** [[F91-pairing-classification-theorem]] (G1 is the free-propagator commutator this extends to the cubic vertex; the classification table this augments), [[F68-minimal-coupling-forces-even-photon]] (the branch-blind ⇒ even argument replayed), [[F162-bgfield-self-energy-b0-gate]] (supplies the model's actual triple-gluon AQQ vertex `gammaF_tensor_continuum`; its open item — the finite d₁/q\* digit — is *magnitude*, orthogonal to branch structure), [[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the lattice 3-gluon + ghost vertices, `cos(k/2)` form factors; same branch-trivial structure), [[F72-universal-even-propagator]] (catalog: gluon EVEN). Modules: `ca-simulation/ca_bgfield_loop.py`, `ca-simulation/ca_lpt_vertex.py`, `ca-simulation/ca_gluon.py`.

---

## The question (audit C3)

The Physics Audit Report (2026-06-29, issue **C3**) flagged that F91's gluon "even" classification was proven **only at the free-propagator level**. F91 G1 showed the *fermion–gluon* coupling is branch-blind —

$$\big[\,\mathrm{diag}(U^+,U^-)\otimes\mathbf I_3,\ \mathbf I_4\otimes e^{i\theta\cdot T}\,\big]=0\qquad(1.1\times10^{-16}),$$

i.e. the colour generator $T^a$ acts identically on both BCC chiral branches. But the **SU(3) self-coupling** (the triple- and quartic-gluon vertices of the Yang–Mills action) was never analysed:

> "If the nonlinear self-coupling has any chiral component, the even classification would need revision … weakens 'forced' to 'forced at the free-field level'."

The recommended fix: **prove the triple-gluon vertex is branch-blind, or downgrade to "forced at linear level."**

## The theorem

**The triple-gluon vertex carries no branch (γ⁵) index, exactly, by construction.**

The gluon self-coupling is generated entirely by the pure-gauge plaquette action $S(A)$ — a functional of the gauge field $A^a_\mu$ alone. The gauge field carries a **Lorentz** index $\mu$ and a **colour** index $a$, and **no branch index**. The model's own one-loop vertex (F162/F163, Abbott background-field, $\xi=1$) is

$$\Gamma^F_{\alpha\mu\lambda}(k,q)=-2q_\lambda\,\delta_{\alpha\mu}+2q_\alpha\,\delta_{\mu\lambda}-(2k+q)_\mu\,\delta_{\lambda\alpha},$$

a rank-3 **Lorentz** tensor times the colour structure constant $f^{abc}$. There is no Dirac/spinor factor anywhere. In branch (BCC-chirality) space its matrix is therefore the identity $\mathbf I_2$, and its chiral (pseudoscalar) projection vanishes identically:

$$P_{\gamma^5}(\mathbf I_2)\equiv\tfrac12\,\mathrm{Tr}\!\big(\gamma^5\,\mathbf I_2\big)=\tfrac12(1-1)=0.$$

By the F68 argument (branch-blind coupling can source only the helicity-symmetric dispersion), the self-coupling — like the photon, and unlike the W — forces the **even** channel. This is the F91-G1 commutator replayed for the cubic vertex.

### Branch-matrix view (extends the F91 table to the vertex)

| sector | branch matrix $M$ | $P_{\gamma^5}(M)=\tfrac12\mathrm{Tr}(\gamma^5 M)$ | channel |
|---|---|---|---|
| γ (coupling $\propto Q$) | $Q\,\mathbf I_2$ | $0$ | **even** |
| **gluon self-coupling** | $\mathbf I_2$ (no branch index) | $\mathbf 0$ (exact) | **even** |
| W± (left projector) | $P_L=\mathrm{diag}(1,0)$ | $1/2$ | chiral |

The gluon self-coupling sits with the photon at $P_{\gamma^5}=0$; the W is the nonzero contrast.

## What the test shows (4/4)

**T1 — vertex has no Dirac/branch axis (exact, structural).** The model's `gammaF_tensor_continuum(k,q)` returns a real rank-3 tensor of shape $(4,4,4)$ — three Lorentz indices, zero spinor/branch axes. The lattice extractor (`ca_lpt_vertex`) reads the vertex off $S(A)$ with no fermion field present; the quadratic term reproduces the gluon propagator (ratio constant to $3.5\times10^{-3}$ at $L{=}6,g{=}0.5$ — a finite-lattice artifact, informational only).

**T2 — F91-G1 commutator extended to the cubic vertex (exact zero).** Embedding the vertex as $\mathbf I_{\text{branch}}\otimes\Gamma$ and the branch chirality operator as $\gamma^5\otimes\mathbf I_{\text{Lorentz}}$,

$$\big[\,\gamma^5\otimes\mathbf I,\ \mathbf I\otimes\Gamma\,\big]=0\qquad(\text{max}|\cdot|=0.0,\ \text{exact}).$$

**T3 — γ⁵-projection per sector (exact + contrast).** Gluon self-coupling $P_{\gamma^5}=0.0$; photon $0.0$; W $=1/2$ (to $<10^{-15}$). The gluon's chiral projection is exactly zero, identical to the photon; the W reproduces the known chiral value.

**T4 — the self-coupling's only nontrivial index is colour (machine).** A leg colour-swap flips the vertex sign ($f^{abc}$ antisymmetry, $V_{123}+V_{\text{swap}}=0.0$, reusing `ca_lpt_vertex.bose_antisymmetry`). The non-Abelian structure lives entirely in colour, not branch.

## What this settles

1. **Audit C3 is upgraded, not downgraded.** The triple-gluon vertex is provably branch-blind, so the only places a chiral component could have entered the gluon sector are (a) the fermion–gluon vertex — branch-blind by F91 G1/G2 — and (b) the pure-gluon self-coupling — branch-blind by T1–T4 here. There is no chiral component anywhere in the gluon sector. The F68 even-forcing therefore holds at the **interacting** level, not merely the free-propagator level.
2. **The quartic vertex follows identically.** It is generated by the same plaquette $S(A)$ with the same (Lorentz⊗colour, no branch) index content; the argument is verbatim. No separate computation is needed.
3. **The classification principle is now complete for the gluon.** "Channel = branch structure of the coupling" (F91) extends from the linear coupling through every $n$-point pure-gauge vertex.

## Scope and honesty

This is a **structural / by-construction** result, not a dynamical theorem with a numerical surprise. Its entire content is that the gauge sector of the model contains **no spinor index**, so every pure-gluon vertex is branch-trivial. That is exactly what audit C3 asked for — the audit's worry was hypothetical ("*if* the self-coupling has any chiral component"), and the answer is that it provably has none. The result does **not** depend on confinement (F91's earlier "confinement makes this unobservable" pragmatic defence is no longer needed) and is not a free-field-only statement.

What this finding does **not** touch: the **magnitude** of the gluon self-energy — the finite constant $d_1$ that pins $q_\ast a$ to the digit (F162/F163), and the Wilson-$28.81$ scheme gate. Those are orthogonal: they concern *how large* the self-energy is, not *which branch channel* it lives in. The F155 bracket $q_\ast a\in[1/\sqrt3,\ \sim0.97]$ is unaffected by this finding and still stands.

## Checks

| # | Check | Result | Tier |
|---|---|---|---|
| T1 | model triple-gluon vertex `gammaF_tensor_continuum` is real rank-3 Lorentz $(4,4,4)$, **no Dirac/branch axis** | PASS | exact/structural |
| T2 | $[\gamma^5\otimes\mathbf I,\ \mathbf I\otimes\Gamma]=0$ (F91-G1 for the cubic vertex) | PASS | exact (0.0) |
| T3 | $P_{\gamma^5}$: gluon $=0$, photon $=0$, W $=1/2$ (contrast) | PASS | exact + contrast |
| T4 | colour-swap antisymmetry ($f^{abc}$), branch-independent | PASS | machine |

## Recommendation (executed here)

Per audit C3's "Recommended fix" first branch: the triple-gluon vertex **is** proven branch-blind. CLAUDE.md decision 5 and the F91 propagator-classification line should reflect that the gluon "even" classification is forced at the interacting (self-coupling) level. The `ca_gluon` even-law BCC step (migrated in F91, 2026-06-04) is consistent with this upgrade; no code change is required.

## Open / next

- **Quartic vertex explicit check** — argued identical here; a one-line extractor analogous to T1 would make it machine-checked rather than argued. Low priority (same index content).
- **Magnitude, not branch:** the finite $d_1$ / $q_\ast$ digit (F162 G3, F163 W5) remains the live gluon-self-energy open item, independent of this result.

## Files
- Test: `tests/findings/test_F166_triple_gluon_branch.py`
- Results: `test-results/F166_triple_gluon_branch.json`
- Operators exercised: `ca_bgfield_loop.gammaF_tensor_continuum`, `ca_lpt_vertex.propagator_check`/`bose_antisymmetry`/`three_gluon_amplitude`.
