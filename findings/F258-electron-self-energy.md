# F258 — The one-loop QED electron self-energy Σ(p): mass renormalization δm, wavefunction renormalization Z₂, and Z₁=Z₂ proven from the loop integrals

> **[PARTIALLY SUPERSEDED 2026-08-02 by F277 — ledger S12-F277-refold-removed-qed-and-gluon]**
>
> **DEAD:** Numbers computed through the refolded _selfenergy_AB, for the same reason and on the same kernel.
>
> **STILL LIVE:** The self-energy construction: mass renormalization delta-m, wavefunction renormalization, and the structure of the result.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-07-22 - 09:30
**Status:** Confirmed — 6/6 checks PASS. The mass shift $\delta m=\tfrac{3\alpha}{4\pi}m\ln(\Lambda^2/m^2)$ and the wavefunction renormalization $Z_2=1-\tfrac{\alpha}{4\pi}\ln(\Lambda^2/m^2)$ are **algebraically exact** (sympy; the on-shell parametric integrals evaluate to exactly $3$ and $-1$); the differential Ward–Takahashi identity $\partial\Sigma/\partial p_\mu=-\Lambda^\mu(p,p)$ is **derived from the loop integrand**, turning $Z_1=Z_2$ from an assumption (F252) into a **computed** identity; lattice = continuum after subtraction. This completes the one-loop 1PI set $\{Z_3\ (\Pi,\text{F251}),\ Z_2\ (\Sigma,\text{F258}),\ Z_1\ (\Lambda,\text{F252})\}$ with all Ward identities verified.
**Module:** `ca-simulation/ca_electron_self_energy.py`
**Verification script:** `tests/findings/test_F258_electron_self_energy.py`
**Result file:** `test-results/F258_electron_self_energy.json`
**Cross-references:** [[F252-qed-vertex-ae-lamb-shift]] (the vertex $\Lambda^\mu$ this $\Sigma$ is tied to by the differential WT identity; F252 *asserted* $Z_1=Z_2$, here it is *proven*), [[F251-qed-vacuum-polarization-running-alpha]] (the abelian one-loop template — same fermion loop, closed vs open legs; reuses its Dirac-γ / parametric machinery and lattice-subtraction), [[F87-charge-coupling-paired-photon]] (the identity-channel vertex $\gamma^\mu$ at both ends), [[F69-paired-spinor-photon]] (the internal even-law paired photon), [[F250-allk-gauge-pole-paired-photon]] (its single massless transverse gauge pole), [[F27-complex-mass-chiral-su2]] / [[F46-pythagorean-lattice-mass]] (the internal Weyl/Dirac electron), [[F249-qed-comparison-battery]] (the QED ledger).

---

## The claim

The one-loop QED electron self-energy $\Sigma(p)$ — the electron emitting and reabsorbing a paired photon, built from two F87 identity-channel vertices, one internal Weyl/Dirac electron (F27/F46), and one internal even-law paired photon (F69/F250) — supplies the mass renormalization $\delta m$ and the field-strength renormalization $Z_2$ with their exact log-divergent coefficients, and satisfies the **differential Ward–Takahashi identity** with the F252 vertex, so that $Z_1=Z_2$ is a *proven identity between the two computed loop integrals* rather than an assumption imported from gauge invariance.

The diagram, in Feynman gauge with a small photon mass $\mu$ as IR regulator:

$$-i\,\Sigma(p)=(-ie)^2\!\int\!\frac{d^4k}{(2\pi)^4}\,\gamma^\mu\,\frac{i(\slashed k+m)}{k^2-m^2}\,\gamma_\mu\,\frac{-i}{(p-k)^2-\mu^2}
\;\Longrightarrow\;
\Sigma(p)=-ie^2\!\int\!\frac{d^4k}{(2\pi)^4}\,\frac{\gamma^\mu(\slashed k+m)\gamma_\mu}{(k^2-m^2)\big((p-k)^2-\mu^2\big)},$$

Lorentz-decomposed as $\Sigma(p)=A(p^2)\,\slashed p+B(p^2)\,m$.

