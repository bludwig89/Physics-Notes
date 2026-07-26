# F239 — The $g_s=\tfrac12$ lattice$\to\overline{\rm MS}$ **scheme** conversion factorises **exactly** into a derived piece and one open piece: $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.773=\underbrace{1.299}_{\text{EXACT }V\to\overline{\rm MS}\text{ via }a_1=\tfrac{11}3}\times\underbrace{1.365}_{\text{open rule}\to V\ =\ 1/q_\ast a}$ — so Q2 is **not** wholly the shared $d_1$: its true *scheme* leg is closed, only the lattice$\to V$ match is the shared open number

**Date:** 2026-07-03 - 08:48
**Numbering:** F229–F235 taken by prior/concurrent sessions; this session adds **F239** (Q2). Max F-number re-checked before numbering.
**Status:** Honest partial (one leg closed exact, one leg the shared open $d_1$) — 3/3 checks PASS (`test_F239_scheme_factor_factorization.py`, <30 s, stdlib+numpy). **This executes open-derivations prompt Q2 (#9).** The prompt asks to derive the lattice$\to\overline{\rm MS}$ **scheme** conversion for the $g_s=\tfrac12$ lock from the rotor/dielectric structure (F115/F117), acceptance $\alpha_s(M_Z)$ to $<1\%$ with the factor derived, *or* a clear statement of the remaining perturbative-matching input. **Result:** the scheme conversion $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.773$ **factorises exactly** as $1.299\times1.365$: the first factor — the true $V\!\to\!\overline{\rm MS}$ **scheme** conversion — is **derived exactly** ($a_1(6)=\tfrac{11}3$, on the exact V-scheme identification of the lock, a rotor-structure fact); the second — the rule$\to V$ one-loop lattice matching $=1/q_\ast a$ — is the **shared open $d_1$** (the F162 vertex form-factor integral). So $\alpha_s(M_Z)=0.1180$ is reproduced *the instant $q_\ast$ is pinned*, and the residual is **one integral**: the lattice 3-gluon+ghost vertex form factors, Wilson-$28.81$-gated. **This sharpens F235's "Q1=Q2=E3=$d_1$":** only the lattice$\to V$ leg is $d_1$; Q2's *scheme* leg is closed.
**Script:** `tests/findings/test_F239_scheme_factor_factorization.py`
**Results:** `test-results/F239_scheme_factor_factorization.json`
**Cross-references:** [[F144-route-a-alpha-s-dimensional-transmutation]] (A4: the $\Lambda$-ratio $1.78$ and the $g_s=\tfrac12$ lock this decomposes), [[F151-scheme-constant-determined]] (S1 the exact V-scheme identification + $a_1=\tfrac{11}3$; S3 the $q_\ast$ band — this factorises S1$\times$S3), [[F154-residuals-A-B-built-and-solved]] (Residual A $=q_\ast$ = the open lattice leg here; Residual B already solved), [[F155-qstar-self-energy-and-freeze-bracket]] (the $q_\ast a\in[1/\sqrt3,0.979]$ bracket and the moment-insensitivity theorem this inherits; A0 tadpole-empty), [[F162-bgfield-self-energy-b0-gate]] (the $b_0=\tfrac{11}3C_A$ gate PASSED + the propagator/vertex decomposition this quantifies for the *scheme*), [[F115-coupling-magnitudes-running-rotor]] (CM3 the rotor lock $g_s^2\chi=\tfrac14$ whose scheme this converts), [[F117-gap-coupled-dielectric-gluon-propagator]] ($m_D$/dielectric structure the prompt points to), [[F235-sqrt-sigma-fpi-scale-setting-unifies-with-d1]] (Q1: the "Q1=Q2=E3=$d_1$" verdict this refines — Q2's scheme leg is *not* $d_1$).

---

## 1. What the prompt asked

Q2: *"Derive the lattice$\to\overline{\rm MS}$ scheme conversion factor for $g_s=\tfrac12$ from the rotor/dielectric structure (F115/F117) rather than fitting it. Acceptance: $\alpha_s(M_Z)$ reproduced with the scheme factor derived (exact or $<1\%$), or a clear statement of what perturbative-matching input remains. Coordinate with F145/F154 (Residual B solved; this is the remaining IR/scheme piece)."*

## 2. The scheme conversion, and its exact factorisation (the Q2 result)

The lock $g_s=\tfrac12$ lives at the lattice scale $\mu_0=\hbar c/a$ with $\alpha_s(\mu_0)=1/16\pi$ (F144). Running the *measured* $\alpha_s(M_Z)=0.1180$ up to $\mu_0$ needs $\Delta(1/\alpha)|_{\mu_0}=0.640$, i.e. a scheme conversion $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.773$ (F144-A4/F151). The single new statement of this finding: **this conversion factorises exactly into two multiplicatively-independent legs**, in the $1/\alpha$ (equivalently $\Lambda$-ratio) representation $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=\exp\!\big(\Delta(1/\alpha)/2b_0^\alpha\big)$:

$$\boxed{\;\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}=\underbrace{\exp\!\Big(\frac{a_1(6)/4\pi}{2b_0^\alpha}\Big)}_{V\to\overline{\rm MS}\ =\ 1.299\ \text{(EXACT)}}\;\times\;\underbrace{\frac{1}{q_\ast a}}_{\text{rule}\to V\ =\ 1.365\ \text{(OPEN }d_1)}\;=\;1.299\times1.365=1.773.\;}$$

with $\Delta(1/\alpha)=\underbrace{a_1/4\pi}_{0.2918}+\underbrace{2b_0^\alpha\ln(1/q_\ast a)}_{0.3465}=0.638$ ($b_0^\alpha=0.5570$, $q_\ast a=0.7327$). Verified exact-factorising: the product of the two $\Lambda$-factors equals the full ratio to $<10^{-12}$ (Q1 check), and the open leg is *exactly* $1/q_\ast a$.

## 3. Leg 1 — the *scheme* conversion ($V\to\overline{\rm MS}$) is derived **exactly**

This is the genuinely-"scheme" part the prompt names, and it is **closed**:

1. **The rule coupling is the V-scheme coupling (exact, rotor structure).** F151-S1: the $g_s=\tfrac12$ lock normalises the *static electric energy* — F110's $\lambda=0$ potential is exactly $V(R)=\tfrac{g^2}{2}q^2R$, and the model's kinetic term is spectral-exact so the tree Coulomb carries no lattice renormalisation. A coupling *defined through the static-source energy* **is** the static-potential (V-) scheme, by definition. This rests on the exact rotor/dielectric structure the prompt points to (F115 CM3's $g_s^2\chi=\tfrac14$ from the $(\mathbf E,\mathbf B)$ rotor stiffness).
2. **The $V\to\overline{\rm MS}$ conversion is the known exact constant.** $a_1(n_f)=(31C_A-20T_Fn_f)/9$, with $a_1(6)=\tfrac{11}3$ an exact rational (verified). It contributes $\Delta(1/\alpha)=a_1/4\pi=0.2918$, i.e. $\Lambda_V/\Lambda_{\overline{\rm MS}}=\exp(a_1/2\beta_0)=1.30$ ($n_f{=}6$).

So the **scheme** leg of Q2 — the actual change of renormalisation scheme — is **derived exactly from structure**, factor $1.299$. This is the part the prompt could in principle have found to be a free fit; it is not. Inserting it alone moves $\alpha_s(M_Z)$ from F144's converged $+8.4\%$ to $+4.4\%$.

## 4. Leg 2 — the rule$\to V$ lattice matching is the shared open $d_1$

The residual leg is $1/q_\ast a=1.365$: the rule$\to V$ matching is the **identity at tree level** (both are static-energy couplings), but carries a **one-loop lattice finite constant** — the difference between the lattice and continuum one-loop self-energies. This is *exactly* Residual A of F154, the $q_\ast$ of F151, and the finite $d_1$ of F155/F162. It is the same object Q1 (F235) and E3 (F233) reduce to. The honest content:

- **It is $O(1)$, not Wilson's $28.81$** — the rule's tadpole sector is *exactly empty* ($u_0\equiv1$, F155-A0), so $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ sits in the physical $O(1)$ band for a good action, far from Wilson.
- **It is bracketed, not pinned:** $q_\ast a\in[1/\sqrt3,0.979]$ (F155), so the open leg $1/q_\ast a\in[1.02,1.73]$ (implied $1.365$), and the full scheme factor $\in[1.33,2.25]$ (target $1.78$) — nowhere near $28.81$ (Q3 check).

### 4.1 The open leg is **vertex-dominated**, not propagator (numeric, this finding)

Using the F162 subtracted transverse coefficient $\Delta B=B_\text{lat}-B_\text{cont}$ (continuum vertices, lattice propagator), the rule's **propagator-driven** finite shift is $\Delta B_\text{rule}=-0.013$ ($n{=}12$; $-0.008$ at $n{=}16$) — about a **sixth to a tenth** of Wilson's $\Delta B_\text{wilson}=-0.079$, and $\approx0$ against the tadpole-free target. So the pull-down from the abelian/near-cutoff band top ($q_\ast\sim0.97$) to the implied $0.733$ is carried by the **vertex form-factor part**, not the propagator (Q2 check). This pins *which* diagram remains: the **lattice 3-gluon + ghost vertex form factors** on the rule/BCC action ($\cos(k/2)$-dressed $\Omega_\text{even}$ vertices, F162-G3), whose validation gate is reproducing Wilson's $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ with the full lattice vertices+tadpole. That single BZ quadrature is the one remaining perturbative-matching input.

## 5. Reconciliation with F235 ("Q1=Q2=E3=$d_1$")

F235 concluded Q1, Q2 and E3 all reduce to the one background-field constant $d_1$. F239 **sharpens this for Q2**: the scheme conversion is *two* legs, and only the **lattice$\to V$** leg is the shared $d_1$. Q2's actual **scheme** leg ($V\to\overline{\rm MS}$, factor $1.30$) is **closed exactly** and is *not* $d_1$. So the correct statement is: **Q2 $=$ (exact $V\!\to\!\overline{\rm MS}$) $\times$ (the shared open $d_1$)** — half of Q2 is derived; the open half is the same integral as Q1/E3. Pinning $d_1$ (F162 vertex form factors) closes all three simultaneously, and for Q2 delivers $\alpha_s(M_Z)=0.1180$ exactly (by construction of the implied $q_\ast$).

## 6. Checks (`test_F239_scheme_factor_factorization.py`, 2026-07-03 - 08:48)

| # | Statement | Result | Tier |
|---|---|---|---|
| Q1 | scheme conversion factorises **exactly**: $1.773=1.299(V\!\to\!\overline{\rm MS},\ a_1=\tfrac{11}3)\times1.365(1/q_\ast)$; product $=$ full to $<10^{-12}$; $\Delta$-sum $=0.638$ | PASS | exact factorisation |
| Q2 | rule propagator-driven $\Delta B_\text{rule}=-0.013$ $=$ $16\%$ of Wilson's $-0.079$ ⇒ open leg **vertex-dominated** | PASS | numeric (grid-stable) |
| Q3 | bracket $q_\ast a\in[0.577,0.979]$ ⇒ open leg $\in[1.02,1.73]$, full $\in[1.33,2.25]$ (target $1.78$); $\ll$ Wilson $28.81$; F235 refined | PASS | bracket / scope |

**Overall 3/3 PASS** (<30 s).

## 7. Ledger impact

Q2 does **not** close to the prompt's $<1\%$ acceptance as a fully-derived factor — but it is materially better than "open": the **scheme** conversion proper ($V\to\overline{\rm MS}$, $1.30$) is now **derived exactly** and separated cleanly from the one open number. Re-tag Q2 **OPEN → half-closed**: the scheme leg exact, the lattice$\to V$ leg $=$ the shared $d_1$ (bracketed $[1.02,1.73]$, implied $1.365$), closable by the single F162 vertex-form-factor integral. The falsification target is sharp and unchanged: that integral must yield $q_\ast a=0.733$ ($\Lambda$-ratio $1.78$), **not** Wilson's $28.81$ — which F155-A0's exact tadpole-emptiness makes structurally impossible.

## 8. Honest scope

- The exact factorisation is an algebraic identity of the F151 decomposition (nothing new is *computed* in Leg 1 beyond re-expressing S1$\times$S3 as a product of $\Lambda$-factors); its value is the clean *separation* of derived-scheme from open-lattice, which corrects the F235 blanket "$=d_1$".
- Leg 1's exactness inherits F151-S1's scope: the V-scheme identification is exact-symbol (static energy + tree no-renormalisation), with the numeric Coulomb shadow at the few-% level along the axis — the *claim* is exact, the numeric check is a shadow.
- The Q2 propagator/vertex split uses the F162 machinery with **continuum vertices** (lattice propagator); it therefore quantifies the *propagator* face only (correctly small for the rule) and *localises* — but does not compute — the vertex face. The absolute $b_0$-normalisation of $\Delta B$ into a q\*-shift needs the full vertex loop (the open piece), so no absolute $q_\ast$ is claimed from $\Delta B$ here; only the propagator-vs-Wilson *ratio* (grid-stable $\sim0.11$–$0.16$) is used.
- $a_1(6)=\tfrac{11}3$ uses $n_f{=}6$ at the matching scale $\mu_0$; the one-loop conversion is the honest order (two-loop conversion is negligible at $\alpha(\mu_0)\approx0.02$).

## 9. Provenance

- **New:** the exact multiplicative factorisation of the scheme conversion into (derived $V\!\to\!\overline{\rm MS}$) $\times$ (open rule$\to V=1/q_\ast$); the identification that only the lattice$\to V$ leg is the shared $d_1$ (sharpening F235); the propagator-vs-vertex split of the *open* leg via the F162 subtracted $\Delta B$ (rule $\approx0.11$–$0.16\times$ Wilson ⇒ vertex-dominated), localising the residual to the lattice 3g+ghost vertex form factors.
- **Reused:** F151-S1 (V-scheme identification, $a_1=\tfrac{11}3$) and S3 ($q_\ast$ band); F155 ($q_\ast$ bracket, A0 tadpole-empty, moment-insensitivity); F162 (`ca_bgfield_loop`: `_Bcoeff_numeric`, the $b_0=11$ gate, subtracted $\Delta B$); F144-A4 ($\Lambda$-ratio $1.78$); `ca_gluon_self_energy.B0_ALPHA`, `lambda_ratio`.
- **Verification:** `tests/findings/test_F239_scheme_factor_factorization.py` (2026-07-03 - 08:48, 3/3 PASS), results `test-results/F239_scheme_factor_factorization.json`.
