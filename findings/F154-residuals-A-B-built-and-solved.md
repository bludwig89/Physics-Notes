# F154 — Building and solving the two strong-sector residuals: **Residual B is solved** (the self-consistent gap fixes the IR coupling $\alpha_\text{eff}^\ast=0.376/0.411\approx0.39$, converged and $L$-stable, reproducing F151-S5 from first principles); **Residual A's cheap route fails** ($q_\ast$ is a UV-finite lattice−continuum subtraction, not a propagator log-moment — the full one-loop integral remains)

**Date:** 2026-06-12 - 19:30
**Status:** Partial (one residual solved, one residual's shortcut ruled out) — 5/5 checks PASS. **B (solved):** the full **nonlinear** self-consistent gap equation $M(k)=m_0+24\langle G_S(k{-}q)M(q)/\sqrt{K{+}M^2}\rangle$ — built here, not in F145 (which only had the *linearised* $M\!\to\!0$ eigenvalue) — converges, with the coupling fixed by the physical constituent mass $M(0)=1.50$ (=311 MeV, F77/F124), to $\alpha_\text{eff}^\ast=0.376$ ($m_D{=}0.532$) / $0.411$ ($m_V{=}0.727$): **identical to F151-S5/F152 to 3 digits**, now as a converged ($\sim130$-iteration) fixed point that is $L$-stable ($0.3764$ at $L{=}16/24/32$). The naive perturbative running ($\Lambda^{(3)}=347$ MeV) **overshoots** to $M(0)\approx1400$–$1570$ MeV, confirming the deep-IR running is unreliable (the IR coupling is genuinely a distinct nonperturbative object, not the frozen running). **A (cheap route fails, honest negative):** with the V-scheme + exact $a_1=\tfrac{11}3$ already fixed (F151), the only residual is the matching scale $q_\ast$. Its natural shortcut — the gluon-propagator **log-moment** over the BZ — does **not** pin it: the converged moments are *UV* scales ($\langle\ln K\rangle_\text{4D}=2$ exactly $\Rightarrow q_\ast^\text{bare}=e/a=2.72/a$; the $1/K$-weighted $=2.30/a$), all **above** F151's band $[1/\sqrt3,1]/a$, while the only weight that reaches the band ($1/K^2$) is IR-divergent and grid-dependent ($1.01\!\to\!0.65$ as $n{:}24\!\to\!64$). The lesson is physical: $q_\ast$ is the **UV-finite lattice−continuum subtraction** (the true $d_1$ integral), not a bare moment — so **A still requires the full one-loop background-field computation**, exactly as F151 §8 said. **Coupling of the two:** B fixes the *dimensionless* gap physics ($\alpha_\text{eff}^\ast\leftrightarrow M(0)$); removing B's mass anchor entirely needs the *absolute scale*, which **is** A — so the last freedom is one scale, and it sits in the one integral A names. See §6.
**Modules:** `ca-simulation/ca_gap_solve.py` (B), `ca-simulation/ca_qstar_logmoment.py` (A); reuse `ca_njl_induced_coupling.py` (F145), `ca_scheme_constant.py` (F151).
**Script:** `tests/findings/test_F154_residuals_A_B.py` (~3 min, numpy)
**Results:** `test-results/F154_residuals_A_B.json`
**Cross-references:** [[F152-ir-coupling-the-irface]] (the IR-face value $\alpha_\text{eff}^\ast\approx0.39$ this **solves for**), [[F151-scheme-constant-determined]] (the UV face: V-scheme + $a_1$ + the $q_\ast$ band/implied $0.733$ this attacks; S5 the IR value reproduced), [[F145-route-c-induced-njl-coupling]] (the linearised gap eigenvalue + Fierz $2/9$ + running this extends to the full nonlinear solve), [[F77-njl-gap-rpa-selfconsistent]] (the constituent mass $M=311$ MeV anchor; $G/G_c=1.277$ linearised), [[F88-colour-condensate-from-model]] / [[F117-gap-coupled-dielectric-gluon-propagator]] ($m_D=0.532/0.727$), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the scale-setting = A; the exact Pagels–Stokar $f_\pi$), [[F144-route-a-alpha-s-dimensional-transmutation]] (the running used in the overshoot test), `docs/status/qcd-ir-coupling-problem-status.md` (the A/B problem statement this executes).

---

## 1. The two residuals, restated

The strong-sector scale problem reduces (per `qcd-ir-coupling-problem-status.md`) to two computations: **A** = the UV matching scale $q_\ast$ (one one-loop lattice integral; F151 fixed everything around it but left $q_\ast$ "implied" at $0.733/a$), and **B** = the IR gap-saturated coupling $\alpha_\text{eff}^\ast\approx0.39$ (one self-consistent gap solve; F151-S5/F152 stated the value but did not expose the solve). This finding builds both and reports honestly which closed.

