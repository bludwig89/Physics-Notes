# F151 — The shared scheme/scale constant determined: $\alpha_\text{rule}=\alpha_V$ (tree-exact), the one-loop conversion is the known $a_1=\tfrac{11}{3}$, and the residual is a matching scale inside a derived band — with $\Lambda^{(3)}_{\overline{\rm MS}}$ corroborating to 1.1%

**Date:** 2026-06-12 - 13:55
**Status:** Confirmed (constant determined to one bounded scale choice) — 5/5 checks PASS. S1 exact (scheme identification + $a_1$ rationals); S2 machine (Wilson-tadpole contrast); S3 zero-parameter PREDICTION band **bracketing** the data; S4 the independent $\Lambda^{(3)}$ corroboration; S5 supporting numerics + the IR-face refinement.
**Module:** `ca-simulation/ca_scheme_constant.py`
**Script:** `tests/findings/test_F151_scheme_constant.py` (~2 min, numpy)
**Results:** `test-results/F151_scheme_constant.json`
**Cross-references:** [[F144-route-a-alpha-s-dimensional-transmutation]] (A4 — the implied $\Lambda$-ratio 1.78 this decomposes and derives), [[F145-route-c-induced-njl-coupling]] (N5 — the IR face, here refined into a separate object), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the scale-setting residual this absorbs), [[F110-realtime-link-hamiltonian-confinement]] (the $\lambda=0$ static energy that *defines* the scheme), [[F115-coupling-magnitudes-running-rotor]]/[[F116-njl-calibration-bz-cutoff-induced-G]] (upstream locks), `docs/theory/qcd-calibration-derivation-routes.md`.

---

## 1. What "the single number" turned out to be

F144-A4, F145-N5 and F124 §5 each met one unknown constant — a scheme conversion, an IR coupling, a scale-setting factor — conjectured to be a single shared object. This finding determines it. The answer has structure:

$$\Delta(1/\alpha)\Big|_\text{needed}=0.640\;=\;\underbrace{\frac{a_1(6)}{4\pi}=0.292}_{\textbf{derived, exact}}\;+\;\underbrace{2b_0^{(\alpha)}\ln\frac{1}{q_\ast a}=0.348}_{\textbf{a matching scale, bounded}}$$

with $q_\ast=0.7327/a$ implied by the data, inside the derived band $[1/\sqrt3,\,1]/a$. The wildcard of F144 — an unknown that for the Wilson action is a factor $28.81$ — is now: one *exactly known* constant plus one scale choice confined to a factor $\sqrt3$ window.

## 2. S1 — the scheme identification (exact)

**The rule's coupling is the V-scheme coupling.** Two exact facts:

1. The F144 lock $g_s^2=\tfrac14$ normalises the **static electric energy**: F110's $\lambda=0$ potential is $V(R)=\tfrac{g^2}{2}q^2R$, re-verified integer-exact here (dev $0.0$). A coupling *defined* through the energy of static sources is, by definition, the static-potential (V-) scheme.
2. The model's Gauss/constraint sector is spectral-exact, so the tree-level Coulomb carries **no lattice renormalisation** (S5a: the exact-symbol Green's function reproduces the continuum $1/4\pi R$ in an image-corrected difference test, $<5\%$ and improving with $R$ — the numeric shadow of an exact symbol statement).

Therefore the one-loop conversion to $\overline{\rm MS}$ is not an unknown — it is the **known static-potential constant**

$$a_1(n_f)=\frac{93-10n_f}{9}\ \ \text{(exact rationals)},\qquad a_1(6)=\frac{11}{3},\qquad \Delta(1/\alpha)=\frac{a_1}{4\pi}=0.2918,$$

equivalently $\Lambda_V/\Lambda_{\overline{\rm MS}}=e^{a_1/2\beta_0}=1.30$ ($n_f{=}6$) / $1.48$ ($n_f{=}3$) / $1.60$ ($n_f{=}0$). Inserting it: $\alpha_s(M_Z)$ moves from $+8.46\%$ (F144) to $+4.43\%$ — the exactly-derivable half of the constant.

## 3. S2 — why the model's constant is small (the Wilson contrast)

The Wilson-action 28.81 is dominated by the compact-link **tadpole** (the integral $Z_0=\int_\text{BZ}\frac{d^4k}{(2\pi)^4}\frac1{\hat K}=0.154933$, reproduced here to $3\times10^{-5}$). The rule's lock is taken on the exact spectral quadratic form — no compact-link expansion enters the coupling's definition anywhere — so the tadpole term is **structurally absent**. This is the *reason* F144-A4 found a near-continuum 1.78 instead of 29: the model's normalisation is tadpole-free by construction.

## 4. S3 — the band brackets the data (zero free parameters)

The remaining ambiguity is the scale $q_\ast$ at which $\alpha_V(q_\ast)=\tfrac1{16\pi}$. The model's geometric conventions (cutoff wavenumber vs rotation-rate/$c_\text{lat}$ conventions, BCC cell vs NN distance) span $q_\ast\in[1/\sqrt3,\,1]/a$. Over that band:

