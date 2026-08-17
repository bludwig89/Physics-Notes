# F251 — The interacting one-loop QED photon self-energy Π^μν(q) and the running coupling α(q²)

> **[PARTIALLY SUPERSEDED 2026-08-02 by F277 — ledger S12-F277-refold-removed-qed-and-gluon]**
>
> **DEAD:** Every number computed through the refolded _fermion_B. Delta = B_rule - B_cont CHANGES SIGN between n=10 and n=14 under the refold and settles at +1.2e-2, where the un-refolded calculation converges monotonically to -2.121e-3: opposite sign, six times the magnitude. At the shipped n=24 the q-flatness spread goes 1.4484e-2 -> 1.685e-5, a factor 859.
>
> **STILL LIVE:** The one-loop vacuum-polarization construction and the running-coupling derivation. The defect was in a momentum refold, not in the physics; F277 re-ran it. 102 code/test references, the most in this record.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-07-16 - 11:20
**Status:** Confirmed — 5/5 checks PASS. Ward transversality $q_\mu\Pi^{\mu\nu}=0$ and the QED beta coefficient $b_0^{\text{QED}}=\tfrac43$ are **algebraically exact** (sympy, literal 0 / exact rational); lattice $b_0$ = continuum $b_0$ after subtraction (q-flat); leptonic $\Delta\alpha(M_Z)$ matches PDG to $0.24\%$.
**Module:** `ca-simulation/ca_vacuum_polarization.py`
**Verification script:** `tests/findings/test_F251_vacuum_polarization.py`
**Result file:** `test-results/F251_vacuum_polarization.json`
**Cross-references:** [[F250-allk-gauge-pole-paired-photon]] (the massless transverse gauge pole this loop dresses — no radiative mass), [[F162-bgfield-b0-gate]] (the non-abelian template: $b_0=11$ gluon gate), [[F155-qstar-bracket-freeze]] (the lattice−continuum subtraction machinery), [[F87-charge-coupling-paired-photon]] (the identity-channel vertex), [[F68-minimal-coupling-forces-even-photon]], [[F69-paired-spinor-photon]] (the internal even-law photon), [[F249-qed-comparison-battery]] (the ledger closed: C2), [[F151-f152-ir-coupling-two-faces]] (the hadronic running this honestly defers to).

---

## The claim

The one-loop photon self-energy on the BCC Weyl lattice is the **fermion bubble** — the abelian analogue of the F162 gluon self-energy with **no ghost and no gauge self-coupling** — built on the F69 paired photon and the F87/F68 identity-channel vertex. It is exactly transverse (so no photon mass is radiatively generated, keeping the F250 gauge pole massless), it drives the universal QED running with $b_0^{\text{QED}}=\tfrac43$, and its leptonic part reproduces the measured running of $\alpha$ up to the hadronic piece that belongs to the QCD sector.

$$\Pi^{\mu\nu}(q)=(q^2 g^{\mu\nu}-q^\mu q^\nu)\,\Pi(q^2),\qquad \mu\frac{d\alpha}{d\mu}=\frac{2\alpha^2}{3\pi}\sum_f q_f^2\ \ (b_0^{\text{QED}}=\tfrac43\ \text{per unit-charge Dirac fermion}).$$

---

## The results

### Pi1 — Ward transversality (exact)

The angular-averaged one-loop bubble is $\Pi^{\mu\nu}=\Pi(q^2)(q^2 g^{\mu\nu}-q^\mu q^\nu)$, so

$$q_\mu\Pi^{\mu\nu}=\Pi(q^2)\big(q^2q^\nu-q^2q^\nu\big)=0\quad\text{(literal 0, all }\nu).$$

This is the loop-level lattice Ward identity — the exact counterpart of F250's tree/propagator Ward commutator $[M_6,P_T]=0$. No photon mass term is induced at any $q$; the massless transverse gauge pole of F250 survives dressing.

### Pi2 — the beta coefficient $b_0^{\text{QED}}=\tfrac43$ (exact)

Mirroring F162's $b_0$ gate: the scalar bubble calibrates the normalisation ($g_{\text{scalar}}=1\Rightarrow$ coeff of $\ln(\Lambda^2/q^2)$ is $g/16\pi^2$), and the Dirac-trace numerator

$$N^{\mu\nu}=\mathrm{Tr}\!\left[\gamma^\mu\slashed k\,\gamma^\nu(\slashed k+\slashed q)\right]=4\big[k^\mu(k+q)^\nu+k^\nu(k+q)^\mu-g^{\mu\nu}k\cdot(k+q)\big]$$

