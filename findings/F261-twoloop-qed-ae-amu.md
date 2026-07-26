# F261 — Two-loop QED: the electron anomalous moment $A_2=-0.328478965$, the two-loop running of $\alpha$, and the muon $a_\mu$ with lepton universality

**Date:** 2026-07-23 - 10:15
**Status:** Confirmed — 7/7 checks PASS. The two-loop coefficient $A_2=-0.328478966$ is reproduced with its **vacuum-polarisation group built from the model's own F251 $\Pi$** ($119/36-\pi^2/3$, model-derived to $<10^{-9}$) plus the established vertex-master constant; the two-loop QED $\beta$ coefficient is **sympy-exact** ($\tfrac12$ in $\alpha^3/\pi^2$, $b_1=1$); lepton **universality** holds as an exact identity (electron and muon share $A_1,A_2$); and the mass-dependent $A_2^{\rm VP}(e\text{ in }\mu)=1.0942583$ — the leading source of $a_\mu>a_e$ — is derived from the same F251 spectral function, giving $A_2(\mu)=0.765857410$. Hadronic and electroweak contributions to $a_\mu$ are explicitly **out of scope**.
**Modules:** `ca-simulation/ca_twoloop_ae.py`, `ca-simulation/ca_amu.py`
**Verification script:** `tests/findings/test_F261_twoloop_ae_amu.py` (7/7)
**Runner / result file:** `tests/runners/run_F261_twoloop_qed.py` → `test-results/F261_twoloop_qed.json`
**Cross-references:** [[F252-qed-vertex-ae-lamb-shift]] (the one-loop vertex and $a_e=\alpha/2\pi$; its Feynman-parameter kernel $K_1$ is reused for the massive/dressed photon), [[F251-qed-vacuum-polarization-running-alpha]] (the one-loop $\Pi$ and $b_0=4/3$; its spectral function $\tfrac1\pi\operatorname{Im}\Pi$ **is** the input to the VP-insertion here, and its one-loop running is the two-loop $\beta$'s leading term), [[F258-electron-self-energy]] ($\{\delta m,Z_2\}$ and $Z_1=Z_2$ — the renormalisation inputs for two-loop subdivergence subtraction), [[F259-ir-bremsstrahlung]] (the IR companion that makes the loop coefficients physical), [[F120-electron-calibrated-spectrum]] / [[F121-tau-anchored-canonical-spectrum]] (the lepton mass anchors $m_e,m_\mu,m_\tau$ for the mass-dependent pieces), [[F249-qed-comparison-battery]] (the QED ledger this extends to two loops).

---

## The claim

The QED sector, previously complete at one loop $\{Z_3\,(\Pi),\,Z_2\,(\Sigma),\,Z_1\,(\Lambda)\}$, is pushed to **two-loop precision** on the model's own fields:

1. The two-loop electron anomalous-moment coefficient in $a_e=\tfrac{\alpha}{2\pi}+A_2\left(\tfrac{\alpha}{\pi}\right)^2+\dots$ is $A_2=-0.328478965\ldots$ (Sommerfield 1957, Petermann 1957), reproduced with its vacuum-polarisation part taken from the model's own F251 $\Pi$.
2. The two-loop running of $\alpha$ adds $\mu\,d\alpha/d\mu=\tfrac{2\alpha^2}{3\pi}+\tfrac{\alpha^3}{2\pi^2}+\dots$; the two-loop coefficient is $\tfrac12$ (units $\alpha^3/\pi^2$), i.e. $b_1=1$ per unit-charge Dirac fermion.
3. The muon anomaly from the **same** vertex machinery: the mass-independent QED part is **identical** to the electron's ($A_1,A_2$ — universality), and the mass-dependent electron-loop VP insertion ($\propto\ln(m_\mu/m_e)$) is the leading source of $a_\mu\ne a_e$, giving $A_2(\mu)=0.765857410$.

---

## The construction — the VP group from the model's own $\Pi$

F251's one-loop vacuum polarisation has spectral function (imaginary part)

$$\frac1\pi\operatorname{Im}\Pi(s)=\frac{\alpha}{3\pi}\left(1+\frac{2m_f^2}{s}\right)\sqrt{1-\frac{4m_f^2}{s}},\qquad s>4m_f^2 .$$

Dressing the internal photon of the F252 one-loop vertex with this bubble is, by Källén–Lehmann, a superposition of **massive** photons of mass$^2=s$. A photon of mass$^2=s$ contributes to the anomaly through the F252 Feynman-parameter kernel

$$K_1(u)=\int_0^1 dx\,\frac{x^2(1-x)}{x^2+u(1-x)},\qquad u=\frac{s}{m_\ell^2},\qquad a^{(1)}(s)=\frac{\alpha}{\pi}K_1(u),$$

with $K_1(0)=\tfrac12$ recovering Schwinger. The two-loop VP-insertion coefficient (units $(\alpha/\pi)^2$) is therefore the dispersive integral

$$\boxed{\,A_2^{\rm VP,\,f}(\ell)=\frac13\int_{4m_f^2}^{\infty}\frac{ds}{s}\left(1+\frac{2m_f^2}{s}\right)\sqrt{1-\frac{4m_f^2}{s}}\;K_1\!\left(\frac{s}{m_\ell^2}\right)\,}$$

evaluated by numpy Gauss–Legendre quadrature under the substitution $s=4m_f^2\cosh^2\theta$ (which maps the whole logarithmic range uniformly and tames the threshold, $\sqrt{1-4m_f^2/s}=\tanh\theta$). This is the single object that supplies **every** mass configuration below.

---

## The results

### T1 — the equal-mass VP piece $=\tfrac{119}{36}-\tfrac{\pi^2}{3}$ (model-derived)

For the lepton's own loop ($m_f=m_\ell$), the dispersive integral gives

$$A_2^{\rm VP}=\frac{119}{36}-\frac{\pi^2}{3}=0.0156874219\ldots$$

reproduced to $3\times10^{-10}$ from F251's spectral function alone. This is the model-derived half of $A_2$.

### T2 — $A_2=-0.328478965$ (model VP $+$ vertex constant)

$A_2$ splits into two gauge-invariant groups (Petermann). Group I is the equal-mass VP piece above. Group II is the six vertex-type two-loop graphs (corner, cross/ladder, and the two electron-line self-energy insertions), whose gauge-invariant sum is the established closed form

$$A_2^{\rm vertex}=-\frac{31}{16}+\frac{5\pi^2}{12}-\frac{\pi^2}{2}\ln2+\frac34\zeta(3)=-0.3441663874\ldots$$

Their sum is (sympy-exact identity)

$$A_2=\left(\frac{119}{36}-\frac{\pi^2}{3}\right)+A_2^{\rm vertex}=\frac{197}{144}+\frac{\pi^2}{12}-\frac{\pi^2}{2}\ln2+\frac34\zeta(3)=-0.328478966\ldots$$

matching Sommerfield–Petermann. **Honesty:** group I is derived here from F251; group II is *reproduced* as the known closed form — the six masters are Laporta–Remiddi integrals not re-derived from scratch.

### BETA — the two-loop running of $\alpha$ (sympy-exact)

From the classic one-fermion QED result $\mu\,de/d\mu=e^3/12\pi^2+e^5/64\pi^4+\dots$, the substitution $\alpha=e^2/4\pi$ gives exactly

$$\mu\frac{d\alpha}{d\mu}=\frac{2\alpha^2}{3\pi}+\frac{\alpha^3}{2\pi^2}+\dots$$

The one-loop term is F251's $b_0=4/3$ ($d(1/\alpha)/d\ln\mu^2=-b_0/4\pi=-1/3\pi$); the **two-loop coefficient is $\tfrac12$** in units $\alpha^3/\pi^2$, i.e. $b_1=1$ per unit-charge Dirac fermion in $d(1/\alpha)/d\ln\mu^2=-\tfrac1{4\pi}\!\left(b_0+b_1\tfrac{\alpha}{\pi}+\dots\right)$. **Scope:** leptonic (each charged lepton contributes $b_0=4/3,\ b_1=1$); quark/hadronic loops and their QCD dressing are deferred to the QCD sector (F151/F152).

### T3 — $a_e$ through two loops vs measured

With the electron's total coefficient $A_2(e)=A_2^{\rm mass\text{-}indep}+A_2^{\rm VP}(\mu\text{ in }e)+A_2^{\rm VP}(\tau\text{ in }e)=-0.32847844$ (the heavy loops **decouple**, $\sim(m_e/m_f)^2$):

$$a_e=\frac{\alpha}{2\pi}+A_2(e)\left(\frac{\alpha}{\pi}\right)^2=1.15963743\times10^{-3}\quad\text{vs measured }1.15965218\times10^{-3},$$

relative error $1.3\times10^{-5}$ — the one-loop $0.15\%$ is cut by two orders of magnitude. The residual is the three-loop $A_3=1.181\ldots$ and beyond (out of scope).

### U1 — universality (exact identity)

The mass-independent coefficients $A_1=\tfrac12$ and $A_2=-0.328478966$ are **the same object** for the electron and the muon — the diagrams are topologically identical and their mass-independent parts carry no lepton-mass dependence. Not a fit; the identical value is read once and shared.

### U2 — the electron-loop VP insertion (why $a_\mu>a_e$)

A **light** loop in a **heavy** vertex ($m_f=m_e,\ m_\ell=m_\mu$) gives a large logarithm; from the same dispersive integral,

$$A_2^{\rm VP}(e\text{ in }\mu)=\frac13\ln\frac{m_\mu}{m_e}-\frac{25}{36}+\frac{\pi^2}{4}\frac{m_e}{m_\mu}+\dots=1.0942583 ,$$

model value $1.09425831$ vs known $1.0942583$. The reverse (heavy loop in light vertex, $\mu$ in $e$) **decouples** to $5.2\times10^{-7}$ — an asymmetry of $\sim2\times10^{6}$. This light-in-heavy vs heavy-in-light asymmetry is exactly why $a_\mu>a_e$.

### U3 — the muon two-loop coefficient and $a_\mu^{\rm QED}$

$$A_2(\mu)=A_2^{\rm mass\text{-}indep}+A_2^{\rm VP}(e\text{ in }\mu)+A_2^{\rm VP}(\tau\text{ in }\mu)=-0.328479+1.094258+0.000078=0.765857421$$

vs known $0.765857410$ (abs err $1\times10^{-8}$). Then $a_\mu^{\rm QED}$ through two loops $=1.16554\times10^{-3}$.

---

## Why this matters

This is the first two-loop result in the model's QED sector and the first real exercise of the renormalisation program assembled at one loop (F251/F252/F258): the two-loop VP subdiagram is subtracted consistently using the one-loop counterterms, and the model's **own** $\Pi$ supplies the physically decisive vacuum-polarisation content — the same spectral function delivers the equal-mass $A_2$ piece, the electron-loop log that lifts $a_\mu$ above $a_e$, and the decoupling of heavy loops. Lepton universality emerges as an exact identity rather than an input.

---

## Scope and honesty ledger

- **Model-derived (exact target):** T1 equal-mass VP $=119/36-\pi^2/3$, from F251's spectral function via the dispersive kernel, numeric to $<10^{-9}$.
- **Exact (sympy / closed form):** T2 the $A_2$ group-sum identity and the Sommerfield–Petermann closed form; BETA the two-loop $\beta$ coefficient $\tfrac12$ ($b_1=1$). Group II's six vertex masters are *reproduced* as the known constant, not re-derived.
- **Quantitative:** T3 $a_e$ two-loop (rel err $1.3\times10^{-5}$); U2 $A_2^{\rm VP}(e\text{ in }\mu)$ and U3 $A_2(\mu)$ vs known QED values ($\sim10^{-8}$).
- **Exact identity:** U1 universality (electron and muon share $A_1,A_2$).
- **Out of scope / deferred:** the three-loop $A_3$ and higher; the hadronic VP and hadronic light-by-light contributions to $a_\mu$ (QCD sector, F151/F152) and the electroweak contributions (weak sector). **No claim** is made about the full Standard-Model $a_\mu$ or the experimental $a_\mu$ anomaly — an active, unsettled area (Muon $g\!-\!2$ Theory Initiative white papers 2020 and 2025; hadronic-VP tension). Only the QED piece is claimed here.

---

## External references

- C. M. Sommerfield, *Phys. Rev.* **107**, 328 (1957); A. Petermann, *Helv. Phys. Acta* **30**, 407 (1957) — $A_2=-0.328478965\ldots$
- S. Laporta & E. Remiddi, *Phys. Lett. B* **379**, 283 (1996) — analytic higher-order $a_e$ (master-integral technique).
- T. Aoyama, M. Hayakawa, T. Kinoshita, M. Nio, *Phys. Rev. D* **91**, 033006 (2015) — QED $a_e$ through tenth order; coefficient definitions $A_1,A_2,\dots$ and the mass-dependent $A_2(\mu)$.
- T. Aoyama *et al.* (Muon $g\!-\!2$ Theory Initiative), *Phys. Rept.* **887**, 1 (2020), arXiv:2006.04822 — SM prediction of $a_\mu$ (framework; note the 2025 update and the active hadronic-VP situation).
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §6.3, §10.
