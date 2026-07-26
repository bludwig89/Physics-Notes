# F262 — Bound-state QED: positronium (reduced-mass spectrum + ortho–para hyperfine + decay rates), hydrogen 21 cm, and Lamb-shift completeness (recoil + finite size)

**Date:** 2026-07-23 - 14:05
**Status:** Confirmed — 10/10 gates PASS. The reduced-mass reduction is **structural/exact** (level ratio $E_n(\mathrm{Ps})/E_n(\mathrm H_\infty)=\tfrac12$ to machine zero, grid-independent); the hyperfine split $\tfrac{7}{12}=\tfrac13+\tfrac14$ and the decay coefficients $\tfrac12\alpha^5$, $\tfrac{2(\pi^2-9)}{9\pi}\alpha^6$ are **algebraically exact**; the Ore–Powell $\pi^2-9$ phase-space integral, the $203\,389$ MHz / $1420.4$ MHz / Lamb numbers are **quantitative** vs measured.
**Modules:** `ca-simulation/ca_positronium.py`, `ca-simulation/ca_hyperfine.py`
**Verification script:** `tests/findings/test_F262_positronium_hyperfine.py` (10/10)
**Result file:** `test-results/F262_positronium_hyperfine.json`
**Cross-references:** [[F125-p5-hydrogen-atom-em-bound-state]] (the one-body Dirac–Coulomb solver reused at $\mu=m_e/2$), [[F260-qed-scattering-smatrix]] (the $e^+e^-$ annihilation vertex / cross section that drives the annihilation hyperfine term and the para decay), [[F252-qed-vertex-ae-lamb-shift]] and [[F257-bethe-log-from-model-spectrum]] (the one-loop radiative Lamb shift and model-derived Bethe log this builds recoil/size on top of), [[F251-qed-vacuum-polarization-running-alpha]] (Uehling), [[F27-complex-mass-chiral-su2]]/[[F46-pythagorean-lattice-mass]] (the $g=2$ Dirac moment behind the spin–spin term), [[F249-qed-comparison-battery]] ($\alpha,m_e$ inputs).

---

## The claim

The one-body Dirac–Coulomb sector (F125 hydrogen fine structure + F252/F257 radiative Lamb shift) covered *single-particle* bound-state QED. The **two-body** and **hyperfine** sectors — positronium, the hydrogen 21 cm line, and the recoil/finite-size completeness of the Lamb shift — had not been built. The claim:

> On the model's own pieces — the F125 Coulomb solver, the F260 charge-conjugate positron and its annihilation vertex, the F27/F46 $g=2$ Dirac moment, and the F252/F257 radiative Lamb shift — bound-state QED reproduces (i) the positronium reduced-mass spectrum (exactly half hydrogen), (ii) the $\tfrac{7}{12}\alpha^4 m_ec^2$ ortho–para hyperfine splitting with the virtual-annihilation piece model-derived, (iii) the para$\to2\gamma$ and ortho$\to3\gamma$ decay rates, (iv) the hydrogen 21 cm line at $1420.4$ MHz, and (v) the recoil + finite-nuclear-size corrections on the Lamb shift, isolating the proton-radius lever.

The only inputs are $\alpha$ and the lepton mass (F249 A5); the proton $g$-factor $g_p$ and the proton radius $r_p$ are the two additional non-QED inputs, stated where used.

---

## The results

### 1. Positronium spectrum — reduced-mass reduction (structural)

The $e^+e^-$ Coulomb problem separates into centre-of-mass + relative motion; the relative motion is a one-body Coulomb problem with reduced mass $\mu=m_e/2$. Reusing F125 (`ca_atom`) at $\mu=m_e/2$:

| Quantity | Value | Tier |
|---|---|---|
| $E_n(\mathrm{Ps})/E_n(\mathrm H_\infty)$ (every level) | $= \tfrac12$ | structural, machine zero (`worst_dev < 1e-9`) |
| ground state $-\tfrac12\,\mathrm{Ry}$ | $-6.803$ eV | closed form |
| numeric solve (N=2000 tridiagonal) | $-6.799$ eV | machine (grid) |

