# F162 — The background-field one-loop gluon self-energy is **assembled and the $b_0=\tfrac{11}{3}C_A=11$ recovery gate PASSES exactly** (transverse, gluon : ghost $=10:1$), and the lattice running is confirmed propagator-independent — but the finite $d_1$ that pins $q_\ast$ to the digit stays **open** (the vertex form-factor part, with its Wilson-28.81 gate), so the F155 bracket $q_\ast a\in[1/\sqrt3,\sim0.97]$ stands

> **[PARTIALLY SUPERSEDED 2026-08-01 by F272 — ledger S11-F272-bgfield-refold-removed]**
>
> **DEAD:** Every number produced through the refolded _Bcoeff_numeric. The `mod 2 pi` refold of k+q evaluated the propagator at a genuinely inequivalent momentum -- omega_even's period lattice is sqrt3*fcc, so 2 pi per axis is not a period of it -- and manufactured a spurious q-dependence indistinguishable from the residual log the test existed to detect. Flatness spread moved 1.58e-2 -> 2.96e-5, a factor 530.
>
> **STILL LIVE:** The background-field apparatus itself, which F287 re-verified SOUND post-F272/F277 and which recovers b_0 = 11. The Wilson control is unaffected: Wilson IS 2 pi-periodic, so for it the refold was an exact no-op (2e-14), which is what made the removal safe rather than a change of result.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-06-18 - 14:30
**Status:** Partial — the **b₀ gate is PASSED** (exact, continuum + lattice-propagator-independent), which is the loop-assembly validation F155 lacked; the **finite $d_1$ to the digit is NOT closed** (it needs the bespoke lattice 3-gluon + ghost form factors, validated against Wilson's $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ — not executed). 3/3 checks PASS. G1 exact (b₀=11, transverse, gluon:ghost 10:1 — symbolic/machine); G2 well-conditioned (lattice b₀ = continuum b₀, subtracted shift q-flat to $<10^{-3}$); G3 scope-sharp.
**Honest headline:** F155 said *"the loop assembly + b₀ recovery is the open computation."* This finding **does** the assembly and **passes b₀ exactly** — the background-field self-energy (gluon loop $\Gamma^F\Gamma^F$ + ghost loop $-2(2k{+}q)(2k{+}q)$, Abbott $\xi{=}1$) is exactly transverse with $b_0=\tfrac{11}{3}C_A=11$. The remaining piece is now sharply isolated: the **finite vertex form-factor constant**, whose validation gate is reproducing Wilson's 28.81 with the full lattice vertices+tadpole. That is not done here, so $q_\ast$ remains **bracketed**, not pinned.
**Modules:** `ca-simulation/ca_bgfield_loop.py` (fills the F155 scaffold: `b0_gate_symbolic`, `gammaF_tensor_continuum`, `lattice_b0_consistency`, `d1_qstar_status`).
**Script:** `tests/findings/test_F162_bgfield_loop.py` (~10 s; sympy + numpy). Native: `tests/runners/run_bgfield_loop.py`.
**Results:** `test-results/F162_bgfield_loop.json`, `test-results/F162_bgfield_loop_highres.json`.
**Cross-references:** [[F155-qstar-self-energy-and-freeze-bracket]] (the bracket this advances; A0 tadpole-empty, A2 b₀-universal, A6 moment-insensitivity — this builds the loop assembly those framed as open), [[F151-scheme-constant-determined]] (V-scheme + $a_1=\tfrac{11}3$ + the $q_\ast$ band this brackets), [[F154-residuals-A-B-built-and-solved]] (A's cheap route ruled out — the finite subtraction this assembles), [[F129-blockspin-free-photon]]/[[F130-blockspin-rg-gauge-gravity]] (the near-perfect action = why the rule's propagator-driven shift is ~0, $q_\ast$ at band top), [[F105-axial-photon-exactly-dispersionless]] (luminal gluon → continuum at small $k$ = why lattice $b_0$ = continuum $b_0$). External: Abbott, *Nucl. Phys.* **B185** (1981) 189; Hashimoto–Kodaira–Yasui–Sasaki, hep-ph/9406271 (the BFM Feynman-gauge self-energy Eq. 18–20, transcribed here). `ca_lpt_ward.py` (the continuum vertex $\Gamma$ + Ward identity this vertex reduces to).

---

## 1. What this finding does

F155 brought Residual A to a sharp point: the tadpole sector is exactly empty (A0), the running coefficient $b_0$ is universal (A2), and the moment route is dead (A6, the moment-insensitivity theorem) — so $q_\ast$'s shift from the band top ($\sim0.97/a$) to the implied $0.733/a$ is *entirely* a finite, vertex-dependent constant $d_1$, computed from the **background-field one-loop gluon self-energy**. The one thing F155 did **not** have was the assembled loop itself — it used a scalar bubble as a stand-in. This finding **assembles the actual loop** and validates it: it passes the $b_0=\tfrac{11}{3}C_A$ recovery gate exactly. It is explicit about the one piece that remains.

## 2. G1 — the $b_0$ gate, PASSED exactly (the loop assembly is correct)

In the background-field method (Abbott; Hashimoto–Kodaira–Yasui–Sasaki, hep-ph/9406271) the coupling renormalisation is $Z_g=Z_A^{-1/2}$, so $b_0$ comes from the background self-energy **alone** — provided one uses the background–quantum–quantum vertices. In Feynman background gauge $\xi=1$ the self-energy is (their Eq. 1, 19, 20)

$$\Pi_{\mu\nu}(q)=\tfrac{N}{2}\!\int\!\frac{d^4k}{(2\pi)^4}\frac{1}{k^2(k+q)^2}\Big[\underbrace{\Gamma^F_{\alpha\mu\lambda}(k,q)\,\Gamma^F_{\lambda\nu\alpha}(k{+}q,-q)}_{\text{gluon loop}}\;\underbrace{-\,2(2k{+}q)_\mu(2k{+}q)_\nu}_{\text{ghost loop}}\Big],$$

with the AQQ vertex (their Eq. 18)

$$\Gamma^F_{\alpha\mu\lambda}(k,q)=-2q_\lambda\,\delta_{\alpha\mu}+2q_\alpha\,\delta_{\mu\lambda}-(2k{+}q)_\mu\,\delta_{\lambda\alpha}.$$

Extracting the UV (log-divergent) part by the large-$k$ expansion and the 4D angular average (`b0_gate_symbolic`, sympy), the result is **exactly transverse** and carries the universal running:

$$g_{\mu\nu}=\tfrac{22}{3}\big(q^2\delta_{\mu\nu}-q_\mu q_\nu\big),\qquad b_0=\tfrac{N}{2}\cdot\tfrac{22}{3}=\tfrac{11}{3}C_A=\boxed{11}\quad(C_A=N=3).$$

The normalisation is fixed by calibrating against the scalar bubble (its log coefficient is exactly $1/16\pi^2$; the code returns $g_{\rm scalar}=1$). The **gluon : ghost split** is clean: $b_0^{\rm gluon}=10$, $b_0^{\rm ghost}=1$ ($g$-coefficients $20/3$ and $2/3$), summing to the QCD $11$. This is an **algebraically exact** statement — it certifies that the loop is assembled with the correct vertices, group theory, and gluon↔ghost gauge cancellation (the transversality is the loop-level Ward identity). **This is the object F155 was missing.**

## 3. G2 — lattice $b_0$ = continuum $b_0$ (well-conditioned, subtracted)

The log coefficient is universal: it is generated in the region $q\ll k\ll 1/a$ where the lattice integrand $\to$ continuum (A1 luminal gluon, A2, F129 near-perfect action). Confirmed numerically and *well-conditioned* via the subtracted transverse coefficient $B$ (the coefficient of $q_\mu q_\nu$, clean of the $\delta_{\mu\nu}\Lambda^2$ mass divergence): swapping $1/k^2\to 1/K_{\rm lat}$ (Wilson $\hat K=4\sum\sin^2(k/2)$ or the rule $K=3\,\Omega_{\rm even}^2$) leaves

$$\Delta(q)\equiv B_{\rm lat}(q)-B_{\rm cont}(q)\quad\text{q-INDEPENDENT (a residual log would grow like }\ln 1/q).$$

The Wilson shift is flat to $<10^{-3}$ ($\Delta_{\rm W}=-0.0787$, spread $7\times10^{-5}$ at $n{=}24$) — decisive evidence that $b_0^{\rm lat}=b_0^{\rm cont}=11$. The rule's propagator-driven shift is $\to 0$ ($\Delta_{\rm rule}\to-0.0002$ at $n{=}24$): the **near-perfect action** means the rule's propagator alone barely moves the finite constant, so $q_\ast$ stays at the band top $\sim0.97$ — exactly the F155 result, now understood as a propagator-vs-vertex decomposition.

## 4. G3 — what is NOT done (the finite $d_1$ to the digit), stated sharply

Pinning $q_\ast a=\exp(-d_1/2b_0^\alpha)=0.733$ to the digit requires the **finite** constant of the *lattice* self-energy, which is

$$d_1^{\rm lat}=\underbrace{d_1^{\rm cont}}_{\overline{\rm MS}}+\underbrace{(\text{propagator-driven shift})}_{\sim0\text{ for the rule (G2, near-perfect action)}}+\underbrace{(\text{vertex form-factor shift})}_{\textbf{OPEN — the bespoke lattice 3g+ghost }\cos(k/2)\text{ vertices}}.$$

The vertex form-factor part is **not computed here**, and its validation gate — reproduce the Wilson finite constant $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ with the full lattice vertices *and* tadpole — is **not executed**. A continuum-vertex stand-in (G2) only reproduces the propagator piece, i.e. the band top. Therefore:

> **$q_\ast$ remains BRACKETED, not pinned.** The F155 bracket $q_\ast a\in[1/\sqrt3,\ \sim0.97]$ (implied $0.733$ inside; $\Lambda$-ratio $O(1)$, not Wilson's $28.81$) **stands.** What this finding removes is the *"is the loop even assembled correctly?"* question — answered yes, exactly ($b_0=11$). The sole remaining computation is the vertex form-factor finite constant, with its sharp Wilson-28.81 gate.

A wrong $q_\ast$ would be worse than this honest bracket; the $g_s=\tfrac12$ lock would be falsified only if a *validated* finite-$d_1$ computation landed near Wilson's $\sim29$ — which A0 (exact tadpole-emptiness) makes structurally impossible.

## 5. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | assembled BFM self-energy exactly transverse; $b_0=\tfrac{11}{3}C_A=11$ (gluon:ghost $=10{:}1$); scalar calibration $g{=}1$ | PASS | exact/symbolic |
| G2 | lattice $b_0$ = continuum $b_0$: subtracted $\Delta=B_{\rm lat}{-}B_{\rm cont}$ q-flat (Wilson spread $<10^{-3}$); rule shift $\to0$ (near-perfect action) | PASS | well-conditioned |
| G3 | scope-sharp: finite $d_1$ to digit OPEN (vertex form factors, Wilson-28.81 gate); F155 bracket stands; targets $q_\ast{=}0.733$, $\Lambda{=}1.78$, Wilson $28.81$ must not match | PASS | scope |

**Overall 3/3 PASS** (~10 s).

## 6. Honest scope

- **The $b_0$ gate is the continuum + lattice-propagator statement**, proven exactly and well-conditioned. It validates the loop **assembly** (vertices, group theory, gluon/ghost cancellation, transversality). It does **not** by itself pin the finite constant.
- **The full Wilson lattice self-energy (→ 28.81) is NOT reassembled here.** That finite-constant gate — the definitive validation of the lattice *vertex* machinery — remains the prerequisite before the rule's $d_1$ digit can be trusted. The validated tadpole $Z_0=0.1549$ (`ca_lpt_wilson`) is the dominant Wilson piece; the vertex+ghost finite parts are still the open increment, as F155/the design doc state.
- **The rule's propagator-driven shift ($\to0$) is reported as small, not as the full $d_1$.** Its $n{=}24$ mean $-0.0002$ is convergent toward zero (near-perfect action); the spread is grid-sensitive (the $\arccos$ kernel), tightening in the native runner. This is consistent with — not a sharpening of — the F155 band-top result.
- This finding is an **increment over F155**: the loop assembly + exact $b_0$ recovery, plus the propagator/vertex decomposition of the finite constant, isolating the vertex form-factor part as the single remaining computation.

## 7. Provenance

- **New:** the assembled background-field gluon+ghost self-energy and the exact $b_0=\tfrac{11}{3}C_A=11$ recovery with the gluon:ghost $10{:}1$ split (`b0_gate_symbolic`); the scalar-bubble normalisation calibration; the well-conditioned subtracted lattice-$b_0$ consistency check (`lattice_b0_consistency`); the propagator-vs-vertex decomposition of the finite $d_1$ (`d1_qstar_status`).
- **Reused:** the Abbott/HKYS BFM Feynman-gauge rules (Eq. 18–20, hep-ph/9406271); the continuum vertex $\Gamma$ + Ward identity (`ca_lpt_ward`); the rule propagator kernel $K=3\Omega_{\rm even}^2$ (`ca_gluon_self_energy.K_true_4d`); F155's A0/A2/A6 framing.
- **External anchors (targets, not inputs):** $b_0=\tfrac{11}{3}C_A$; Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$; implied $q_\ast a=0.7327$, $\Lambda$-ratio $1.78$ (F151/F144).
- **Verification:** `tests/findings/test_F162_bgfield_loop.py` (2026-06-18, 3/3 PASS); results `test-results/F162_bgfield_loop.json`.
