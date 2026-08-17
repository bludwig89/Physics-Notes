# F305 — The lattice Feynman rules of the **genuine** BCC gauge action are derived, not transcribed: the 4-bond rhombus reproduces $\delta_{ij}\sum_l\hat k_l^2-\hat k_i\hat k_j$ **exactly**, has the Yang–Mills continuum limit to $O(a^2)$, and carries **one extra massless mode** the hypercubic action never had

**Date:** 2026-08-08 - 12:20
**Status:** Established — **9/9 PASS** + control, `casim test --id F305-bcc-rhombic-vertices` (PASS on the tree, 0.3 s; control **CONTROL**, journalled). Executes F265 §9 item 1 (*"`ca_lpt_*` — the entire one-loop chain is 4D hypercubic Wilson … the BCC-BZ vertex computation is the one remaining production-grade job"*) for the vertex half.
**Module:** `casim.engine.gauge.lpt_bcc_vertex` (`src/casim/engine/gauge/lpt_bcc_vertex.py`)
**Script:** `tests/findings/test_F305_bcc_rhombic_vertices.py` (registry entry `check_bcc_vertices`, tier **gate**)
**Results:** `test-results/F305_bcc_rhombic_vertices.json`
**Cross-references:** [[F265-bcc-gauge-action-blindness]] (the defect this answers: the gauge action was simple-cubic while the propagators were BCC, and the composite plaquette is blind to 1/3 of the curvature), [[F278-bcc-lattice-constant-two-over-root-three]] (the cube/BZ ratio, here re-derived for the gauge **link** lattice by primitive-cell volume), [[F267-walk-bz-measure-not-the-fft-cube]]/[[F273-mode-sum-vs-bz-integral-audit]] (the domain hazard; this finding supplies a genuine fundamental domain for the gauge side), [[F162-bgfield-self-energy-b0-gate]]/[[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the vertex machinery generalised), [[F280-d1-subtracted-against-wilson]] (leg 3, the consumer), [[F141-ws-cell-onshell-counting]] (the 4-axis/6-orientation counting this puts in momentum space). Consumer: [[F307-action-consistent-d1-and-a-live-refold]].

---

## 1. The obstruction

F265 found the model's gauge sectors split down the middle — BCC propagators, simple-cubic action — and showed the composite-SC plaquette is *blind*: there is an exact family of link configurations on which every composite plaquette is the identity while the genuine BCC plaquettes are maximally disordered. It then re-scoped the whole $d_1$ chain (F144/F151/F152/F154/F155/F162/F163/F239, and since F280) as *"measured on an action that is blind to 1/3 of the curvature"*, and listed `ca_lpt_*` under **still cubic, explicitly open**.

`lpt_vertex`'s own docstring states the premise F265 invalidated:

> what differs between the rule and Wilson is the PROPAGATOR (the luminal F26 $\Omega_\text{even}$ kinetic sector), **not the plaquette vertex**.

It does differ. The rule's minimal gauge loop is not a square plaquette at all — the BCC nearest-neighbour graph has no closed 3-bond loop and no square; it has a **4-bond rhombus**, on **4 link axes**, in **6 spatial orientations**.

## 2. Method — one code path, two actions

The same multilinear link expansion as `casim.engine.core.lpt_generator` (HiPPy/HPsrc-style: expand $U=e^{iA}$ order by order, read the momentum-space coefficient off the action). Nothing is transcribed. The one new observation that makes it cheap: the $n$-point vertex of any compact plaquette action is a **finite** sum

$$V=\sum_t c_t\,\exp\Big(i\sum_r k_r\cdot v_{t,r}\Big),$$

$c_t$ a colour trace and $v_{t,r}$ the link-midpoint shift leg $r$ sits at. So the term list is enumerated **once** per (action, axis-tuple) and then evaluated vectorised — $2.2\times10^{-16}$ against the brute-force generator on the hypercubic action, and **exactly zero** on the BCC one.

Because the enumeration is parameterised by the loop word, the hypercubic plaquette and the BCC rhombus run through **one** code path. That is not tidiness: it is what makes a rule-minus-Wilson difference a difference rather than two pipelines compared by eye (F307).

Generalised hatted momentum: $\hat k_i=2\sin(k\cdot D_i/2)$ over the 5 generalised axes (4 spatial $\langle111\rangle$ link axes + Euclidean time). For the hypercubic action $D_i=e_\mu$ and this **is** Wilson's $2\sin(k_\mu/2)$.

## 3. The gates

| # | Statement | Result | Tier |
|---|---|---|---|
| G1 | 2-point vertex $=\delta_{ij}\sum_l\hat k_l^2-\hat k_i\hat k_j$, overall $K=1$ | $K=1+2\times10^{-16}$, structure spread $8.9\times10^{-15}$ | **exact** |
| G2 | $\sum_i d_i d_i^{\mathsf T}=4\,\mathbb I$; isotropic continuum limit, on-axis $S=4k^2-k^4/3$ | deviation **literally 0.0**; quartic $-0.33322,-0.33331$ vs $-1/3$ | **exact** |
| G3 | 3-point vertex $\to$ axis-space YM tensor, $K=i$, deviation $O(a^2)$ | $K_\text{im}=1-4.6\times10^{-9}$, rel-spread $8.58\{-5,-7,-9\}$, order ratios $99.999,\,100.000$ | **exact + $a^2$** |
| G4 | antisymmetry under simultaneous (axis, momentum) exchange | $1.6\times10^{-16}$ | **exact** |
| G5 | lattice Ward identity $\sum_j\Gamma_{ij}\hat k_j=0$ at finite $a$ | $<10^{-13}$ | **exact** |
| G6 | mode count — **one gauge zero mode and four massless modes** | see §4 | **exact + fork** |
| G7 | cube $[-\pi,\pi)^3$ holds exactly **4** BCC Brillouin zones; $S$ exactly reciprocal-periodic | $4.0000000000$; $1.15\times10^{-14}$; WS fraction $0.2497$ (MC) | **exact** |
| — | declared gap: action vs propagator (§5) | agree at small $k$ to $1.4\times10^{-5}$, differ by up to **86%** at generic $k$ | reported |

**Control (D9).** `--param nhat_perturb=0.4` tilts the redundant link-axis combination out of the null space of $\sum_i n_id_i=0$. **G6 goes red and nothing else does** — verified. That is the right perturbation because G6's content is that *that particular* combination is the massless eigenvector; any other direction is not.

## 4. G6 — the mode count, and the fork it opens

$\Gamma=S\,\delta-\hat k\hat k^{\mathsf T}$ with $S=\sum_l\hat k_l^2$ has **one** zero eigenvalue (the gauge mode, the Ward identity of G5) and **four** degenerate eigenvalues $S$. Continuum 4-D Yang–Mills has **three**. The extra one is not an accident of bookkeeping — it is the unique redundant link-axis combination

$$\hat n=\tfrac12(-1,1,1,1),\qquad \sum_i n_i d_i=0 ,$$

and three things are true of it simultaneously:

1. it is an eigenvector with eigenvalue $S$ — i.e. **massless and exactly transverse** — to $3.2\times10^{-15}$ in the continuum limit, with the finite-$a$ mixing into the gauge mode measured at $2.9\times10^{-5}$ at $|k|\sim0.5$ (an $O(a^2)$ effect);
2. the 3-gluon vertex does **not** annihilate it: the contraction is $0.500$ of the vertex's own scale;
3. the Cartesian projector $P^a{}_i=d_i^a/2$ satisfies $PP^{\mathsf T}=\mathbb I$ **exactly** (residual `0.0`), so the space orthogonal to $\hat n$ maps *isometrically* onto 3 Cartesian directions + time.

So the rhombic action, read as a functional of 4 independent spatial link fields, propagates one massless adjoint mode more than SU(3) Yang–Mills does, and that mode interacts. Point 3 is what settles which reading is the physical one: **the projected branch's continuum limit is exactly 4-D Yang–Mills, because the projection is an isometry.** The unprojected branch's is not.

That is corroborated, not merely argued, by the one-loop coefficient. Running the rhombic action's own background-field self-energy on its own Brillouin zone in a small-$Q$ window:

| $n$ | projected branch $b_0$ | unprojected branch $b_0$ |
|---:|---:|---:|
| 8 | $9.67$ | $-2.21$ |
| 12 | $10.94$ | $-1.89$ |
| 16 | $11.56$ | $-1.86$ |

against $b_0=\tfrac{11}{3}C_A=11$. The projected branch trends onto it; the unprojected branch is not merely wrong in magnitude but **wrong in sign** — it is not an asymptotically free theory at all. (This window sits below the F287 §5 resolution floor, so these are a trend and a sign, deliberately not quoted as a digit; F307 §3 is where that is handled properly.)

**Named honestly:** it is *not* a theorem that the rule's link fields carry no independent $\hat n$ excitation. What is established is that if they do, the continuum limit is not Yang–Mills. The model has never recorded a decision here, and F265 could not have surfaced it because the pre-F265 action had only 3 composite link directions and therefore no redundant mode to find.

## 5. The gap this opens, stated rather than hidden

The rhombic **action**'s own quadratic form and the F26 rotation law's **propagator** are not the same object at finite lattice spacing:

$$\tfrac14 S(k)\ \longrightarrow\ 3\,\Omega_\text{even}(k)^2\ \longrightarrow\ |k|^2 \quad (k\to0),$$

agreeing to $1.4\times10^{-5}$ at $|k|\sim10^{-2}$ — and differing by up to **86%** at generic $k$ in the zone. Lattice perturbation theory is only internally consistent (Ward identity, $b_0$ recovery) when the propagator is the inverse of the same quadratic form the vertices came from, so an LPT calculation must pick one. This finding supplies the action-consistent object and **does not decide** which is "the rule's gauge action" at finite $a$. That decision is now visible, which it was not before.

## 6. Honest scope

- **Vertices and the action's quadratic form only.** No claim is made that the rule's gauge action *is* the rhombic Wilson action; §5 is the reason that matters.
- **G6's fork is decided in one direction only** — by an exact isometry argument plus a $b_0$ trend, not by a theorem about the model's link content.
- **The Brillouin-zone result is for the gauge link lattice.** F267's fermion-walk question is untouched.
- **$C_{\overline{\rm MS}}$, the Wilson anchor and F280's budget are reused, not re-derived.**
- The $b_0$ table in §4 is at $Q$ below the F287 §5 floor and is a **trend**, not a measurement.

## 7. What this hands on

1. **The rule's vertex form factors now exist**, derived and gated, which is what F280 leg 3 was waiting on. F307 consumes them.
2. **A genuine fundamental domain for the gauge side** (the Wigner–Seitz cell of the BCC reciprocal lattice), with cube/BZ $=4$ confirmed exactly by primitive-cell volume — the F267-class hazard is *removed* on this side rather than bounded.
3. **A decision the model owes itself:** whether the redundant link-axis mode is dynamical. It changes the sign of $b_0$, so it is not a refinement.
4. **The same machinery is action-agnostic.** Pointing it at any other loop word (an improved action, a rectangle term) costs one function.

## 8. Provenance

- **New:** the rhombic loop words and their axis/sign resolution; the finite-term enumeration of a compact plaquette vertex and its vectorised evaluator (validated against the brute-force generator at $2.2\times10^{-16}$ / exactly 0); the exact 2-point form on the BCC link-axis space; the $\sum_i d_id_i^{\mathsf T}=4\mathbb I$ isotropy theorem and the on-axis $-k^4/3$; the axis-space YM continuum-limit gate with its $O(a^2)$ order read; the redundant-mode analysis and the fork; the WS fundamental domain and the primitive-cell volume derivation of cube/BZ $=4$.
- **Reused:** `casim.engine.core.lpt_generator` (link expansion, colour generators, $f^{abc}$); `casim.engine.lattice.geometry` (`BCC_LINK_AXES`, `BCC_PLAQUETTES`); `casim.engine.gauge.gluon_self_energy.omega_even` for §5.
- **Verification:** registry record `F305-bcc-rhombic-vertices` (tier gate, entry `check_bcc_vertices`), 9/9 PASS + control, 2026-08-08 - 12:20.

## 9. Verification amendment — 2026-08-08 - 14:05

Run on the tree, not in a sandbox copy. `casim test --id F305-bcc-rhombic-vertices` **PASS**;
`check_control_soundness.py --run` returns **CONTROL** — *"`--param nhat_perturb=0.4` reddens
exactly `['G6_mode_fork']` of 8 leg(s)"* — and the verdict is journalled in
`test-results/control-soundness.json` (**commit it**). Gate checks verified individually
(the 45 s ceiling forbids one `run_gate.py` pass): `casim index --check`, `gen_test_registry
--check`, `gen_module_graph --check`, `check_test_registry`, `check_module_registry`
(205 registered, all covered), `check_finding_records` (300 findings, every declared record
exists at the tier it claims), `check_control_soundness --gate` (31 of 31 verified RED at the
current fingerprint), `check_deprecated`, `check_claims`, and the D8/D7 ratchets — all green.
`gen_module_graph.py` was run **before** `gen_test_registry.py`, per the standing generator-order
gotcha. One implementation note: the D9 runner reads control legs from `payload["checks"]`, so
the entry point emits `checks` with `legs` kept as a readable alias — a payload naming its legs
only under `legs` is scored `INVALID`, which is how this was caught.