The $\tfrac12$ is exact — it is the ratio of reduced masses $(m_e/2)/m_e$ — and grid-independent, since the Ps and $\mathrm H_\infty$ spectra share the identical dimensionless grid; only the Rydberg prefactor $\tfrac12\mu c^2\alpha^2$ carries the mass.

### 2. Ortho–para hyperfine splitting $\Delta E_\text{hfs}=\tfrac{7}{12}\alpha^4 m_ec^2$

$\tfrac{7}{12}=\tfrac13+\tfrac14$, verified exactly (sympy). The two pieces, both derived from $|\psi(0)|^2=(\mu\alpha)^3/\pi$ with $\mu=m_e/2$ in Gaussian natural units ($e^2=\alpha$):

- **Spin–spin (Fermi contact) $=\tfrac13\alpha^4 m_ec^2$.** Contact Hamiltonian $\tfrac{8\pi}{3}\tfrac{e^2}{m^2}(\mathbf S_e\!\cdot\!\mathbf S_{\bar e})\delta^3(\mathbf r)$ between two $g=2$ Dirac moments (F27/F46); triplet$-$singlet $\Delta\langle\mathbf S_1\!\cdot\!\mathbf S_2\rangle=1$. Reproduces $\tfrac13$ to `rel_err < 1e-12`.
- **Virtual annihilation $=\tfrac14\alpha^4 m_ec^2$.** Unique to a particle–antiparticle pair: ortho-Ps ($^3S_1$, $J{=}1$) can annihilate into a single virtual photon ($J{=}1$); para-Ps ($^1S_0$) cannot. Operator $\tfrac{\pi\alpha}{m^2}\tfrac{3+\boldsymbol\sigma_e\cdot\boldsymbol\sigma_{\bar e}}{2}\delta^3(\mathbf r)$ acts as $2P_\text{triplet}$, giving $2\tfrac{\pi\alpha}{m^2}|\psi(0)|^2=\tfrac14\alpha^4 m$. The contact strength $\pi\alpha/m^2$ **is the model's own single-photon $e^+e^-$ coupling** (F260 Bhabha $s$-channel / annihilation vertex): the threshold $\beta\to0$ limit of the F260 $e^+e^-\to2\gamma$ cross section gives $\sigma v\to\pi\alpha^2/m^2$ (one extra $\alpha$ from the second vertex), reproduced to $<0.04\%$; the model amplitude trace $|\mathcal M|^2/e^4\to4$ at threshold.

| Quantity | Value | Measured | Tier |
|---|---|---|---|
| $\Delta E_\text{hfs}$ (LO) | $204\,387$ MHz | $203\,389$ MHz | quantitative (LO, $+0.49\%$) |

The $\sim0.5\%$ excess is the known $O(\alpha^5)$ radiative correction (Karplus–Klein), out of leading-order scope.

### 3. Decay rates

| Channel | Rate (LO) | $\tau$ (LO) | $\tau$ measured | Source of amplitude |
|---|---|---|---|---|
| para $\to2\gamma$ | $\tfrac12\alpha^5 m_ec^2/\hbar$ | $0.1245$ ns | $0.1245$ ns | model (F260 annihilation $\sigma v$) |
| ortho $\to3\gamma$ | $\tfrac{2(\pi^2-9)}{9\pi}\alpha^6 m_ec^2/\hbar$ | $138.7$ ns | $142.05$ ns | Ore–Powell $3\gamma$ spectrum |

The para rate is fully model-derived: $\Gamma(\text{para})=4\,(\sigma v)_\text{thr}\,|\psi(0)|^2$, with $(\sigma v)_\text{thr}=\pi\alpha^2/m^2$ the $\beta\to0$ limit of the F260 cross section and the factor 4 projecting the spin-averaged $\sigma$ onto the annihilating singlet; the coefficient matches $\tfrac12\alpha^5$ to `rel_err < 1e-12`. The ortho rate needs one extra photon emission ($\alpha^6$); its spin/phase-space factor $\tfrac{2(\pi^2-9)}{9\pi}$ is the Ore–Powell (1949) result, reproduced by integrating the Ore–Powell photon spectrum $\int_0^1 P(x)\,dx=\pi^2-9$ to `rel_err < 5e-4`. The LO $138.7$ ns rises to the measured $142$ ns under the known $O(\alpha)$ correction.