---

## The results

### S0 — the numerator contraction (exact)

With explicit $4\times4$ Dirac gammas (Clifford $\{\gamma^\mu,\gamma^\nu\}=2\eta^{\mu\nu}$ confirmed), the $d=4$ contraction

$$\gamma^\mu(\slashed k+m)\gamma_\mu=-2\slashed k+4m$$

holds to literal zero residual. This numerator over $(k^2-m^2)\big((p-k)^2-\mu^2\big)$ is the entire self-energy integrand — the seed of everything below.

### S1 — the mass shift $\delta m=\tfrac{3\alpha}{4\pi}m\ln(\Lambda^2/m^2)$ (exact)

Feynman-parametrizing and shifting $k\to k+xp$ kills the odd $\slashed k$ term and leaves the numerator $N(x)=4m-2x\slashed p$. The log-divergent scalar bubble is $\int d^4k/(2\pi)^4\,(k^2-\Delta)^{-2}\to (i/16\pi^2)\ln(\Lambda^2/\Delta)$, and with the loop prefactor $-ie^2$ (using $e^2/16\pi^2=\alpha/4\pi$):

$$\Sigma(p)\big|_{\text{div}}=\frac{\alpha}{4\pi}\int_0^1 dx\,(4m-2x\slashed p)\,\ln\frac{\Lambda^2}{m^2}.$$

