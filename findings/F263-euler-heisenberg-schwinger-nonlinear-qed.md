# F263 — Nonlinear & non-perturbative QED: the Euler–Heisenberg effective Lagrangian, light-by-light scattering, field-induced vacuum birefringence, and Schwinger pair production

**Date:** 2026-07-23 - 11:54
**Status:** Confirmed — 7/7 checks PASS. The nonlinear corner of QED — the physics with **no classical Maxwell analogue** — is reproduced on the model's own electron loop. The Euler–Heisenberg coefficient $2\alpha^2/45$ and the box-diagram invariant weight $7$ are **sympy-exact**; the low-energy light-by-light cross section $\sigma=\tfrac{973}{10125\pi}\alpha^4\omega^6/m^8$ (Karplus–Neuman) is reproduced **exactly** (the angular integral closes to a rational $\times\,1/\pi$) with **gauge invariance exact on all four photon legs** and Bose symmetry; the field-induced vacuum birefringence ratio $(n_\parallel-1):(n_\perp-1)=7:4$ (Adler) is exact; and the Schwinger pair-production exponent $\pi m^2/eE$ with critical field $E_\text{crit}=m^2/e=1.32\times10^{18}\,$V/m falls out of the proper-time residue, with the full instanton series $w=\tfrac{(eE)^2}{4\pi^3}\sum_n\tfrac1{n^2}e^{-n\pi m^2/eE}$.
**Modules:** `ca-simulation/ca_euler_heisenberg.py`, `ca-simulation/ca_schwinger_pair.py`
**Verification script:** `tests/findings/test_F263_euler_heisenberg_schwinger.py` (7/7)
**Runner / result file:** `tests/runners/run_F263_euler_heisenberg_schwinger.py` → `test-results/F263_euler_heisenberg_schwinger.json`
**Cross-references:** [[F251-qed-vacuum-polarization-running-alpha]] (the SAME electron loop — the two-photon bubble $\Pi^{\mu\nu}$; Euler–Heisenberg is that loop with **four** external legs, the box, in the constant-field limit, and its $b_0=4/3$ machinery is the two-leg counterpart of the four-leg Ward gate here), [[F250-allk-gauge-pole-paired-photon]] (the external photons are the even-law paired photon with a single massless transverse gauge pole; the four-photon amplitude is exactly transverse on every leg, preserving that pole), [[F69-paired-spinor-photon]] (the paired photon whose $(\mathbf E,\mathbf B)$ the nonlinear corrections act on), [[F249-qed-comparison-battery]] (B1: **zero linear** vacuum birefringence for the free paired photon — this finding gives the **nonlinear, non-zero** field-induced birefringence, distinct and consistent), [[F27-bcc-weyl-walk]] / [[F46-dirac-from-two-weyl]] (the internal electron / Dirac sea whose Sauter–Schwinger tunnelling is the pair-production channel).

---

## The claim

QED, previously built here at the perturbative-diagram level (vacuum polarisation F251, vertex F252, self-energy F258, two-loop F261, bound states F262), is extended to its **nonlinear and non-perturbative** sector — the effects that vanish identically in classical electrodynamics and are generated only by integrating out the electron:

1. **Euler–Heisenberg effective Lagrangian.** The leading four-field term of the one-loop electron determinant in a constant background,
$$\mathcal L_\text{EH}=\frac{2\alpha^2}{45\,m^4}\Big[(\mathbf E^2-\mathbf B^2)^2+7(\mathbf E\cdot\mathbf B)^2\Big].$$
Both the prefactor $2\alpha^2/45$ and the relative weight $7$ are derived exactly.
2. **Light-by-light scattering $\gamma\gamma\to\gamma\gamma$.** From $\mathcal L_\text{EH}$ the low-energy cross section is
$$\sigma=\frac{973}{10125\pi}\,\frac{\alpha^4\omega^6}{m^8}\qquad(\omega\ll m),$$
gauge-invariant and Bose-symmetric — the analytic limit of the box diagram whose full form ATLAS observed in Pb+Pb collisions.
3. **Field-induced vacuum birefringence.** A probe photon in a strong background $B$ acquires polarisation-dependent refractive indices in the ratio $(n_\parallel-1):(n_\perp-1)=7:4$.
4. **Schwinger pair production.** The non-perturbative $e^+e^-$ creation rate from a static field,
$$w=\frac{(eE)^2}{4\pi^3}\sum_{n=1}^\infty\frac{1}{n^2}\exp\!\Big(-\frac{n\pi m^2}{eE}\Big),\qquad E_\text{crit}=\frac{m^2}{e}\simeq1.32\times10^{18}\,\text{V/m}.$$

---

## The construction

### 1. Euler–Heisenberg coefficients (EH1) — exact

