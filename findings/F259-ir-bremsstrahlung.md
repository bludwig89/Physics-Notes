# F259 — The infrared sector of QED: soft bremsstrahlung and the Bloch–Nordsieck cancellation of IR divergences

**Date:** 2026-07-22 - 14:10
**Status:** Confirmed — 6/6 checks PASS. The eikonal factor, the current-conservation $k\cdot J=0$ / transverse-projector collapse, the soft IR-log $\int d\omega/\omega=\ln(\Delta E/\mu)$, and the Bloch–Nordsieck $\mu$-cancellation are **algebraically exact** (sympy, literal 0); the shared IR coefficient $f_{IR}(q^2)$ and the finite Sudakov observable are quantitative.
**Module:** `ca-simulation/ca_ir_bremsstrahlung.py`
**Verification script:** `tests/findings/test_F259_ir_bremsstrahlung.py`
**Result file:** `test-results/F259_ir_bremsstrahlung.json`
**Cross-references:** [[F258-electron-self-energy]] (the IR-companion this session was flagged for: F258's on-shell $Z_2$ is IR-divergent with the SAME photon-mass $\mu$; its $\ln\mu$ is cancelled here), [[F252-vertex-ae-lamb]] (the vertex $F_1$ whose IR log this cancels; the $Z_1=Z_2$ Ward tie), [[F251-qed-vacuum-polarization-running-alpha]] (the sibling one-loop function), [[F87-charge-coupling-paired-photon]] (the identity-channel vertex the eikonal factorises from), [[F69-paired-spinor-photon]] (the emitted even-law photon), [[F250-allk-gauge-pole-paired-photon]] (the transverse 2-polarisation residue used in the pol sum; $\Omega_\text{pair}\to\lvert k\rvert/\sqrt3$ soft measure), [[F249-qed-comparison-battery]] (the Tier-C radiative ledger this closes at the IR level).

---

## The claim

The one-loop QED vertex (F252) and electron self-energy (F258) are each individually **IR-divergent** on shell: the renormalised electric form factor $F_1(q^2)$ and the on-shell wavefunction renormalisation $Z_2$ both carry $\ln\mu$ with a small photon mass $\mu$ as IR regulator. No loop-corrected cross section is finite until the **real soft-photon emission** (bremsstrahlung) is added. On the BCC lattice the emitted real photon is the F69/F250 **even-law paired photon** — massless, transverse, one gauge pole — and in the soft limit its dispersion is $\Omega_\text{pair}(k)\to\lvert k\rvert/\sqrt3=c_\text{lat}\lvert k\rvert$. The claim:

> The soft-emission amplitude factorises into the **eikonal factor** off the F87 vertex; its phase-space integral produces an IR log $\ln(\Delta E/\mu)$ with the **same coefficient** $f_{IR}(q^2)$ as the virtual correction; the two are **equal and opposite in $\mu$**, so the $O(\alpha)$ inclusive rate is **finite and $\mu$-independent** (Bloch–Nordsieck), leaving a physical $\ln(\Delta E)$ (Sudakov) dependence on the detector energy resolution.

---

## The results

### B1 — the eikonal soft-emission factor (exact)

Radiation off an external electron leg, using the F87/F68 identity-channel vertex $e\gamma^\mu$ (the U(1) minimal coupling forces), factorises in the soft limit $k\to0$ to

$$\mathcal M_\text{rad}\;\longrightarrow\;e\,\mathcal M_0\left(\frac{p'\cdot\epsilon}{p'\cdot k}-\frac{p\cdot\epsilon}{p\cdot k}\right).$$

The outgoing-leg propagator denominator is the exact on-shell $(p'+k)^2-m^2=2\,p'\cdot k$, and the numerator spinor structure collapses via the on-shell identity

$$\bar u(p')\,\gamma^\mu(\slashed p'+m)=2\,p'^\mu\,\bar u(p'),$$

verified to literal zero with explicit $4\times4$ Dirac gammas (the component form $\gamma^\mu(\slashed p'+m)+(\slashed p'-m)\gamma^\mu=2p'^\mu\mathbb I$ holds for all $\mu$). The incoming leg gives $-e\,p^\mu/(p\cdot k)$ analogously.

### B2 — current conservation and the transverse-projector collapse (exact)

For the eikonal current $J^\mu=p'^\mu/(p'\cdot k)-p^\mu/(p\cdot k)$,

$$k_\mu J^\mu=\frac{p'\cdot k}{p'\cdot k}-\frac{p\cdot k}{p\cdot k}=1-1=0\quad(\text{literal}).$$

So the longitudinal/gauge terms in the polarisation sum drop against the conserved current, and the F250 **transverse (2-polarisation) residue projector** is sufficient: $\sum_{\lambda=1,2}\lvert\epsilon^\lambda\cdot J\rvert^2=-J\cdot J$. With $p^2=p'^2=m^2$,

$$-J\cdot J=\frac{2\,p\cdot p'}{(p\cdot k)(p'\cdot k)}-\frac{m^2}{(p'\cdot k)^2}-\frac{m^2}{(p\cdot k)^2}.$$

### B4 — the IR log from soft phase space (exact structure)

With $-J\cdot J=\mathcal A(\hat n)/\omega^2$ and the BCC measure $\Omega_\text{pair}\to c_\text{lat}\lvert k\rvert$, the photon-energy integral factorises to a pure log,

$$\int_\mu^{\Delta E}\frac{d\omega}{\omega}=\ln\frac{\Delta E}{\mu}\quad(\text{sympy, exact}),\qquad \frac{\sigma_\text{soft}}{\sigma_0}=\frac{\alpha}{\pi}\,f_{IR}(q^2)\,\ln\frac{\Delta E^2}{\mu^2},$$

IR-divergent as $\mu\to0$. The lattice speed $c_\text{lat}=1/\sqrt3$ **cancels out** of the dimensionless IR coefficient (the eikonal is written in the measured photon energy $\omega$); because the IR log lives at $k\to0$, where the lattice is Lorentz-restored (F249 A2/A3), the coefficient is the **continuum** $f_{IR}$ and cancels the continuum loop **like-for-like**.

### Q1 — the shared IR coefficient $f_{IR}(q^2)$ (quantitative)

$$f_{IR}(q^2)=\tfrac12\cdot\frac{1}{4\pi}\int d\Omega\left[\frac{2\,p\cdot p'}{(p\cdot\hat k)(p'\cdot\hat k)}-\frac{m^2}{(p'\cdot\hat k)^2}-\frac{m^2}{(p\cdot\hat k)^2}\right],\qquad \hat k=(1,\hat n).$$

The eikonal angular integral equals $2f_{IR}$; numerically at $-q^2/m^2=10^4$ it is $16.434$, i.e. $f_{IR}=8.217$ vs the closed high-energy form $\ln(-q^2/m^2)-1=8.210$ (rel. err. $8\times10^{-4}$, quadrature-limited). The leading log is $\ln(-q^2/m^2)$.

### B3 — the Bloch–Nordsieck cancellation (exact, literal zero)

$$\frac{\sigma_\text{virtual}}{\sigma_0}\bigg|_{IR}=-\frac{\alpha}{\pi}f_{IR}\ln\frac{-q^2}{\mu^2},\qquad \frac{\sigma_\text{soft}}{\sigma_0}=+\frac{\alpha}{\pi}f_{IR}\ln\frac{\Delta E^2}{\mu^2}.$$

Both carry the **same** $f_{IR}$ (that is Bloch–Nordsieck). The coefficient of $\ln\mu^2$ in the sum is **literally zero** (sympy $\partial/\partial\mu^2=0$), so

$$\frac{\sigma_\text{virtual}+\sigma_\text{soft}}{\sigma_0}=1-\frac{\alpha}{\pi}f_{IR}(q^2)\,\ln\frac{-q^2}{\Delta E^2},$$

finite as $\mu\to0$. The virtual side is $2\,\mathrm{Re}\,F_1$ (F252) with the external-leg $Z_2$ (F258) folded in; the computed Ward identity $Z_1=Z_2$ (F258 differential WT, F252 V1) ties the vertex and self-energy IR pieces so exactly this log cancels.

### Q2 — the finite KLN / Sudakov observable (quantitative)

$$\frac{\sigma}{\sigma_0}=1-\frac{\alpha}{\pi}f_{IR}(q^2)\,\ln\frac{-q^2}{\Delta E^2}\;\xrightarrow{\text{hi-}E}\;1-\frac{\alpha}{\pi}\ln\frac{-q^2}{m^2}\ln\frac{-q^2}{\Delta E^2}$$

(the Sudakov double log). At $\sqrt{-q^2}=1\,\text{GeV}$ with detector resolution $\Delta E=0.1\sqrt{-q^2}=100\,\text{MeV}$: $f_{IR}=14.16$, $\ln(-q^2/\Delta E^2)=4.605$, giving an $O(\alpha)$ correction $-0.151$ and an exponentiated (YFS-resummed) suppression $e^{-0.151}=0.859$. The $\mu$-dependence has cancelled; the $\ln(\Delta E)$ dependence is the **physical, measurable** part (finite inclusive cross section, KLN).

---

## Verification summary (6/6)

| # | Check | Type | Result |
|---|-------|------|:------:|
| B1 | eikonal factor $e(p'\cdot\epsilon/p'\cdot k-p\cdot\epsilon/p\cdot k)$ from F87 | exact | spinor identity literal 0 |
| B2 | $k\cdot J=0$; pol-sum collapse $-J\cdot J$ (F250 2-pol) | exact | literal 0 |
| B4 | soft $\int d\omega/\omega=\ln(\Delta E/\mu)$; $c_\text{lat}$ drops out | exact | log, $c_\text{lat}$-free |
| Q1 | $f_{IR}(q^2)$ vs closed $\ln(-q^2/m^2)-1$ | quantitative | rel. err. $8\times10^{-4}$ |
| B3 | coeff of $\ln\mu^2$ in virtual+soft $=0$ | exact | literal 0, $\mu$-finite |
| Q2 | finite $\mu$-independent Sudakov correction | quantitative | $-0.151$; $e^{-0.151}=0.859$ |

---

## Scope and honesty

- **Exact vs quantitative.** The eikonal factor, $k\cdot J=0$ / projector collapse, the soft IR log, and the $\mu$-cancellation are algebraic identities (sympy, literal 0). The value of $f_{IR}(q^2)$ and the Sudakov number are quantitative; $f_{IR}$ is quoted at leading log $\ln(-q^2/m^2)$ (closed high-energy form $\ln(-q^2/m^2)-1$), matching the angular integral to $8\times10^{-4}$ (quadrature-limited).
- **Like-for-like regulator.** The IR regulator is a small photon mass $\mu$, the **same** one F258 uses for its on-shell $Z_2$ (Feynman gauge), so the cancellation is genuine, not a convention artefact.
- **Model-native.** The emitted photon is the F69/F250 paired photon with its BCC soft measure and transverse residue; the vertex is the F87 identity channel. $c_\text{lat}=1/\sqrt3$ cancels out of the dimensionless IR coefficient, so the continuum $f_{IR}$ cancels the continuum loop.
- **What is deferred.** Higher-order (two-loop / multi-photon) exponentiation is quoted only as the leading YFS estimate $\exp[\text{$O(\alpha)$}]$; a full YFS resummation and hard-collinear (non-soft) real emission are out of scope. The physical statement — a finite, $\mu$-independent inclusive rate with measurable $\ln(\Delta E)$ dependence — is complete at $O(\alpha)$.

This closes the IR level of the F249 Tier-C radiative ledger: with F251 ($Z_3$), F258 ($Z_2$), F252 ($Z_1$, $F_1$, $a_e$, Lamb) and now F259 (IR finiteness), the one-loop QED sector produces **physical, finite cross sections**.

---

## Files
- Module: `ca-simulation/ca_ir_bremsstrahlung.py`
- Test: `tests/findings/test_F259_ir_bremsstrahlung.py`
- Results: `test-results/F259_ir_bremsstrahlung.json`