$$\alpha_s(M_Z)\in[0.1143,\ 0.1232]\qquad\text{— PDG }0.1180\ \textbf{inside}.$$

For the first time the zero-parameter chain *brackets* the measured strong coupling rather than missing it on one side.

## 5. S4 — the determination and its independent corroboration

Fixing $q_\ast$ by $\alpha_s(M_Z)$ **alone**: $q_\ast=0.7327/a$ — in the band, $3.6\%$ below the geometric mean $3^{-1/4}/a=0.7598$ (recorded as an observation, not a derivation). The corroboration is that a *second, independent* observable then lands:

$$\Lambda^{(3)}_{\overline{\rm MS}}=347\ \text{MeV}\quad\text{vs FLAG }343(12)\ \text{MeV}\ \ (\times1.011),\qquad N=\Lambda^{(3)}/\mu_0=1.87\times10^{-19}.$$

(At the geometric-mean point with nothing fitted at all: $\alpha_s(M_Z)=0.1186$ ($+0.50\%$), $\Lambda^{(3)}=356$ MeV ($\times1.04$).) The F124 scale chain inherits this directly: with $\Lambda^{(3)}$ on FLAG, the empirical $\sqrt\sigma/\Lambda^{(3)}$ puts $\sqrt\sigma\approx451$ MeV vs the physical $\sim445$ — the F124 12% residual is absorbed by the same constant.

## 6. S5 — the IR face, refined (honest correction to F144/F145)

The self-consistent resolved gap (F145 kernel, $M(0)=1.50$ = the F77 constituent mass) requires $\alpha_\text{eff}^\ast=0.376$ ($m_D{=}0.532$) / $0.411$ ($m_V{=}0.727$) — sharp and stable ($\pm5\%$ across the MC spread). But locating it on the perturbative running is pole-dominated and unreliable; it is **not** the same number as the UV constant. The "one shared number" conjecture of F144/F145 therefore *refines*: the UV faces (F144-A4 scheme constant, F124 scale-setting) collapse onto $(a_1\ \text{exact})+(q_\ast\ \text{in the band})$ — now determined; the IR face ($\alpha_\text{eff}^\ast\approx0.39$, the strong-coupling crossover) is a distinct nonperturbative target, connected through the full running but not identical.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| S1 | $V(R)=\tfrac{g^2}{2}q^2R$ exact (dev $0.0$) ⇒ V-scheme; $a_1=(93-10n_f)/9$ exact, $a_1(6)=\tfrac{11}{3}$ | PASS | exact |
| S2 | Wilson tadpole $Z_0=0.154933$ reproduced ($3\times10^{-5}$); structurally absent from the lock | PASS | machine |
| S3 | band $[1/\sqrt3,1]/a$: $\alpha_s(M_Z)\in[0.1143,0.1232]$ ∋ PDG; $a_1$ alone $+8.46\%\to+4.43\%$ | PASS | PREDICTION |
| S4 | implied $q_\ast=0.7327/a$ in band ($-3.6\%$ vs $3^{-1/4}$); $\Lambda^{(3)}=347$ vs FLAG $343(12)$ ($\times1.011$) | PASS | corroboration |
| S5 | spectral Coulomb $<5\%$ (R-improving); IR $\alpha_\text{eff}^\ast=0.376/0.411$ stable — separate target | PASS | supporting |

## 8. Honest scope

- $q_\ast$ is **implied**, not derived: the first-principles closure is the one-loop background-field LPT computation on the model's BCC action, whose result must land at $0.733/a$ (equivalently reproduce $\alpha_s(M_Z)=0.1180$) — a sharp falsification target now confined to a $\sqrt3$ window. The proximity to $3^{-1/4}/a$ ($-3.6\%$) is suggestive (the F107 cell itself carries $3^{1/4}$) but is *not* claimed as a derivation.
- The $a_1$ conversion is one-loop; at $\alpha(\mu_0)\approx0.02$ the two-loop conversion term is negligible, so the band, not loop order, dominates the honest uncertainty.
- The V-scheme identification rests on the static-energy definition of the lock (exact) plus the tree no-renormalisation of the constraint sector (exact symbol; numeric check at the few-% level along the axis direction, limited by BZ-truncation oscillations, not by the claim).
- $N=1.9\times10^{-19}$ vs F119's $5.5\times10^{-19}$: different definitions ($\Lambda^{(3)}/\mu_0$ vs $m_\text{lat}(\tau)$ for the fermion scale); the 19-decade magnitude is the shared content.

## 9. Provenance

- New: the V-scheme identification of the lock; the $a_1$ insertion; the tadpole-contrast explanation of the small constant; the $q_\ast$ band + bracketing; the implied $q_\ast$ and the $\Lambda^{(3)}$ corroboration; the IR-face refinement.
- Reused: F110 $\lambda=0$ exactness, F144 chain machinery, F145 kernel (IR face), known QCD constants ($a_1$, $Z_0$, FLAG).
- Verification: `tests/findings/test_F151_scheme_constant.py` (2026-06-12, 5/5 PASS), results `test-results/F151_scheme_constant.json`.
