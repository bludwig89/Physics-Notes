# F336 — B9's two-loop leading log cross-checked via a second construction (unitarity + dispersion) — an RG-forced consistency check, not a disjoint derivation; the Källén–Sabry non-log constant precisely scoped, not derived

**Date:** 2026-08-30 - 13:10
**Session:** `careful-diligent-sabry`
**Sector:** interactions
**Status:** Confirmed — 3/3 PASS (gate record), 1 declared control verified red on exactly the two dependent legs and nowhere else.
**Checked:** 2026-08-30 — 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/interactions/qed_twoloop_vacuum_polarization_nonlog.py`
**Test record:** `F336-twoloop-vp-nonlog-scope` (tier gate, `casim test --id F336-twoloop-vp-nonlog-scope`)
**Results:** `test-results/F336_twoloop_vp_nonlog.json`
**Cross-references:** [[F251-qed-vacuum-polarization-running-alpha]] (⚠ partially superseded by S12→[[F277-qed-gluon-refold-period]] — the refold touched only the lattice-numeric `_fermion_B` piece; the closed-form one-loop spectral function and $\Delta\alpha^{(1)}(Q^2)$ this module's calibration gate and optical-theorem normalisation are built from are on the unaffected continuum side, per F322 §9), [[F261-twoloop-qed-ae-amu]] (the sympy-exact two-loop QED β-function coefficient $b_1=1$ this module independently re-derives, and whose T1-style dispersive construction this module extends from the vertex to the two-point function), [[F252-qed-vertex-ae-lamb-shift]] (its vertex form factor is evaluated only at $q^2=0$ — the first of the two pieces §5 names as missing), [[F259-ir-bremsstrahlung]] (its real-emission calculation is scoped to the soft/eikonal limit only — the second missing piece), [[F311-gap5-three-numbers-adjudicated]] (§2.2, the first published statement of the non-log constant as *cited, not derived*), [[F322-b9-running-alpha-ew-rederived-post-f277]] (§6.1/§9, the reconciliation of the two published residuals and the explicit "not attempted" statement this session responds to), CL280 (the rubric row B9 claim card this finding narrows, not closes).

---

## 1. What this session was asked to do, and what it delivers

The session brief asked for a **derivation, not an import**, of the two-loop leptonic non-log constant

$$\Delta\alpha^{(2)}_{\ell,\text{non-log}} = \left(\frac{\alpha}{\pi}\right)^2\left[\zeta(3) - \frac{5}{24}\right]\quad\text{per lepton,}$$

which F311 §2.2 and F322 §6.1/§9 both name explicitly as the standard Källén–Sabry (1955) form, **cited, not derived here** — the same status F311 §8 states outright. The brief named F261's dispersive machinery (the Källén–Lehmann assembly that built the two-loop $g\!-\!2$ coefficient $A_2^{\rm VP}$ from F251's own spectral function) as the natural place to start extending.

**What this session establishes:** the two-loop photon self-energy $\Pi^{(2)}(s)$ does **not** admit F261's exact trick (dressing an *internal photon* with F251's bubble), because a bare one-loop fermion bubble has no internal photon propagator to dress — that shortcut is specific to the vertex, which has one. What *is* available is the **optical theorem**: cutting the three 1PI topologies that make up $\Pi^{(2)}(s)$ (a vertex correction on one leg of the loop, a self-energy insertion on the internal fermion line, and a photon exchanged across the loop) reproduces exactly the standard next-to-leading-order decomposition of the total $e^+e^-\to f\bar f(\gamma)$ cross section into a virtual piece (one-loop vertex + self-energy interfering with tree) and a real piece (the full $f\bar f\gamma$ three-body phase space). This is the *same class* of construction as F261 — a Källén–Lehmann dispersive assembly from a spectral function — one order further up, applied to $\Pi$ itself rather than to a photon line inside another diagram.

Using this route, this session:

1. **Cross-checks F261's sympy-exact two-loop leading-log coefficient $b_1=1$** — i.e. the $(\alpha/\pi)^2 L/4$ term in $\Delta\alpha^{(2)}(s)$ — via a construction (unitarity + Euclidean dispersion) whose *mechanics* share no lines of algebra with F261's original derivation (direct conversion of the classic QED $\beta$-function). This exercises new model-internal machinery on $\Pi$ itself for the first time, but the 2026-08-30 attack pass (see below) established that the **match itself is largely RG-forced, not a surprise**: the standard theorem that the first two QED $\beta$-function coefficients are scheme-independent ties $b_1$ to exactly the massless $R^{(1)}=\tfrac34\cdot\tfrac\alpha\pi$ cited in §2.3, so once both citations ($b_1=1$ and $R^{(1)}=3/4$) are accepted, the numbers agreeing is close to guaranteed arithmetic (§2.3), not new physics content. What the construction *does* newly establish — and what a bug anywhere in the chain would have broken — is that this module's own normalisation, sign conventions and dispersion-integral implementation are consistent with that RG fact.
2. **Does not derive** the non-log constant $\zeta(3)-\tfrac5{24}$.
3. **Names precisely** what a derivation needs and shows neither piece exists in the tree today (§5), converting the open target from "not attempted" (F322 §9) into two well-posed missing calculations.

---

## 2. The construction

### 2.1 The optical theorem, checked against F251 at $m\to0$

$$\operatorname{Im}\Pi(s) = \frac{\alpha}{3}R(s),\qquad R(s)\equiv\frac{\sigma(\gamma^*\to f\bar f(+\gamma))}{\sigma_{pt}}.$$

At tree level, for a unit-charge fermion pair, $R_{\rm tree}=1$ by definition of $R$ as a ratio to the point cross section. This must give $\operatorname{Im}\Pi^{(1)}(s\to\infty)=\alpha/3$ — and it does: F251's own one-loop spectral function, $(1/\pi)\operatorname{Im}\Pi^{(1)}(s)=\frac{\alpha}{3\pi}(1+2m^2/s)\sqrt{1-4m^2/s}$, tends to $\alpha/(3\pi)$ as $m/\sqrt s\to0$, i.e. $\operatorname{Im}\Pi^{(1)}\to\alpha/3$. Exact match, zero free parameters — this fixes the normalisation used below rather than assuming it.

### 2.2 Calibration gate — the dispersion machinery, validated at one loop first

Before trusting the construction at two loops, the identical machinery is validated at one loop, mirroring F261's own T1 pattern ("reproduce a known number first"). The **Euclidean** (spacelike $Q^2>0$, principal-value-free) once-subtracted dispersion relation,

$$\Delta\alpha(Q^2) = \frac{Q^2}{\pi}\int_{4m^2}^{\infty}\frac{\operatorname{Im}\Pi(s')}{s'(s'+Q^2)}\,ds',$$

evaluated numerically (Gauss–Legendre quadrature, $s'=4m^2\cosh^2\theta$ substitution — the same substitution F261's `A2_vp_dispersive` uses) with **F251's own** one-loop spectral function, reproduces F251's closed form $\Delta\alpha^{(1)}(Q^2)=\frac{\alpha}{3\pi}[\ln(Q^2/m^2)-\tfrac53]$ to $1.8\times10^{-13}$ at $Q^2/m^2=10^{12}$ — machine precision, zero free parameters (`F336-1`). Working in **Euclidean** momentum sidesteps the principal-value singularity a timelike dispersion integral would carry, and is exact for the coefficient extracted here (see §4 for why this matters for what is *not* attempted).

### 2.3 The leading-log coefficient at two loops

The standard, **cited** (not re-derived here — the same status F261 assigns its own six vertex masters) massless one-loop QED correction to the total annihilation cross section is

$$R^{(1)}_{\rm massless} = \frac34\cdot\frac{\alpha}{\pi}$$

(Appelquist–Georgi 1973 / Zee 1973 — the abelian $C_F\to1$ limit of the universally-quoted QCD "$1+\alpha_s/\pi$" K-factor: $C_F\cdot\frac34 = \frac43\cdot\frac34=1$). Feeding this through §2.1's normalisation,

$$\operatorname{Im}\Pi^{(2)}(s\to\infty) = \frac{\alpha}{3}R^{(1)}_{\rm massless} = \frac{\alpha^2}{4\pi}.$$

Re-running the **identical** dispersion quadrature from §2.2, now with this constant standing in for the (unknown, full) massive $\operatorname{Im}\Pi^{(2)}(s')$, gives the elementary closed form $\Delta\alpha^{(2)}_{\rm LL}(Q^2) = \frac{C}{\pi}\ln\!\left(1+\frac{Q^2}{4m^2}\right)$ (verified to $4.1\times10^{-13}$ against the numeric quadrature, `F336-3`), whose exact $Q^2\to\infty$ log coefficient is

$$\frac{C}{\pi} = \frac{\alpha^2}{4\pi^2} = \left(\frac{\alpha}{\pi}\right)^2\cdot\frac14.$$

This is **sympy-exact** (`F336-2`) and matches F261's independently-derived $b_1=1\Rightarrow(\alpha/\pi)^2\cdot\frac{b_1}{4}=(\alpha/\pi)^2\cdot\frac14$ identically. It also matches the leading-log coefficient reported in the literature's own asymptotic expansion of the two-loop leptonic contribution to the effective coupling (Sturm 2013, arXiv:1305.0581, the $k{=}1$ identical-flavour term $-L+\tfrac56-4\zeta_3$ in units $\frac{\alpha}{4\pi}(\alpha/\pi)$, whose $L$-coefficient converts to the same $\tfrac14$ after the sign/normalisation map worked out in §3) — a third, external confirmation. **Caveat (added in review):** this three-way agreement is largely forced rather than a coincidence — RG universality of the first two QED $\beta$-function coefficients guarantees $b_1$ equals the coefficient fixed by $R^{(1)}$, so given both citations are correct, the arithmetic above ($\tfrac13\cdot\tfrac34=\tfrac14$) was always going to close. What it actually tests is this module's own bookkeeping (normalisation, signs, the dispersion integral), not an independent physical fact.

---

## 3. Cross-check against the literature's own asymptotic form

Sturm (arXiv:1305.0581) gives the identical-flavour two-loop asymptotic term as $\frac{\alpha}{4\pi}\left(\frac\alpha\pi\right)\left[-L+\frac56-4\zeta_3+O(m^2/q^2)\right]$ (their $L=\ln(-q^2/M^2)$, spacelike). At **one loop** the same paper's term $\frac{\alpha}{4\pi}\left[-\frac43 L+\frac{20}9\right]$ equals $-\frac{\alpha}{3\pi}L+\frac{5\alpha}{9\pi} = -\Delta\alpha^{(1)}_{F251}$, i.e. their convention is $\Delta\alpha=-\Pi_{\rm paper}$ (an overall sign flip from this module's / F251's convention). Applying the **same** sign flip at two loops:

$$\Delta\alpha^{(2)} = -\left(\frac\alpha\pi\right)^2\left[-\frac L4+\frac14\left(\frac56-4\zeta_3\right)\right] = \left(\frac\alpha\pi\right)^2\left[\frac L4+\zeta_3-\frac5{24}\right],$$

which is **exactly** the full Källén–Sabry form F311/F322 cite, log **and** constant together. This is a valuable independent confirmation that the cited constant is correct and that this module's sign/normalisation conventions are self-consistent with an external, verifiable source; it is **not** a derivation of the constant — the constant is read off Sturm's own asymptotic expansion, not built from anything in this model's tree (§4).

---

## 4. What is not attempted, and why (the non-log constant)

The non-log constant is **not derived here**. Two things distinguish this from a bare citation:

**(a) The constant needs two calculations that do not exist in the tree.** By the same unitarity decomposition used in §2, the finite ($s$-independent, as $s\to\infty$) remainder of $\Pi^{(2)}$ requires the finite part of $2\,{\rm Re}(\text{one-loop vertex} + \text{one-loop self-energy})$ interfering with tree **at general timelike $s$**, plus the **full** (hard-photon-included, not merely soft) $f\bar f\gamma$ three-body phase-space integral. Neither exists:

- F252 (`qed_vertex_loop.py`) evaluates the vertex **only** at $q^2=0$ — the Schwinger term $a_e=\alpha/2\pi$ (its V2). There is no general-$s$ form factor in the tree.
- F259 (`qed_ir_bremsstrahlung.py`) computes **only** the soft (eikonal, $k\to0$) limit, and its own honesty ledger states this explicitly: *"a full YFS resummation and hard-collinear (non-soft) real emission are out of scope"* (F259.md, "Scope and honesty").

**(b) There is a structural reason the Euclidean machinery of §2.2–2.3 cannot be repurposed for the constant.** The leading-log coefficient is a single power of a real momentum-space logarithm, and is continuation-safe: its value is the same whether read off in Euclidean or timelike kinematics. A **constant** term is not — continuing a two-loop expression from spacelike to timelike ($\ln(-s-i\epsilon)\to\ln s - i\pi$) can mix $\ln^2\to-\pi^2$ pieces into what was, in Euclidean space, a pure constant. So even a hypothetical "just read the constant off the same integral" attempt would not safely reproduce the timelike physical constant without the genuine unitarity/timelike calculation — it is not simply that (a)'s two calculations are tedious, but that the Euclidean shortcut this module otherwise relies on is specifically unavailable for this piece.

This converts the open target from a generic "F261's dispersive machinery, not attempted" (F322 §9) or "cited, not derived" (F311 §8) into two named, well-posed calculations for a follow-up session, plus the explicit warning in (b) that a naive continuation is not a safe substitute for doing them.

---

## 5. Verification summary (3/3, 1 control)

| leg | check | type | result |
|---|---|---|:---:|
| F336-1 | Euclidean dispersion integral of F251's own $\operatorname{Im}\Pi$ reproduces F251's closed-form $\Delta\alpha^{(1)}(Q^2)$, zero free parameters | machine precision | $1.8\times10^{-13}$ |
| F336-2 | $\operatorname{Im}\Pi=(\alpha/3)R(s)$ checked exactly at $m\to0$ vs. F251; cited $R^{(1)}$ gives leading-log coefficient $(\alpha/\pi)^2/4$ | exact (sympy) | matches F261's $b_1=1$ identically |
| F336-3 | the **same** dispersion quadrature as F336-1, given a constant $\operatorname{Im}\Pi^{(2)}$, reproduces the elementary closed form; its exact $C/\pi$ matches F261's fixed reference | machine precision | $4.1\times10^{-13}$ (quadrature); exact match (reference) |

**Control (D9/H2), measured not expected:**

| perturbation | reddens | why it must |
|---|---|---|
| `R1_control: 1` (replaces the cited $\tfrac34$ with a wrong coefficient) | **F336-2, F336-3** | both legs read the perturbed $R_1$ into their leading-log coefficient, which then no longer matches F261's fixed $b_1=1$ reference |

`F336-1` never reads `R1_control` (it is the one-loop calibration gate, using only F251's own spectral function), so its red set is disjoint from the control by construction — verified, not assumed: `casim test --id F336-twoloop-vp-nonlog-scope --control` reports the control reddening exactly `['F336-2', 'F336-3']` of 3 legs. `can-fail` traced by execution (`tools/check_control_soundness.py --can-fail`): CAN FAIL, journalled.

---

## 6. What this closes, and what it does not

**Closed:** nothing in the sense of removing a residual — B9's numbers ($0.0495\%$ model-internal, $0.00158\%$ after the Källén–Sabry import, F322 §6.1) are **unchanged**. B9 stays `QUANT`.

**New model-internal content:** the two-loop leading-log coefficient $(\alpha/\pi)^2/4$ (equivalently F261's $b_1=1$) now has a **second, mechanically different check** — F261's direct QED $\beta$-function conversion, and this session's unitarity/dispersion construction — that agree exactly. As the 2026-08-30 attack pass established (see below), this agreement is largely RG-forced given both external citations ($b_1=1$, $R^{(1)}=3/4$) are correct, so the honest framing is a **citation-consistency and implementation check**, not two disjoint physical derivations of the same number: a bug in this module's normalisation, sign convention, or dispersion integral would still have broken the match, and none did — that is what the check is actually worth. A mismatch would have been "a genuinely interesting discrepancy worth its own finding", per the session's own falsification criterion; there is none.

**Not closed, stated rather than absorbed:** the non-log constant $(\alpha/\pi)^2[\zeta(3)-\tfrac5{24}]$ per lepton remains **cited, not derived** on the model's own fields. §4 narrows this from a generic "not attempted" to two named, missing calculations (F252 at general $s$; F259's hard-photon phase space) plus a structural reason (§4(b)) the Euclidean shortcut used for the leading log cannot be repurposed for the constant. A future session attempting (a) should treat a value differing from $\zeta(3)-\tfrac5{24}$ by more than a few percent as a genuinely interesting discrepancy, not a bug to paper over — exactly the session brief's own falsification criterion.

---

## 7. Honest scope

- **Exact:** the optical-theorem normalisation check at $m\to0$ (F336-2's `one_loop_calibration_ok`); the sympy identity that the two-loop leading-log coefficient derived here equals F261's $(\alpha/\pi)^2\cdot b_1/4$ with $b_1=1$.
- **Machine precision, zero free parameters:** the one-loop Euclidean dispersion calibration gate (F336-1, $1.8\times10^{-13}$); the two-loop leading-log quadrature-vs-elementary-closed-form check (F336-3, $4.1\times10^{-13}$).
- **Cited, not re-derived (same status as F261's six vertex masters):** the massless one-loop QED correction to the total cross section, $R^{(1)}_{\rm massless}=\tfrac34\cdot\tfrac\alpha\pi$ (Appelquist–Georgi 1973 / Zee 1973).
- **External cross-check, not a model derivation:** §3's match against Sturm (arXiv:1305.0581)'s own asymptotic expansion, which independently confirms the full Källén–Sabry form (log and constant) is correctly stated by F311/F322 — but that confirmation reads the constant off Sturm's paper, not off anything in this model's tree.
- **Not derived, precisely scoped:** the non-log constant itself (§4). Nothing in this module computes it; §4 exists to make the missing calculation concrete rather than to substitute for it.

---

## Reviewed & corrected

**2026-08-30 - 13:45** — attack pass: **CONFIRMED-NARROWER**. Found: (1) the finding's "independent
construction / shares no algebra" framing overclaimed — the leading-log match is largely RG-forced
given both external citations ($b_1{=}1$, $R^{(1)}{=}3/4$) are correct, since the first two QED
$\beta$-function coefficients are scheme-independent by a standard theorem, so the two "independent
legs" (§1, §2.3, §6) are really a citation-consistency and implementation check, not two disjoint
physical derivations; (2) F251 was cited nine times (cross-references line, module docstring/comments)
with no disclosure that it carries S12's `⚠ partially superseded → F277` flag, unlike the disclosure
pattern F322 §9 uses for the same citation. Fixed: reworded the title, §1 item 1, §2.3's closing
sentence, and §6's "new model-internal content" paragraph to state the RG-forced nature of the match
plainly, framing the genuine content correctly as *this module's own normalisation/sign/implementation
consistency*, not new physical independence; added the S12→F277 supersession annotation to the
cross-references line and a corresponding note to the module docstring, confirming (per F322 §9 and
`docs/theory/supersessions.yaml`) that the specific F251 pieces reused here (the closed-form spectral
function and $\Delta\alpha^{(1)}(Q^2)$) are on the refold's unaffected continuum side, not the corrected
lattice-numeric `_fermion_B` term. Rejected: none — both defects were verified directly (RG-universality
algebra re-checked by hand; supersession status re-checked against `supersessions.yaml` and F322 §9) and
both were real. Deferred: none — no further physics run needed, both were prose/citation-hygiene fixes.
All 3 gate legs and the control still verify unchanged after the edit (no code or test-record touched).

## Files
- Module: `src/casim/engine/interactions/qed_twoloop_vacuum_polarization_nonlog.py`
- Registry: `src/casim/engine/registry.py` (Module entry `interactions.qed_twoloop_vacuum_polarization_nonlog`)
- Test: `tests/registry/interactions.yaml`, record `F336-twoloop-vp-nonlog-scope` (gate tier, 3/3 PASS, 1 control verified `CONTROL`)
- Results: `test-results/F336_twoloop_vp_nonlog.json`
- Can-fail journal: `test-results/can-fail.json`