### 4. Hydrogen 21 cm line (Fermi contact)

$\Delta E_F=\tfrac43 g_p\tfrac{m_e}{m_p}\alpha^4 m_ec^2$ (same contact operator, proton moment $g_p=5.5857$ an **input**):

| Step | Value (MHz) | Tier |
|---|---|---|
| $E_F$ point nucleus | $1421.16$ | quantitative |
| $E_F$ reduced mass $\times(m_r/m_e)^3$ | $1418.84$ | quantitative |
| $\times(1+a_e)$, $a_e=\alpha/2\pi$ (F252 Schwinger) | $1420.49$ | quantitative |
| **measured** | $1420.4058$ | — |

Final $1420.49$ MHz, `rel_err 5.8e-5` ($\lambda=21.1$ cm). The reduced-mass factor and the model's own electron anomalous moment (F252) close the gap from the bare Fermi value to the 21 cm line; $g_p$ is the single non-QED input.

### 5. Lamb-shift completeness — recoil + finite size

On the F252/F257 baseline ($1052.19$ MHz, self-energy $+$ Uehling):

| Correction | Value (MHz) | Tier |
|---|---|---|
| reduced-mass rescaling $(m_r/m_e)^3$ | $-1.72$ | derived scaling |
| leading pure recoil (Salpeter/EGS) | $+0.36$ | cited (EGS Phys.Rept.342) |
| finite nuclear size (2s, $r_p=0.8409$ fm) | $+0.138$ | derived, $\propto r_p^2$ |
| **shifted total** | $1050.97$ | — |
| measured | $1057.845$ | — |
| residual | $+6.87$ | two-loop / higher-order radiative |

Finite size $\Delta E_\text{fs}=\tfrac1{12}(Z\alpha)^4 m_r(m_rc\,r_p/\hbar)^2$ shifts **only** the s-state ($2p$ has $\psi(0)=0$) and is the **proton-radius lever**: $\Delta E_\text{fs}\propto r_p^2$, so switching $r_p=0.8409\to0.8770$ fm swings the shift $0.138\to0.150$ MHz ($d\ln\Delta E_\text{fs}=2\,d\ln r_p$). The key conclusion: recoil and finite size are sub-MHz to $\sim$MHz — the $\sim6$ MHz residual to the measured value is dominated by **two-loop/higher-order radiative QED** (the F261 two-loop sector), not by recoil or size.

---

## What this closes

Bound-state QED now covers the **two-body** and **hyperfine** sectors, not just one-body fine structure + one-loop radiative shift: positronium (spectrum, hyperfine, decays), the hydrogen 21 cm line, and the recoil/finite-size completeness of the Lamb shift. The annihilation hyperfine term and the para decay are built from the model's own F260 $e^+e^-$ vertex; the spin–spin term from the F27/F46 $g=2$ moment; the 21 cm QED closure from the F252 Schwinger $a_e$. The proton radius $r_p$ and proton $g$-factor $g_p$ are the only inputs beyond $\alpha$ and $m_e$.

## Open / out of scope

- The $O(\alpha^5)$ radiative correction to the Ps hyperfine ($204\,387\to203\,389$ MHz) and the $O(\alpha)$ correction to the ortho lifetime ($138.7\to142$ ns) are higher-order (F261 two-loop territory).
- The ortho $3\gamma$ **matrix element** itself (the Ore–Powell spectrum $P(x)$) is reproduced numerically but its per-diagram construction from the model's $e^+e^-\to3\gamma$ amplitude (one photon beyond F260's $2\gamma$) is not yet built.
- The pure relativistic-recoil term ($+0.36$ MHz) uses the Eides–Grotch–Shelyuto coefficient; a model-native two-body Bethe–Salpeter recoil derivation is future work.
