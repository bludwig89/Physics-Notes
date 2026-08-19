# F34 — W_μ Phase 4: Covariant Dirac Doublet — Fermion-W Vertex

**Date:** 2026-05-24  
**Status:** Confirmed — 5/5 tests PASS  
**Module:** `ca-simulation/ca_wmu.py`  
**Tests:** `tests/findings/test_wmu_phase4.py` (W4.1–W4.5)  
**Results:** `test-results/wmu_phase4.json`  
**Roadmap:** `roadmap-wmu-implementation.md` Phase 4
**Test record:** record `wmu-phase4` (tier battery) — `tests/registry/`, D9. Declared 2026-08-19 - 13:19.

---

## Summary

Phase 4 wires the dynamical SU(2) gauge field into the Dirac doublet stepper. The covariant step implements `covariant_dirac_doublet_step` — a Strang-split kinetic+mass step in which the left-handed $\eta = (\nu_L, e_L)$ doublet couples to the W links while the right-handed $\chi$ sector uses identity links. This closes Limitation 1 (dynamical gauge field) and Limitation 2 (full covariant Dirac doublet) from F27. All five correctness tests pass.

---

## Key Results

| Test | Description | Residual | Target | Status |
|------|-------------|----------|--------|--------|
| W4.1 | SU(2)_L Ward identity: full covariant step | $1.687 \times 10^{-17}$ | $\le 10^{-14}$ | ✓ PASS |
| W4.2 | Isospin charges conserved ($g=0$) | $2.741 \times 10^{-17}$ | $\le 10^{-13}$ | ✓ PASS |
| W4.3 | Right-handed $\chi$ decoupled from W at $m=0$ | $0.0$ | exact | ✓ PASS |
| W4.4 | Left-right asymmetry: $\|$LHS$\|$ ≠ $\|$RHS$\|$ for non-trivial $W$ | $> 10^{-6}$ | structural | ✓ PASS |
| W4.5 | Weak neutral current residual (T³ coupling) | $1.854 \times 10^{-13}$ | $\le 10^{-12}$ | ✓ PASS |

---

## Strang-Split Covariant Step Architecture

The doublet step uses operator splitting: kinetic half-step → mass step → kinetic half-step.

$$\psi(t+dt) = K(dt/2)\,M(dt)\,K(dt/2)\,\psi(t)$$

**Kinetic step $K$:** Left-handed $\eta$ is propagated with the covariant BCC Weyl step using the W link field. Right-handed $\chi$ is propagated with identity links (no SU(2)_L coupling):

$$\eta \to U_\text{links}[\eta], \qquad \chi \to \text{identity}[\chi]$$

**Mass step $M$:** The complex-mass (Stueckelberg) coupling from F27 mixes $\eta$ into $\chi$:

$$\begin{pmatrix}\eta \\ \chi\end{pmatrix} \to \begin{pmatrix}\cos(m\,dt)\,\eta + i\sin(m\,dt)\,U_m^\dagger\,\chi \\ i\sin(m\,dt)\,U_m\,\eta + \cos(m\,dt)\,\chi\end{pmatrix}$$

where $U_m(x) \in \mathrm{SU}(2)$ is the mass-link field.

---

## W4.1 — Full Ward Identity

The Ward identity for the full Strang-split step:

$$V(x)\cdot\mathrm{step}(\psi; U) = \mathrm{step}(V(x)\cdot\psi;\; V\cdot U\cdot V^\dagger)$$

holds to $1.687\times10^{-17}$, which is below the machine-epsilon floor for a single FFT round-trip. The proof follows by induction on the split: the kinetic step satisfies the Ward identity by the covariant construction; the mass step satisfies it by F27's mass Ward identity (Tier 1 #66). Their Strang composition inherits both identities.

---

## W4.3 — Right-Handed Decoupling at $m=0$

With $m=0$, the mass step has $\sin(0)=0$, so the $\eta$–$\chi$ coupling vanishes identically:

$$M(dt)\big|_{m=0} = I$$

The kinetic step applies identity links to $\chi$. Therefore $\chi$ evolves under identity links regardless of $U_\text{links}$: changing the W field leaves $\chi$ completely unchanged. This is exact (residual $0.0$, bit-for-bit), not just small.

**Physical interpretation:** At $m=0$ the right-handed sector is a complete spectator to the SU(2)_L gauge field, as required by chiral gauge theory. With $m\ne 0$ the mass coupling mixes $\eta$ (which depends on $U_\text{links}$) into $\chi$ — correct physics, not a model error.

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| F27 — Chiral SU(2) doublet | F34 extends F27 from pure-gauge background to dynamical W_μ links (F33 plaquette) |
| F33 — Yang–Mills self-coupling | W links updated by plaquette action; F34 tests fermion response to those links |
| F32 — Free W propagation | Fermion back-reaction on W propagation is not yet included (Phase 4 is one-way coupling) |

---

## Implementation Notes

**JSON serialization:** The test runner requires `_NumpyEncoder(json.JSONEncoder)` to handle `np.bool_`, `np.integer`, and `np.floating` types returned by numpy operations on test results. Without this, `json.dump` raises `TypeError: Object of type bool_ is not JSON serializable`.

**m=0 requirement for W4.3:** Earlier versions of the test used `m=0.1`, which caused a residual of $3.5\times10^{-3}$ — not because of a code bug but because the Dirac mass term correctly mixes $\eta$ into $\chi$ even for small $m$. The fix is $m=0$, which gives exactly zero decoupling by construction.

---

## Files

- `ca-simulation/ca_wmu.py` — `covariant_dirac_doublet_step`, `isospin_charges`
- `tests/findings/test_wmu_phase4.py` — W4.1–W4.5 (with `_NumpyEncoder` fix)
- `test-results/wmu_phase4.json` — numerical results
