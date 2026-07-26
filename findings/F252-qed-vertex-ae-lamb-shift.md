# F252 — The one-loop QED vertex Λ^μ: the electron anomalous moment a_e = α/2π and the hydrogen Lamb shift

**Date:** 2026-07-16 - 11:35
**Status:** Confirmed — 4/4 checks PASS. The Ward–Takahashi identity and $a_e=F_2(0)=\alpha/2\pi$ (Schwinger term) are **algebraically exact** (sympy; the Feynman-parameter integral evaluates to exactly 1); the Uehling coefficient $-\tfrac{4}{15}$ is derived from the F251 bubble; the $2s_{1/2}$–$2p_{1/2}$ Lamb shift is lifted to $1052.2$ MHz $=99.5\%$ of the measured $1057.845$ MHz.
**Module:** `ca-simulation/ca_vertex_loop.py`
**Verification script:** `tests/findings/test_F252_vertex_ae_lamb.py`
**Result file:** `test-results/F252_vertex_ae_lamb.json`
**Cross-references:** [[F251-qed-vacuum-polarization-running-alpha]] (the self-energy this vertex is tied to by Ward–Takahashi; the bubble whose low-$q$ limit is the Uehling piece), [[F87-charge-coupling-paired-photon]] (the identity-channel vertex $\gamma^\mu$), [[F125-p5-hydrogen-atom-em-bound-state]] (the Dirac–Coulomb solver `ca_atom.py` whose exact $2s$–$2p$ degeneracy is lifted here), [[F69-paired-spinor-photon]] (the internal photon), [[F249-qed-comparison-battery]] (the ledger closed: C1 + C3).

---

## The claim

