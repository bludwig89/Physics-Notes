# F54 — FG-8: End-to-end β-decay charged-current integration

**Date:** 2026-05-29 - 20:47
**Status:** Confirmed — 10/10 tests PASS (7 bit-for-bit / exact-ℚ, 3 at machine ε)
**Module:** `ca-simulation/ca_charged_current.py` (new, additive — no existing surface modified)
**Verification script:** `model-tests/test_FG8_beta_decay.py`
**Results:** `test-results/FG8_beta_decay.json`
**Closes:** first-gen-completeness.md §5.1 row **FG-8** and §7 step 5 (β-decay half)

---

## 1. Result

The signature first-generation weak process

$$d \;\to\; u + W^- \;\to\; u + e^- + \bar\nu_e$$

now runs end-to-end on the lattice as a single integrated chain, wiring together
pieces previously verified only in isolation: the left-handed SU(2)$_L$ doublet
bilinears (F29), the W-covariant Dirac doublet step and its maximal parity
violation (F34), the W-coupled quark doublet (FG-2/FG-3), dynamical and Proca-mass
W propagation (F36), and the per-species electroweak charge registry (F35/F48).
The new module adds the charged-current raising/lowering structure ($T^\pm$, $W^\pm$,
$J^\pm$) that the process requires and that was the one missing primitive.

All ten checks pass. Seven are exact (bit-for-bit, or exact over $\mathbb Q$ via
`fractions.Fraction`): the SU(2) charged-current algebra, the $d\to u$ isospin
raising, charge conservation at *both* vertices, maximal parity violation, quark–lepton
universality, the heavy-W Fermi limit at $q^2=0$, and the full-process
$\Delta Q=\Delta B=\Delta L=\Delta(B{-}L)=0$ bookkeeping. Three are dynamical and hold
at the FFT round-off floor: the W$^-$ emission identity, the Proca W$^-$ dispersion,
and the end-to-end propagation pipeline.

The headline structural identity is that the **W$^-$ field is sourced by the
raising quark current $J^+$ exactly**,

$$\Delta E(W^-) \;=\; \frac{g}{\sqrt2}\,\big(J^1 + iJ^2\big)\,\Delta t \;=\; \frac{g}{\sqrt2}\,J^+_{\rm quark}\,\Delta t ,
\qquad J^+_{\rm quark}(x) = u_L^*(x)\,d_L(x),$$

with residual $9.2\times10^{-16}$ (CC6) — i.e. the $d\to u+W^-$ vertex falls out of
the existing `w_sourced_propagation_step` machinery once the charged combination
$W^- = (W^1+iW^2)/\sqrt2$ is formed, with no new dynamics introduced.

---

## 2. Conventions

Weak-isospin generators $T^a=\tau^a/2$. The charge raising/lowering generators are

$$T^+ = T^1+iT^2 = \begin{pmatrix}0&1\\0&0\end{pmatrix},\qquad
T^- = T^1-iT^2 = \begin{pmatrix}0&0\\1&0\end{pmatrix},$$

obeying $[T^3,T^\pm]=\pm T^\pm$ and $[T^+,T^-]=2T^3=\tau^3$. A left-handed doublet
is $\psi_L=(f_{\rm up},f_{\rm down})$ in *upper-Weyl* components only (the right-handed
$\chi$ does not couple — F34/W4.3); $(\text{up},\text{down})=(\nu,e)$ for leptons,
$(u,d)$ for quarks. The site charged currents are

$$J^+(x)=\psi_L^\dagger T^+\psi_L = f_{\rm up}^*\,f_{\rm down}=J^1+iJ^2,\qquad
J^-(x)=(J^+)^*=J^1-iJ^2,$$

exactly $J^1\pm iJ^2$ of `ca_wmu.fermion_isospin_current`. The charged W mass
eigenstates are $W^\pm=(W^1\mp iW^2)/\sqrt2$, with the interaction
$\mathcal L_{\rm cc}=(g/\sqrt2)(W^+_\mu J^{+\mu}+W^-_\mu J^{-\mu})$. The $d\to u$
transition emits the $W^-$ via $J^+_{\rm quark}=u_L^*d_L$; the leptonic
$W^-\to e^-\bar\nu_e$ vertex is the conjugate $J^-_{\rm lepton}=e_L^*\nu_L$.