## 2. B — the self-consistent gap solve (SOLVED)

F145 had only the **linearised** criticality eigenvalue $R=G/G_c$ (the $M\!\to\!0$ limit). The physical condensate needs the **full nonlinear** equation, with the dynamical mass kept in the quasiparticle energy:

$$M(k)=m_0+24\;\Big\langle\, \frac{(2/9)\,g^2/2}{\varepsilon_c K(k{-}q)+m_D^2}\;\frac{M(q)}{\sqrt{K(q)+M(q)^2}}\,\Big\rangle_q ,\qquad 24=4_{\rm Dirac}\times3_{\rm colour}\times2_{\rm flavour}.$$

Solved by FFT convolution + under-relaxed iteration to a fixed point. **Inverse solve** (bisection for the coupling that yields the physical constituent mass $M(0)=1.50$, i.e. 311 MeV via the BZ-edge map $\Lambda_{\rm NJL}/\pi=0.207$ GeV/unit):

| input gluon mass | $\alpha_\text{eff}^\ast$ (this solve) | F151-S5 | $M(0)$ check | $G/G_c$ (linearised) |
|---|---|---|---|---|
| $m_D=0.532$ (F88) | **0.3764** | 0.376 | 311.1 MeV | 3.60 |
| $m_V=0.727$ (F117) | **0.4111** | 0.411 | 311.0 MeV | 2.41 |

Mean $\alpha_\text{eff}^\ast\approx0.39$, squarely in the continuum frozen-coupling window $[0.3,0.5]$ (MOM/V/APT) and matching F152's branch placement. The solve is a converged ($\sim130$ iterations) fixed point and **$L$-stable** to 4 digits ($0.37641/0.37644/0.37644$ at $L=16/24/32$). **This is Residual B's machinery built and run** — F151-S5's stated number is now the verified output of the nonlinear solve.