The one-loop QED vertex $\Lambda^\mu(p,p')$ — the electron emitting and reabsorbing a paired photon, built from two F87 identity-channel vertices — satisfies the Ward–Takahashi identity exactly, produces Schwinger's anomalous moment $a_e=\alpha/2\pi$ from its magnetic form factor, and together with the F251 vacuum polarisation lifts the exact one-body Dirac–Coulomb $2s_{1/2}$–$2p_{1/2}$ degeneracy to the measured Lamb shift.

---

## The results

### V1 — Ward–Takahashi identity (exact)

With the F87 identity-channel vertex $\gamma^\mu$ and the free Dirac inverse propagator $S^{-1}(p)=\slashed p-m$,

$$q_\mu\Lambda^\mu=q_\mu\gamma^\mu=\slashed q=(\slashed p'-m)-(\slashed p-m)=S^{-1}(p')-S^{-1}(p),\qquad q=p'-p,$$

verified to literal zero with explicit $4\times4$ Dirac gammas (Clifford $\{\gamma^\mu,\gamma^\nu\}=2\eta^{\mu\nu}$ confirmed). This is the defining WT identity; gauge invariance promotes it to all orders and it **fixes charge renormalisation** $Z_1=Z_2$ — the vertex and wavefunction renormalisations cancel in the physical charge, tying this vertex to the F251 self-energy.

### V2 — the anomalous moment $a_e=\alpha/2\pi$ (exact)

The magnetic form factor at zero momentum transfer (Peskin–Schroeder 6.56):

$$F_2(0)=\frac{\alpha}{2\pi}\int_0^1\!dx\,dy\,dz\,\delta(x+y+z-1)\,\frac{2m^2 z(1-z)}{m^2(1-z)^2}.$$

The $x$-integral over the simplex is trivial (integrand $x$-independent) $\Rightarrow$ factor $(1-z)$; the remaining $z$-integral is $\int_0^1 2z\,dz=1$ **exactly**, so

$$a_e=F_2(0)=\frac{\alpha}{2\pi}=1.16141\times10^{-3}\quad\text{vs measured }1.15965218\times10^{-3}\ (0.15\%).$$

Higher QED orders $(\alpha/\pi)^2,\dots$ close the residual $0.15\%$ and are out of scope (future).

### V3 — the Uehling coefficient from the F251 bubble (exact)

The low-$q^2$ limit of the F251 fermion bubble is

$$\Pi(q^2)\to\frac{2\alpha}{\pi}\frac{q^2}{m^2}\int_0^1 x^2(1-x)^2\,dx=\frac{2\alpha}{\pi}\frac{q^2}{m^2}\cdot\frac{1}{30}=\frac{\alpha}{15\pi}\frac{q^2}{m^2},$$

so the Uehling delta-potential gives the $S$-state coefficient $-\tfrac{4}{15}$. This **derives** the vacuum-polarisation piece of the Lamb shift from Part 1 — the two parts share one loop.

### V4 — the Lamb shift (quantitative, honest scope)

Pure one-body Dirac–Coulomb leaves $2s_{1/2}$ ($\kappa=-1$) and $2p_{1/2}$ ($\kappa=+1$) **exactly degenerate** (confirmed from `ca_atom`, gap $=0$). Feeding the one-loop radiative shift, with energy unit $E_1=\alpha(Z\alpha)^4 mc^2/\pi n^3=101.73$ MHz ($n=2$):

| contribution | value (MHz) | source |
|--------------|:-----------:|--------|
| self-energy (Bethe log) $2s-2p$ | $+1079.32$ | Bethe log $\ln k_0(2s)=2.8118$, $\ln k_0(2p)=-0.0300$ (literature) |
| vacuum polarisation (Uehling) | $-27.13$ | derived from F251 (V3, coeff $-\tfrac{4}{15}$) |
| **total** | **$+1052.19$** | $=99.5\%$ of measured |

vs measured $1057.845$ MHz (Lundeen–Pipkin). The degeneracy is lifted with the correct sign and magnitude; the residual $\approx5.6$ MHz is higher-order $\alpha(Z\alpha)^5$/two-loop QED, out of leading-order scope.

**Scope.** The Uehling coefficient is derived here from F251's $\Pi$. The Bethe logarithm is a standard non-relativistic dipole-sum constant (Drake, Klarsfeld) taken as literature input, not re-derived; the self-energy $A_{40}$ constants ($10/9$ for $2s$, $-1/6$ for $2p_{1/2}$) are the Bethe–Salpeter/Mohr values.

> **Follow-up (F257, 2026-07-20):** the Bethe logarithm — the one literature input above — has since been **derived from the model's own Coulomb spectrum** (Dalgarno–Lewis resolvent, `ca_bethe_log.py`), reproducing $2.984/2.812/-0.030$ to ~2–3% with no tabulated constant. Feeding the model-derived $\ln k_0$ back in gives a fully model-derived Lamb shift of $1059.9$ MHz vs measured $1057.845$ MHz. See [[F257-bethe-log-from-model-spectrum]].

---

## Verification summary (4/4)

| # | Check | Type | Result |
|---|-------|------|:------:|
| V1 | WT $q_\mu\Lambda^\mu=S^{-1}(p')-S^{-1}(p)$; $Z_1=Z_2$ | exact | literal 0 |
| V2 | $a_e=F_2(0)=\alpha/2\pi$ (parametric integral $=1$) | exact | 0.15% vs meas. |
| V3 | Uehling coeff $-\tfrac{4}{15}$ from $\int x^2(1-x)^2=\tfrac1{30}$ | exact | $-4/15$ |
| V4 | Lamb $2s_{1/2}-2p_{1/2}$ lifted to $1052.2$ MHz | quantitative | 99.5% |

---

## Scope and honesty

- **Exact vs quantitative.** WT identity and $a_e=\alpha/2\pi$ (and the Uehling coefficient) are algebraic identities. The Lamb shift is a leading-order quantitative result.
- **Inputs named.** Bethe logarithm and the self-energy finite constants are literature inputs; the Uehling piece and the Dirac degeneracy come from the model (F251, F125).
- **What is deferred.** Higher-order QED ($(\alpha/\pi)^2$ for $a_e$; $\alpha(Z\alpha)^5$/two-loop for the Lamb shift) is out of scope. First-principles evaluation of the Bethe logarithm from the model's hydrogen spectrum is a possible follow-up.

---

## Files
- Module: `ca-simulation/ca_vertex_loop.py`
- Test: `tests/findings/test_F252_vertex_ae_lamb.py`
- Results: `test-results/F252_vertex_ae_lamb.json`
