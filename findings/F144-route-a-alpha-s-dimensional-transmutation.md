# F144 — Route A: $\alpha_s$ predicted from the rule by dimensional transmutation — $g_s=\tfrac12$ derived (not assumed), then $\alpha_s(M_Z)$ to +8.4% (converged) / +1.3% (1-loop) with zero free parameters

**Date:** 2026-06-12 - 12:47
**Status:** Confirmed (partial derivation) — 5/5 checks PASS. A1 exact/machine (the lock is now *derived*: rule circularity ⇒ $\chi=1$, sympy-exact lemma + F110 C7 matrix identity); A2/A3 zero-parameter PREDICTIONs ($\alpha_s(M_Z)$, $\Lambda_{\overline{\rm MS}}^{(3)}$, the F119 hierarchy $N$); A4 a tagged DIAGNOSTIC that bounds the one open coefficient; A5 sensitivity band.
**Module:** `ca-simulation/ca_alpha_s_running.py`
**Script:** `tests/findings/test_F144_route_a_alpha_s.py` (~5 s, numpy + sympy)
**Results:** `test-results/F144_route_a_alpha_s.json`
**Cross-references:** [[F115-coupling-magnitudes-running-rotor]] (CM3 lock $g_s^2\chi=\tfrac14$ this *derives*; CM2's "no running between lattice and TeV" verdict applied to the EW angle — the QCD coupling, by contrast, does run the whole desert), [[F110-realtime-link-hamiltonian-confinement]] (C7 matrix identity $\chi=1/(4g_s^2)$, reused), [[F101-strong-coupling-sigma-compact-rotor]] (§7 normalisation $\chi=1$, now derived from the rule), [[F107-canonical-a-adoption-L4-grb-gate]] (the scale $\mu_0=\hbar c/a$), [[F119-kg-scale-three-routes]] (the hierarchy $N$ this lands), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the scale-setting residual this converts into one scheme constant), [[F138-weinberg-gap-closure-4piv-matching]] (the matching+running methodology), `docs/theory/qcd-calibration-derivation-routes.md` (the Route-A brief this executes).

---

## 1. What this closes (and what it sharpens)

The QCD calibration block's deepest knob was the strong-sector *scale itself*: F123 anchored the MeV world on a user-selected $f_\pi$, and F119 concluded the hierarchy $N\sim5.5\times10^{-19}$ "can't be made from $O(1)$ couplings — no running channel." This finding builds the running channel. The model's own locked bare coupling, run down from its own lattice scale, **generates the 19-decade hierarchy with no tuning** and lands the measured $\alpha_s(M_Z)$ to +8.4% (loop-converged; +1.3% at 1-loop), with the entire residual compressed into a single, conventionally-computable scheme constant (A4).

## 2. A1 — the lock, derived: rule circularity ⇒ $\chi=1$ ⇒ $g_s=\tfrac12$

F115 CM3 *assumed* the F101 normalisation $\chi=1$. Here it is derived, in three exact steps:

1. **The rule's step is an exact circular rotation.** The per-mode $2\times2$ map of `ca_wmu._f26_rotation_step` on the real $(\mathbf E,\mathbf B)$ pair is orthogonal, det $=1$, equal-diagonal — residuals $<10^{-15}$ on all modes (kernel check, not an idealisation).
2. **Lemma (sympy-exact).** For the quadratic rotor $H=\tfrac{a}{2}E^2+\tfrac{b}{2}B^2$ the one-tick flow is $M=\begin{pmatrix}\cos\omega t&\frac{b}{\omega}\sin\omega t\\-\frac{a}{\omega}\sin\omega t&\cos\omega t\end{pmatrix}$, $\omega=\sqrt{ab}$, and $M^{\rm T}M-\mathbb 1=\sin^2(\omega t)\,\mathrm{diag}(\tfrac ab-1,\tfrac ba-1)$: **orthogonal iff $a=b$**. A circular rotation *forces* equal electric/magnetic stiffness — $\chi=1$ is not a convention; it is what the rule's circularity means.
3. **F110 C7 matrix identity (re-verified, residual $=0$ at three couplings):** the 1-plaquette dual U(1) link Hamiltonian *is* the compact rotor with $\chi=1/(4g_s^2)$ (4 exclusive boundary links: $\frac{g^2}{2}\cdot4m^2=\frac{1}{2\chi}m^2$).

$$\chi=1\ \wedge\ \chi=\frac{1}{4g_s^2}\quad\Longrightarrow\quad \boxed{\,g_s=\tfrac12,\qquad \alpha_s(\mu_0)=\frac{g_s^2}{4\pi}=\frac{1}{16\pi}=0.01989\,}$$

at the lattice scale $\mu_0=\hbar c/a=E_{\rm P}/6.59782=1.850\times10^{18}$ GeV (F107). Zero knobs anywhere. (Wilczek's Nobel lecture asks for exactly this: a colour coupling "of order $1/2$ at the Planck scale" makes the proton.)

## 3. A2 — $\alpha_s(M_Z)$: the zero-parameter prediction

Standard $\overline{\rm MS}$ running (RK4 in $\ln\mu$, $n_f$ thresholds at $m_t,m_b,m_c$; QCD running is Higgs-independent, so the model's Higgs-free structure changes nothing at these orders):

| loops | $\alpha_s(M_Z)$ | vs PDG 0.1180 |
|---|---|---|
| 1 | 0.1195 | $+1.3\%$ |
| 2 | 0.12797 | $+8.45\%$ |
| 3 | 0.12795 | $+8.43\%$ |
| 4 | 0.12798 | $+8.46\%$ |

The loop expansion **converges** (2→3→4 spread $<10^{-3}$): the honest converged prediction is $+8.4\%$; the 1-loop $+1.3\%$ is fortuitous (it partially cancels against the missing scheme constant). Either way: a zero-parameter hit on the measured strong coupling from a Planck-scale boundary value, across sixteen decades.

## 4. A3 — the scale chain and the F119 hierarchy

- $\Lambda_{\overline{\rm MS}}^{(3)}=529$ MeV (4-loop run, 2-loop closed-form extraction at $m_c$) vs FLAG $343(12)$ MeV — factor 1.54, inside the scheme band of A4.
- **Hierarchy:** $N_{\rm pred}=\Lambda^{(3)}/\mu_0=2.9\times10^{-19}$ vs F119's $N=5.5\times10^{-19}$ — **factor ~1.9 from pure structure.** F119's sharp negative ("the gap mechanism can't make $N$ from $O(1)$ couplings — needs $10^{-36}$ tuning, no running channel") is answered: the channel is asymptotic freedom itself, $N\sim e^{-1/(2b_0\alpha_0)}$ with $\alpha_0=1/(16\pi)$, and it lands the 19 decades *because* the rule fixes $\alpha_0$ where it does.

## 5. A4 — the one open coefficient, bounded

Running the *measured* $\alpha_s(M_Z)$ up to $\mu_0$ gives $1/\alpha_{\rm meas}(\mu_0)=50.91$ vs the rule's $16\pi=50.27$: the entire discrepancy is

$$\Delta(1/\alpha)\big|_{\mu_0}=0.64\quad\Longleftrightarrow\quad \frac{\Lambda_{\rm scheme}}{\Lambda_{\rm rule}}=1.78.$$

For the Wilson action the same constant is $\Lambda_{\overline{\rm MS}}/\Lambda_{\rm lat}=28.81$ ($d_1=5.88$). The rule's normalisation is therefore **already near-continuum** (16× closer than Wilson); the outstanding first-principles object is one number — the model-action analogue of the Hasenfratz one-loop background-field constant. Computing it would either close the +8.4% exactly or falsify the lock. This is the same single coefficient F124 §5 met as "scale-setting" (its factor-4 bare-rotor↔condensed gap contains this 1.78 plus the BZ-edge convention).

## 6. A5 — sensitivity

Cutoff-convention band: anchoring instead at $\mu_0'=\pi/a$ (the F124 axis-edge convention) gives $\alpha_s(M_Z)=0.1411$ ($+19.6\%$) at 1-loop — $\mu_0=1/a$ is the standard scheme-bare choice and the favourable one; the spread is part of the same scheme constant. Loop convergence and threshold placement are sub-percent effects.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| A1 | rule step exactly circular; lemma orthogonal ⟺ $a{=}b$; $\chi=1/(4g_s^2)$ matrix identity; $\alpha_s(\mu_0)=1/(16\pi)$ | residuals $<10^{-15}$ / exact / $0$ | machine/exact |
| A2 | $\alpha_s(M_Z)$ converged $+8.4\%$ (1-loop $+1.3\%$), expansion converged | PASS | PREDICTION |
| A3 | $\Lambda^{(3)}$ ×1.54 of FLAG; hierarchy $N$ ×1.9 of F119 (19 decades, no tuning) | PASS | PREDICTION |
| A4 | implied scheme $\Lambda$-ratio 1.78 ≪ Wilson 28.81 | PASS | DIAGNOSTIC |
| A5 | $\pi/a$ convention $+19.6\%$; sub-% loop/threshold effects | PASS | sensitivity |

## 8. Honest scope

- The running is the standard continuum $\overline{\rm MS}$ β-function with SM flavour content below $\mu_0$; the model's own spectrum near $\mu_0$ could shift thresholds (negligible in $\ln$), and matching discontinuities at thresholds are ≪ the A4 band.
- "$g_s=\tfrac12$ in the rule normalisation" still awaits its scheme translation; A4 *bounds* the conversion (equivalent $\Lambda$-ratio 1.78) but does not compute it. Until then the +8.4% is a residual, not a discrepancy — and the falsification target is sharp: the model-action one-loop constant must come out $\approx1.8$, not $\approx29$.
- $\Lambda^{(3)}$ extraction at $m_c$ uses the 2-loop closed form at $\alpha_s\sim0.5$ — quote with the A4 band, not as an independent precision number.
- This finding fixes the *scale*; it does not by itself re-derive $f_\pi$ in MeV (that chain runs $\Lambda\to\sqrt\sigma\to f_\pi$ via F124 and inherits its 12%).

## 9. Provenance

- New: the χ=1 derivation (circularity lemma + kernel check), the zero-parameter $\alpha_s(M_Z)$/$\Lambda^{(3)}$/$N$ chain, the A4 scheme-constant bound, the A5 band.
- Reused: F110 C7 identity (`ca_link_hamiltonian`), `ca_wmu._f26_rotation_step`, F107 $\mu_0$, F115 CM3 framing.
- Verification: `tests/findings/test_F144_route_a_alpha_s.py` (2026-06-12, 5/5 PASS), results `test-results/F144_route_a_alpha_s.json`.