The renormalised constant-field one-loop Lagrangian (Schwinger proper time) is
$$\mathcal L=-\frac1{8\pi^2}\int_0^\infty\frac{ds}{s^3}\,e^{-m^2 s}\Big[e^2s^2\,ab\,\coth(eas)\cot(ebs)-1-\tfrac{e^2s^2}{3}(a^2-b^2)\Big],$$
with the secular invariants $a^2-b^2=2\mathcal F=\mathbf B^2-\mathbf E^2$, $a^2b^2=\mathcal G^2$, where $\mathcal F=\tfrac14 F_{\mu\nu}F^{\mu\nu}$, $\mathcal G=\tfrac14 F_{\mu\nu}\tilde F^{\mu\nu}$. Writing $x=eas,\ y=ebs$, the integrand core is $(x\coth x)(y\cot y)-1-\tfrac13(x^2-y^2)$. Its weak-field (fourth-order) part is
$$-\tfrac1{45}(x^4+y^4)-\tfrac19 x^2y^2,$$
and with $\int_0^\infty s\,e^{-m^2 s}\,ds=1/m^4$ and $e^4=16\pi^2\alpha^2$,
$$\mathcal L^{(1)}=\frac{\alpha^2}{m^4}\Big[\tfrac{1}{45}(a^4+b^4)+\tfrac19 a^2b^2\Big]\cdot\tfrac12=\frac{2\alpha^2}{45\,m^4}\big[4\mathcal F^2+7\mathcal G^2\big].$$
The **7** is the sum $\tfrac{2}{45}$ (from $a^4+b^4=4\mathcal F^2+2\mathcal G^2$) $+\tfrac{5}{45}$ (from $\tfrac19 a^2b^2=\tfrac{5}{45}\mathcal G^2$), over the $\tfrac2{45}$ of $(\mathbf E^2-\mathbf B^2)^2=4\mathcal F^2$. In the invariant basis the weights are $8/45:14/45=4:7$. `sympy`-exact.

### 2. Light-by-light cross section (EH2) — exact

The contact four-photon vertex is read off from $\mathcal L=\mu(F\!\cdot\!F)^2+\nu(F\!\cdot\!\tilde F)^2$, $\mu=\tfrac{\alpha^2}{90m^4}$, $\nu=\tfrac{7\alpha^2}{360m^4}$, as
$$\mathcal M=8\mu\!\!\sum_\text{pairings}\!\!(f^a\!\cdot\!f^b)(f^c\!\cdot\!f^d)+8\nu\!\!\sum_\text{pairings}\!\!(f^a\!\cdot\!\tilde f^b)(f^c\!\cdot\!\tilde f^d),\quad f^i_{\mu\nu}=k^i_\mu\epsilon^i_\nu-k^i_\nu\epsilon^i_\mu.$$
Summing $|\mathcal M|^2$ over the 16 linear-polarisation configurations in the CM frame, averaging over the 4 initial states, applying the 2→2 massless phase space $d\sigma/d\Omega=|\mathcal M|^2/(64\pi^2 s)$ ($s=4\omega^2$) and the identical-particle factor $\tfrac12$, the angular integral closes **exactly** to
$$\sigma=\frac{973}{10125\pi}\,\frac{\alpha^4\omega^6}{m^8}.$$
This is the Karplus–Neuman (1951) result, reproduced symbolically — a simultaneous confirmation that the vertex normalisation from $\mathcal L_\text{EH}$ is correct and that the coefficient is exact.

### 3. Gauge + Bose gates (EH3) — exact

Each photon enters only through the antisymmetric $f^i_{\mu\nu}=k^i_\mu\epsilon^i_\nu-k^i_\nu\epsilon^i_\mu$, which vanishes identically when $\epsilon^i\to k^i$. So the amplitude is **exactly transverse on every one of the four legs** (Ward, literal $0$), the four-leg counterpart of F251's two-leg loop Ward identity. The symmetric sum over pairings makes $\mathcal M$ invariant under exchange of any two photons (Bose). Both are exact gates — the F250 massless gauge pole is preserved by the nonlinear interaction.

### 4. Field-induced birefringence (EH4) — exact

Expanding $\mathcal L_\text{EH}$ to second order in a probe field about a constant background $\mathbf B=B\hat x$ (probe propagating along $\hat z$), the two eigen-polarisations give
$$\Delta\mathcal L_\parallel=7\kappa B^2 e^2,\qquad \Delta\mathcal L_\perp=4\kappa B^2 e^2,\qquad \kappa=\frac{2\alpha^2}{45m^4},$$
for $\mathbf E$ parallel vs perpendicular to $\mathbf B$. With $n-1=\Delta\mathcal L/2e^2$,
$$n_\parallel-1=\frac72\cdot\frac{2\alpha^2}{45}\frac{B^2}{m^4},\qquad n_\perp-1=\frac42\cdot\frac{2\alpha^2}{45}\frac{B^2}{m^4},\qquad \frac{n_\parallel-1}{n_\perp-1}=\frac74.$$
This is the **nonlinear**, field-induced birefringence — the physical, non-zero effect — distinct from and consistent with F249-B1's confirmed **zero linear** birefringence of the free paired photon.