The Fermi limit (integrating out a heavy W, $|q^2|\ll m_W^2$):

$$\frac{G_F}{\sqrt2}=\frac{g^2}{8m_W^2},\qquad
A(q^2)=\frac{g^2}{8\,(m_W^2+q^2)},\qquad
\frac{A(q^2)-G_F/\sqrt2}{G_F/\sqrt2}=-\frac{q^2}{m_W^2+q^2}\xrightarrow{q^2\ll m_W^2}-\frac{q^2}{m_W^2}.$$

---

## 3. The module

`ca-simulation/ca_charged_current.py` exports:

| Function | Purpose |
|---|---|
| `T1,T2,T3,T_PLUS,T_MINUS`, `commutator` | isospin generators + raising/lowering |
| `su2_raising_algebra_residuals()` | CC1 algebra diagnostic |
| `raise_isospin`, `lower_isospin`, `KET_UP/DOWN` | $d\leftrightarrow u$, $\nu\leftrightarrow e$ |
| `charged_current_plus/minus(f_up,f_down)` | $J^\pm(x)=f_{\rm up}^*f_{\rm down}$, conj |
| `charged_current_from_isospin(...)` | $J^\pm=J^1\pm iJ^2$ cross-check route |
| `P_L,P_R`, `va_vertex_kills_right_handed()` | V−A projector / parity violation |
| `QUANTUM_NUMBERS`, `charge`, `baryon_number`, `lepton_number` | exact-ℚ registry (incl. $\bar\nu_e,e^+,W^\pm$) |
| `conservation_residuals(initial,final)` | exact $\Delta Q,\Delta B,\Delta L,\Delta(B{-}L)$ |
| `w_charged_components(F_W)` | $W^\pm=(W^1\mp iW^2)/\sqrt2$ |
| `emit_w_minus(E_W,B_W,f_up,f_down,...)` | $d\to u+W^-$ emission step |
| `fermi_constant`, `w_exchange_amplitude`, `fermi_limit_relative_deviation` | heavy-W limit |
| `run_beta_decay_pipeline(...)` | end-to-end integration driver (A→B) |

The module imports only already-verified primitives from `ca_wmu`
(`fermion_isospin_current`, `w_sourced_propagation_step`,
`w_massive_propagation_step_spectral`) and changes no existing surface.

---

## 4. Test results

| # | Test | Residual | Target | Status |
|---|---|---|---|---|
| CC1 | SU(2) charged-current algebra $[T^3,T^\pm]=\pm T^\pm$, $[T^+,T^-]=2T^3$ | $0.0$ | $10^{-15}$ | **PASS** (bit-for-bit) |
| CC2 | $d\to u$ raising $T^+\lvert d\rangle=\lvert u\rangle$; $\Delta Q=+1=-Q(W^-)$ | $0$ (ℚ) | $0$ | **PASS** (exact ℚ) |
| CC3 | Vertex charge conservation $d\to u+W^-$ **and** $W^-\to e^-\bar\nu_e$ | $0$ (ℚ) | $0$ | **PASS** (exact ℚ) |
| CC4 | Maximal parity violation: $P_L\psi_R=0$, $P_L\psi_L=\psi_L$ | $0.0$ | $10^{-15}$ | **PASS** (bit-for-bit) |
| CC5 | Quark–lepton universality of $J^+$ bilinear / coupling | $0.0$ | $10^{-13}$ | **PASS** (bit-for-bit) |
| CC6 | W$^-$ emission $\Delta E(W^-)=(g/\sqrt2)J^+_{\rm quark}\,dt$ | $9.2\times10^{-16}$ | $10^{-13}$ | **PASS** |
| CC7 | Proca W$^-$ dispersion $\omega^2=m_W^2+\Omega_{\rm even}^2(k)$ (3 masses × 3 comps, 30 ticks) | $3.1\times10^{-13}$ | $10^{-10}$ | **PASS** |
| CC8 | Heavy-W Fermi limit $G_F/\sqrt2=g^2/8m_W^2$ exact at $q^2=0$; rate $-q^2/(m_W^2+q^2)$ | $4.2\times10^{-17}$ | $10^{-15}$ | **PASS** (exact at $q^2{=}0$) |
| CC9 | Full process $d\to u+e^-+\bar\nu_e$: $\Delta Q=\Delta B=\Delta L=\Delta(B{-}L)=0$ | $0$ (ℚ) | $0$ | **PASS** (exact ℚ) |
| CC10 | End-to-end pipeline: causal W$^-$ arrival A→B + global charge balance | integration | — | **PASS** |