Two clarifications fall out:
- **Nonlinear $\ne$ linearised.** The physical gap ($M\!=\!1.5$, large) needs $G/G_c=2.4$–$3.6$, *not* the linearised $M\!\to\!0$ value $1.277$ (F77). The $1.277$ is the onset of χSB; producing the full physical mass requires the supercritical coupling above. The two "IR coupling" numbers in the prior findings (F145-N5's $0.256/0.340$ from $G/G_c{=}1.277$; F151-S5's $0.376/0.411$ from $M(0){=}1.5$) are the linearised-onset vs full-gap values; F152 adopted the latter, and this solve confirms it.
- **The naive running overshoots.** Feeding the perturbative running coupling ($\Lambda^{(3)}=347$ MeV, freeze $0.50$) into the *same* solve gives $M(0)=7.58/6.65$ lattice $=1572/1379$ MeV — a $\sim5\times$ overshoot. So $\alpha_\text{eff}^\ast\approx0.39$ is **well below** the perturbative running at the gap scale: the IR coupling is set by saturation/decoupling, not by the running (F152's branch statement, now quantified).

## 3. A — the matching scale $q_\ast$ (cheap route ruled out)

F151 fixed everything in A except the scale $q_\ast$ where $\alpha_V(q_\ast)=1/16\pi$, with $\Delta(1/\alpha)=0.640=\underbrace{a_1/4\pi}_{0.292\ \rm exact}+\underbrace{2b_0^\alpha\ln(1/q_\ast a)}_{0.348}$ and implied $q_\ast=0.733/a$ in the band $[1/\sqrt3,1]/a$. The obvious shortcut is the **propagator log-moment** $q_\ast a=\exp(\tfrac12\langle\ln K\rangle_w)$. It fails:

| weight (4D BZ) | converged $q_\ast a$ | vs band $[0.577,1.0]$ |
|---|---|---|
| flat | $e=2.718$ ($\langle\ln K\rangle=2$ exactly) | **above** (UV scale) |
| $1/K$ (propagator) | $2.30$ | **above** |
| $1/K^2$ (vac-pol-like) | $1.01\to0.65$ ($n{:}24\to64$, **not converged**) | grid-dependent |

The converged moments are **UV** scales ($\sim e/a$), not the matching scale; the only weight that dips into the band is IR-divergent and regularisation-dependent. The physical reason: $q_\ast$ is set by the **UV-finite difference** between the lattice and continuum gluon loops (the genuine $d_1$ after subtraction), which a bare moment cannot represent. **A is therefore not solved** — it requires the full one-loop background-field self-energy on the rule's action, exactly as F151 §8 stated. The cheap route is now explicitly closed (a useful negative: no moment trick substitutes for the loop).

## 4. The two residuals are coupled by the scale

B's solve is *dimensionless*: it fixes the relation $\alpha_\text{eff}^\ast\leftrightarrow M(0)$, taking $M(0)=311$ MeV (the F77/F124 constituent mass) as the physical anchor. Removing that anchor — outputting $m_c$ in MeV from nothing — requires the **absolute scale**, which is precisely Residual A. So the last freedom in the whole strong sector is **one overall scale**, and it lives in the one integral A names. B contributes the gap physics; A contributes the ruler; neither is circular, and together they would close $\alpha_s$, $\Lambda$, $\sqrt\sigma$, $f_\pi$, $m_c$, $\lambda_6$.

## 5. Check summary (`test_F154_residuals_A_B.py`, 2026-06-12 - 19:28)

| Check | Statement | Tier | Result |
|---|---|---|---|
| B1 | gap solve $\Rightarrow\alpha_\text{eff}^\ast=0.376/0.411$, $M(0)=1.50$ | **solved** (converged) | PASS |
| B2 | $L$-stable ($0.3764$ at $L=16,32$) | numeric | PASS |
| B3 | naive running overshoots ($M(0)\approx1570$ MeV $\gg311$) | numeric | PASS |
| A1 | $a_1(6)=\tfrac{11}3$ exact; log-moment gives UV $e/a$, above band — **A open** | honest negative | PASS |
| C | $\alpha_\text{eff}^\ast\approx0.39\in[0.3,0.5]$ frozen window | grounding | PASS |

**Overall 5/5 PASS** (~3 min).

## 6. What is now closed, and what remains

**Closed (this finding).** Residual **B** is built and solved: the IR gap-saturated coupling is the converged, $L$-stable output $\alpha_\text{eff}^\ast=0.376/0.411\approx0.39$, reproducing F151-S5/F152 from the full nonlinear gap; the nonlinear-vs-linearised coupling distinction is clarified; the running-overshoot is quantified. The cheap shortcut for **A** (propagator log-moment) is explicitly ruled out.

**Open (sharply).** Residual **A** — the one-loop background-field lattice self-energy on the rule's gauge action, whose UV-finite part is $q_\ast$ (must come out $0.733/a$). This is the single remaining strong-sector computation; B's mass anchor is removed only once A supplies the absolute scale. Also still open within B: deriving the *freeze value* $\alpha_\text{eff}^\ast\approx0.39$ from the saturation mechanism **without** anchoring $M(0)$ (the solve currently inputs the physical constituent mass; the running overshoots, so the freeze is a genuine nonperturbative input the gap equation does not itself supply).

## 7. Honest scope

- **B** inputs the physical constituent mass $M(0)=311$ MeV (F77/F124) and solves for the coupling; it does **not** derive $311$ MeV from scratch (that needs A's scale). What is new and verified is that the self-consistent gap is a converged, $L$-stable fixed point reproducing F151-S5's $\alpha_\text{eff}^\ast$, and that the perturbative running overshoots it.
- The gap kernel uses the F145 lattice kernel $K=\sum2(1-\cos q_i)$ and the exact Fierz $2/9$; $\varepsilon_c=1$ (no dielectric enhancement) — including it would lower $\alpha_\text{eff}^\ast$ modestly (F145).
- A Pagels–Stokar $f_\pi$ proxy was computed but **overshoots** ($\sim360$ vs 92 MeV) — the crude lattice mean is not the proper PS log-integral (F124 has $f_\pi/M$ exactly); not claimed here.
- **A**'s negative is robust: the converged log-moments are grid-independent UV scales; only the IR-divergent weight is grid-sensitive. The conclusion (q\* needs the subtraction, not a moment) is physical, not a numerical accident.

## 8. Provenance

- **New:** the full nonlinear self-consistent gap solver (`ca_gap_solve.py`) and the inverse solve for $\alpha_\text{eff}^\ast$ (B, solved, $L$-stable); the propagator-log-moment computation and its explicit failure to pin $q_\ast$ (`ca_qstar_logmoment.py`, A negative); the nonlinear-vs-linearised coupling clarification; the running-overshoot quantification; the scale-coupling-of-A-and-B observation.
- **Reused:** F145 kernel/Fierz/running (`ca_njl_induced_coupling`), F151 V-scheme/$a_1$/$q_\ast$ band (`ca_scheme_constant`), F77 constituent mass, F88/F117 $m_D$, F144 running.
- **Verification:** `tests/findings/test_F154_residuals_A_B.py` (2026-06-12 - 19:28, 5/5 PASS), results `test-results/F154_residuals_A_B.json`.