### 5. Schwinger pair production (SC1–SC3)

For a pure electric background the proper-time integrand's $eEs\cot(eEs)$ term has poles on the positive real axis at $s_n=n\pi/(eE)$. The imaginary part is $\pi$ times the sum of residues:
$$\operatorname{Im}\mathcal L=\sum_{n\ge1}\frac{(eE)^2}{8\pi^3 n^2}\,e^{-n\pi m^2/eE}\ \Rightarrow\ w=2\operatorname{Im}\mathcal L=\frac{(eE)^2}{4\pi^3}\sum_{n\ge1}\frac1{n^2}e^{-n\pi m^2/eE}.$$
The tunnelling exponent $\pi m^2/eE=\pi E_\text{crit}/E$ and the $1/n^2$ instanton weights both fall out of the residue (`sympy`-exact). From CODATA, $E_\text{crit}=m_e^2c^3/e\hbar=1.323\times10^{18}\,$V/m and $B_\text{crit}=m_e^2c^2/e\hbar=4.414\times10^{9}\,$T. The rate is a genuine essential singularity: $\exp(-\pi E_\text{crit}/E)$ has an identically-zero Taylor series about $E=0$ — invisible to any finite order of perturbation theory (SC4, sympy-exact). Physically this is the Sauter–Schwinger tunnelling of the F27/F46 Dirac sea tilted by the field.

---

## Results

| # | Quantity | Tier | Result |
|---|---|---|---|
| EH1 | $\mathcal L_\text{EH}$ prefactor $2\alpha^2/45$ and invariant weight $7$ (basis $8/45:14/45=4:7$) | exact (sympy) | prefactor $=2/45$, weight $=7$ literal |
| EH2 | $\sigma(\gamma\gamma\to\gamma\gamma)=\tfrac{973}{10125\pi}\alpha^4\omega^6/m^8$ (Karplus–Neuman) | exact (sympy) | coeff $=973/10125$ literal |
| EH3 | Ward on all 4 photon legs ($\epsilon^i\to k^i\Rightarrow\mathcal M=0$) + Bose | exact (sympy) | all residuals literal $0$ |
| EH4 | field-induced birefringence $(n_\parallel-1):(n_\perp-1)=7:4$ | exact (sympy) | $7:4$ literal |
| SC1 | Schwinger $\operatorname{Im}\mathcal L_n=\tfrac{(eE)^2}{8\pi^3 n^2}e^{-n\pi m^2/eE}$; exponent $\pi m^2/eE$ | exact (sympy) | ratio to target $=1$ |
| SC2 | $E_\text{crit}=m^2/e=1.323\times10^{18}\,$V/m; $B_\text{crit}=4.414\times10^{9}\,$T | quantitative | rel err $2.5\times10^{-3}$ vs $1.32\times10^{18}$ |
| SC3 | non-perturbative: $\exp(-\pi E_\text{crit}/E)$ Taylor about $E=0$ | exact (sympy) | series $\equiv 0$ |

---

## Honest scope

The Euler–Heisenberg Lagrangian and everything derived from it are the **leading (four-field, one-loop)** term; higher field powers and higher loops are not included but are not needed for the targets above. The light-by-light coefficient is the $\omega\ll m$ **contact limit**; the ATLAS Pb+Pb observation (Nature Phys. 13, 852, 2017) is the measured contact point but sits in the **full-box** ($m_{\gamma\gamma}\sim$ GeV) regime, so no cross-section fit to ATLAS is claimed — only the analytic low-energy limit is reproduced. The Schwinger rate is the constant-field (worldline-instanton) result; time-dependent-field corrections (the Keldysh/adiabaticity regime) are out of scope. $E_\text{crit}$ uses CODATA $m_e$; the $2.5\times10^{-3}$ residual is rounding of the $1.32\times10^{18}$ reference, not a model error.

## Significance

With F263 the model covers QED **beyond perturbative diagrams**: the nonlinear self-interaction of light (light-by-light, birefringence) and the non-perturbative decay of the vacuum (Schwinger production). Both are consequences of the **same electron loop** already used for F251's vacuum polarisation — the two-point bubble becomes the four-point box (Euler–Heisenberg) and, in an electric field, develops the imaginary part that is pair creation. The exactness of $2\alpha^2/45$, the $7$ weight, the $973/10125\pi$ cross section, the $7:4$ birefringence, and the $\pi m^2/eE$ exponent, together with exact gauge invariance on all four legs, places the nonlinear/non-perturbative sector on the same footing as the perturbative one.