CC10 numbers: source kick $|W^-|_A=3.56\times10^{-1}$ on emission; at the distant
site B $|W^-|_B=1.6\times10^{-13}$ on emission (causally zero — the field has not
yet propagated in) rising to $2.9\times10^{-3}$ after 24 Proca ticks (signal has
arrived); global $\Delta Q=\Delta B=\Delta L=\Delta(B{-}L)=0$ exactly.

---

## 5. Physics content

1. **The charged current is purely left-handed (V−A).** CC4 confirms the vertex
   projector $P_L=(1-\gamma^5)/2$ annihilates a right-handed spinor bit-for-bit;
   combined with F34/W4.3 (right-handed $\chi$ decoupled from W) this is maximal
   parity violation built into the construction, not imposed by hand.

2. **Quark–lepton universality.** The same bilinear $J^+=f_{\rm up}^*f_{\rm down}$
   and the same coupling $g/\sqrt2$ describe the quark ($d\to u$) and lepton
   ($\nu\to e$) vertices (CC5). For one generation the CKM/PMNS mixing is the
   trivial $1\times1$ matrix $V_{ud}=1$, so no flavour factor enters.

3. **Charge, baryon, and lepton number** are each conserved *exactly* (over $\mathbb Q$)
   at both vertices and for the full process (CC2/CC3/CC9). $B-L$ is conserved, as
   it must be for a Standard-Model weak process.

4. **The Fermi theory is the heavy-W limit** of the lattice charged current (CC8):
   $G_F/\sqrt2=g^2/8m_W^2$ holds exactly at zero momentum transfer, with the
   leading correction $-q^2/m_W^2$ — the textbook propagator-expansion result,
   reproduced with no fit parameters.

5. **The whole chain is one dynamical object** (CC10): a localized quark current
   sources a $W^-$ field that propagates causally (Proca, F36) to a distant
   absorption site, where it drives the leptonic charged current — the lattice
   realisation of $n\to p\,e^-\bar\nu_e$ at the quark level.

---

## 6. Limitations / open follow-ups

- **Tier-B calibration unaddressed (by design).** Absolute rates (the β-decay
  half-life, the physical $G_F=1.166\times10^{-5}\,$GeV$^{-2}$) need the SI-unit
  identification (CO-1/F10) and calibrated $g$, $m_W$; FG-8 is the *structural*
  (Tier-A) integration test only. The $\sin^2\theta_W$ value (F45 $1/4$ vs F49
  $2/9$) does not enter the charged current, only the neutral current (F48).
- **Spin/momentum kinematics are not the V−A matrix element.** CC currents here are
  the site-local isospin bilinears; the full angular correlation of the emitted
  $e^-$/$\bar\nu_e$ (the $\beta$-spectrum shape, the Fierz term) is a separate
  observable-level test, naturally the FG-8 companion to FG-9 ($C$/$CP$ per species).
- **CKM beyond one generation** is trivially $V_{ud}=1$ here; Cabibbo mixing is a
  multi-generation extension.

---

## 7. Bottom line

FG-8 closes the β-decay charged current — and together with **FG-9** ($C$/$CP$ per
species, completed concurrently as F53) it closes the **last two open Tier-A
structural tests** of the first generation. With FG-1 (anomaly cancellation),
FG-2/3 (quark EW vertex + mass), FG-4 (dynamical $Z$), FG-5 (right-handed
hypercharge), FG-6 (two-helicity photon), FG-7 (dynamical gluons), FG-8 (β-decay
charged current), and FG-9 ($C$/$CP$) all closed, **every §5.1 Tier-A structural
test is now done.** The first generation is structurally complete as a closed,
integrated lattice model; what remains is Tier-B calibration (SI units CO-1/F10,
coupling constants, absolute masses).

**Numbering note.** This finding was developed concurrently with FG-9; both
initially took the number F53. FG-9 retains **F53** (already recorded in
changelog/project-status/memory); this β-decay finding is **F54**, with exactness
rows #142–148 (Tier 1), #54–55 (Tier 2), #27 (Tier 3) — slotted after FG-9's
reserved #136–141 / #51–53.