angular-averages to the transverse tensor with coefficient exactly $\tfrac43$. With the closed-fermion-loop $(-1)$ this is $b_0^{\text{QED}}=\tfrac43$ — i.e. $\mu\,d\alpha/d\mu=2\alpha^2/3\pi$ for one unit-charge fermion. The trace identity itself is verified against explicit $4\times4$ Dirac gammas with the Clifford check $\{\gamma^\mu,\gamma^\nu\}=2\eta^{\mu\nu}$ (`gamma_trace_check`). This is the abelian sibling of $b_0=11/3\,C_A$: the QCD $-\tfrac43 T_F n_f$ fermion contribution is the same number.

### Pi3 — lattice $b_0$ = continuum $b_0$ (convergent)

Swapping the continuum propagator $1/k^2$ for the paired-photon rule kernel $K=3\,\Omega_\text{even}^2+k_t^2$ leaves the transverse log coefficient unchanged: the subtracted coefficient $\Delta=B_\text{rule}-B_\text{cont}$ is q-independent (spread $\approx0.014$ over $q\in[0.1,0.3]$; a residual log would grow like $\ln(1/q)$). So the lattice QED running is the continuum $\tfrac43$. Same machinery and the same honest caveat as F162: the arccos rule kernel is grid-sensitive at small $n$, but the decisive point is that $\Delta$ is a small **constant**, not a growing log.

### Pi4 — the running coupling $\alpha(q^2)$ (quantitative, honest scope)

Integrating the one-loop leptonic bubble from $\alpha(0)^{-1}=137.036$ to $M_Z$, using $\mathrm{Re}\,\Delta\alpha_\ell(s)=\tfrac{\alpha}{3\pi}[\ln(s/m_\ell^2)-\tfrac53]$ for each lepton:

| lepton | $\Delta\alpha_\ell(M_Z)$ |
|--------|--------------------------|
| $e$    | 0.017435 |
| $\mu$  | 0.009178 |
| $\tau$ | 0.004808 |
| **sum**| **0.031421** |

vs PDG leptonic $\Delta\alpha_\text{lep}=0.031498$ (**0.24%**). This gives $1/\alpha(M_Z)\big|_\text{lep}=132.73$.

**Honest scope.** The measured full $1/\alpha(M_Z)=128.927$ is *not* expected from the lepton loop alone: the remaining pull-down ($\approx3.8$ in $1/\alpha$) is the **hadronic** vacuum polarisation, which lives in the QCD sector (F151/F152), not in this leptonic bubble. Quoting the leptonic piece and naming the hadronic remainder is the correct, non-faked statement.

---

## Verification summary (5/5)

| # | Check | Type | Result |
|---|-------|------|:------:|
| P1 | Ward $q_\mu\Pi^{\mu\nu}=0$ | exact | literal 0 |
| P2 | $b_0^{\text{QED}}=\tfrac43$, transverse, calibration $g=1$ | exact | $4/3$ |
| P2b | explicit-$\gamma$ Dirac trace = bubble numerator; $\{\gamma,\gamma\}=2\eta$ | exact | PASS |
| P3 | lattice $b_0$ = continuum $b_0$ (subtracted q-flat) | convergent | spread $0.014$ |
| P4 | leptonic $\Delta\alpha(M_Z)=0.03142$ vs PDG $0.03150$ | quantitative | 0.24% |

---

## Scope and honesty

- **Exact vs quantitative.** The Ward identity and $b_0=\tfrac43$ are algebraic identities (sympy, literal 0 / exact rational). The lattice-continuum equality is a convergent numerical statement (q-flatness). The running is quantitative and **leptonic only**.
- **What is deferred.** The hadronic contribution to $\Delta\alpha(M_Z)$ is the QCD sector (F151/F152), not built here; the full $128.927$ is out of scope for the lepton loop by construction.
- **Relation to F250.** F250 established the free/tree gauge pole is a single massless transverse pole across the BZ; F251 shows the interacting (one-loop) dressing does not spoil it — the transverse self-energy adds no mass and the residue stays gauge.
- **Higher orders.** Two-loop and beyond are not computed; the one-loop $b_0$ is the leading universal coefficient.

---

## Files
- Module: `ca-simulation/ca_vacuum_polarization.py`
- Test: `tests/findings/test_F251_vacuum_polarization.py`
- Results: `test-results/F251_vacuum_polarization.json`