On shell $\slashed p=m$ the numerator is $m(4-2x)$, and the parametric integral is **exactly** $\int_0^1(4-2x)\,dx=3$ (the mass-sector analogue of F251's $b_0=\tfrac43$ gate), so

$$\delta m=\Sigma(\slashed p=m)=\frac{3\alpha}{4\pi}\,m\,\ln\frac{\Lambda^2}{m^2}+\text{finite}.$$

The anomalous-dimension-like coefficient $3/4\pi$ is reproduced as an exact rational $\times\,\pi^{-1}$.

### S2 — the wavefunction renormalization $Z_2$ (exact), and $Z_1=Z_2$ log coefficient

$$Z_2^{-1}=1-\frac{d\Sigma}{d\slashed p}\bigg|_{\slashed p=m}.$$

Only the explicit $\slashed p$ in $N(x)=4m-2x\slashed p$ gives a UV-divergent derivative (the $\slashed p$ inside $\Delta$ contributes a UV-*finite* piece), so

$$\frac{d\Sigma}{d\slashed p}\bigg|_{\text{div}}=\frac{\alpha}{4\pi}\int_0^1(-2x)\,dx\,\ln\frac{\Lambda^2}{m^2}=-\frac{\alpha}{4\pi}\ln\frac{\Lambda^2}{m^2},$$

since $\int_0^1(-2x)\,dx=-1$ exactly. Hence

$$Z_2=1-\frac{\alpha}{4\pi}\ln\frac{\Lambda^2}{m^2}+\text{finite}\,(+\,\text{IR }\ln\mu).$$

In **Feynman gauge** the one-loop vertex $Z_1$ (F252's $\Lambda$) carries the *same* log coefficient $-\alpha/4\pi$, so $Z_1=Z_2$ at the level of the divergent coefficients.

### S3 — the differential Ward–Takahashi identity (exact, computed) → $Z_1=Z_2$

The self-energy has one internal electron line $S_F(k+p)$. Differentiating $\Sigma$ with respect to the **external** momentum acts only on that line, and by the integrand identities

$$\frac{\partial}{\partial p_\mu}(\slashed p-m)=\gamma_\mu,\qquad
\frac{\partial}{\partial p_\mu}S_F(p)=-S_F(p)\,\gamma_\mu\,S_F(p),$$

differentiation **inserts a zero-momentum photon vertex** into the electron line — exactly the $q\to0$ limit of the F252 vertex. Both matrix identities are verified to literal zero with explicit gammas and *exact symbolic inverses* (checked for $\mu=0$ and $\mu=1$). Therefore

$$\boxed{\;\frac{\partial\Sigma}{\partial p_\mu}=-\Lambda^\mu(p,p)\;}$$

as a relation between the two computed loop objects. Combined with S2 (both divergent coefficients equal $-\alpha/4\pi$), this **derives** $Z_1=Z_2$ from the loop integrals rather than assuming it from gauge invariance — the upgrade over F252, which stated the identity at the defining/tree level.

### S4 — the renormalized propagator (pole at $m$, residue 1)

Imposing the on-shell conditions that $\{\delta m,Z_2\}$ enforce,

$$\Sigma_R(\slashed p=m)=0,\qquad \frac{d\Sigma_R}{d\slashed p}\bigg|_{\slashed p=m}=0,$$

the renormalized inverse propagator is

$$S_R^{-1}(p)=\slashed p-m-\Sigma_R(p)=\slashed p-m+O\big((\slashed p-m)^2\big),$$

verified symbolically to have its pole exactly at the physical mass $m$, **residue exactly 1**, and **no residual $\ln\Lambda$** (both divergences absorbed).

### S5 — lattice = continuum (convergent)

Swapping the continuum photon $1/k^2$ for the F251 rule kernel $K=3\,\Omega_{\text{even}}^2+k_t^2$ (paired-photon dispersion) leaves the log-divergent $A$ and $B$ coefficients unchanged: the subtracted differences $\Delta_A=A_{\text{rule}}-A_{\text{cont}}$ and $\Delta_B=B_{\text{rule}}-B_{\text{cont}}$ are IR-scale ($P$) independent (spreads $\sim4\times10^{-4}$ and $\sim8\times10^{-5}$ across $P\in\{0.1,0.15,0.2,0.3\}$; a residual log would grow like $\ln(1/P)$). Same subtracted machinery and grid caveat as F251/F162.

---

## The IR caveat (stated honestly)

The **on-shell** $Z_2$ is IR-divergent in massless-photon QED — this is expected, not a defect. It is regulated here with a small photon mass $\mu$, and the IR piece cancels against real soft-photon emission (Kinoshita–Lee–Nauenberg). The UV coefficients (S1, S2) and the WT identity (S3) are IR-safe; only the *finite on-shell value* of $Z_2$ carries the $\ln\mu$. This is the hook for the IR-companion session (soft-photon / KLN cancellation).

---

## Why this matters

This is the third and final one-loop 1PI function of QED on the BCC lattice. Together with F251 ($\Pi$, the photon self-energy and $Z_3$) and F252 ($\Lambda$, the vertex and $Z_1$), the renormalization set $\{Z_3,Z_2,Z_1\}$ is now complete, and **every Ward identity is verified between computed objects**: $q_\mu\Pi^{\mu\nu}=0$ (F251, transversality), $q_\mu\Lambda^\mu=S^{-1}(p')-S^{-1}(p)$ (F252), and the differential $\partial\Sigma/\partial p_\mu=-\Lambda^\mu$ (F258, which promotes $Z_1=Z_2$ to a theorem of the loop integrals). One-loop QED closes.

---

## Scope and honesty ledger

- **Exact (sympy):** S0 contraction; S1 $\delta m$ coefficient $3/4\pi$ (integral $=3$); S2 $Z_2$ coefficient $-1/4\pi$ (integral $=-1$) and $Z_1=Z_2$ log coefficient; S3 differential WT (vertex insertion + propagator identity, exact symbolic inverse); S4 renormalized pole/residue.
- **Convergent (numerical):** S5 lattice = continuum, subtracted $A,B$ coefficients $P$-flat (F251/F162 caveat: the arccos rule kernel is grid-sensitive at small $n$; the decisive point is that $\Delta$ is a small constant, not a growing log).
- **IR:** on-shell $Z_2$ finite part is IR-divergent ($\ln\mu$); regulated, cancels against real emission (KLN) — deferred to the IR-companion session.
- **Out of scope:** two-loop and higher; the full finite parts of $A(p^2),B(p^2)$ away from the shell (only the divergent coefficients and on-shell structure are the subject here).
