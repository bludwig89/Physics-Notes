# F208 — Relativistic (F125 Dirac–Coulomb) ionization energies in the multi-electron SCF, and the light-element accuracy map

**Date:** 2026-07-01 - 00:30
**Status:** Confirmed — 7/7 checks PASS (`test_F208_relativistic_scf_ie.py`). The F125 scalar Dirac–Coulomb shift is now wired into the Hartree SCF; a Z=1–20 sweep quantifies where the multi-electron accuracy breaks down.
**Module:** `ca-simulation/ca_manybody.py` — `_scalar_relativistic_shift_Ha` + `electron_cloud_hartree(..., relativistic=True)`.
**Tests:** `tests/findings/test_F208_relativistic_scf_ie.py`
**Results:** `test-results/F208_relativistic_ie_sweep.json`
**Cross-refs:** [[F125-p5-hydrogen-atom-em-bound-state]] (the Dirac–Coulomb / Sommerfeld fine structure this imports), [[F157-manybody-nuclei-and-electron-clouds]] (the Hartree SCF this extends), [[F195-blockspin-element-atom]] (the live element atom that consumes the same Aufbau/Hartree structure), [[F123-p6-si-scale-matter-sector]] (the m_e/α anchors that set the absolute eV)

---

## Summary

The non-relativistic multi-electron SCF (F157) is given the **F125 relativistic
correction**: the scalar Dirac–Coulomb (mass-velocity + Darwin) $O((Z\alpha)^4)$
shift, applied per orbital with the orbital's own screened effective charge. A
Z=1–20 sweep of first ionization energies against CRC/NIST then **maps where the
construction's accuracy actually breaks down** — and the answer is unambiguous:

> The light-element ionization-energy error is set by the **Hartree (no
> exchange-correlation) + Koopmans** approximation, **not** by relativity. The
> relativistic correction to the valence ionization energy is **< 0.6 meV for
> every element H→Ca**, while the SCF error against experiment is **−15 % to
> −40 %** from lithium onward (mean 28 %).

## The correction (F125 → SCF)

Each orbital's non-relativistic energy fixes a hydrogenic effective charge
$Z_\text{eff}=n\sqrt{-2\varepsilon}$; the scalar (spin-averaged) Dirac shift is

$$\Delta E_{n\ell} = -\frac{Z_\text{eff}^4\,\alpha^2}{2 n^4}\,\Big(C(n,\ell)-\tfrac34\Big),\qquad C(n,0)=n,\quad C(n,\ell\ge1)=\frac{n}{\ell+\tfrac12},$$

the $(2j+1)$-weighted average of the F125 fine-structure factor $n/(j+\tfrac12)$
(for $\ell=0$ only $j=\tfrac12$ exists, so $C=n$, **not** $n/(\ell+\tfrac12)$ — the
one subtlety). This reproduces the F125 hydrogen $1s$ shift exactly:
$\Delta E_{1s}(\mathrm H)=-\alpha^2/8\ \text{Ha}=-0.181\ \text{meV}$. Only $\alpha$
and $m_e$ enter (the F125/F123 anchors). It is the **direct** relativistic shift;
the **indirect** effect (relativistic core contraction feeding back into valence
screening) needs a self-consistent Dirac–Fock solve and is not included — flagged,
and irrelevant at this Z range.

## The accuracy map (Z = 1–20, first ionization energy, eV)

| Z | el | HOMO | IE (SCF) | IE (CRC/NIST) | err | rel. shift | 1s core rel. |
|---|----|------|---------:|--------------:|----:|-----------:|-------------:|
| 1 | H | 1s | 13.599 | 13.598 | **+0.0 %** | 0.181 meV | −0.000 eV |
| 2 | He | 1s | 23.980 | 24.587 | −2.5 % | 0.563 meV | −0.001 eV |
| 3 | Li | 2s | 4.613 | 5.392 | −14.5 % | 0.104 meV | −0.004 eV |
| 4 | Be | 2s | 7.472 | 9.323 | −19.8 % | 0.273 meV | −0.015 eV |
| 6 | C | 2p | 7.969 | 11.260 | −29.2 % | 0.145 meV | −0.083 eV |
| 10 | Ne | 2p | 14.447 | 21.565 | −33.0 % | 0.477 meV | −0.593 eV |
| 15 | P | 3p | 6.357 | 10.487 | **−39.4 %** | 0.198 meV | −2.510 eV |
| 18 | Ar | 3p | 10.070 | 15.760 | −36.1 % | 0.496 meV | −4.311 eV |
| 20 | Ca | 4s | 3.933 | 6.113 | −35.7 % | 0.197 meV | −5.728 eV |

(full 20-element table in the results JSON). Aggregate over Z=2–20: mean
$|\text{err}|$ **27.7 %**, median 29.2 %, worst 39.4 % (P).

## What this says

1. **Hydrogen is exact** (one electron, +0.004 %) and **helium is good** (−2.5 %,
   the F157 number). The accuracy **breaks at lithium** — the first atom where a
   second shell and electron exchange matter — and never recovers: every
   many-electron IE is **underbound by 15–40 %**, with a characteristic
   intra-period rise (e.g. Na→Ar: −22 %→−36 %).
2. **The error is exchange-correlation, not relativity.** The sign is
   systematically negative — the Hartree mean field omits the exchange
   self-interaction correction that deepens valence orbitals, and Koopmans omits
   orbital relaxation on ionization. Both push the IE **down**, exactly as seen.
3. **Relativity is correctly negligible here.** The valence IE shift never exceeds
   **0.6 meV** through Ca — ~4 orders of magnitude below the eV-scale SCF error —
   because the valence $Z_\text{eff}\sim1$–2 makes $\Delta E\propto Z_\text{eff}^4\alpha^2$
   tiny. Relativity is **not** the light-element ceiling.
4. **Where relativity does grow:** the $1s$ **core** shift climbs from −0.6 eV
   (Ne) to −4.3 eV (Ar) to −5.7 eV (Ca), a log–log slope of **3.38** vs Z — the
   $\sim Z^4$ fine-structure law. So the machinery is live and correct; it simply
   acts on the deep core, becoming a leading **valence** effect only for heavy
   atoms (high-Z, the superheavy regime), which this light sweep does not reach.

## Decision / scope

- **Built & certified:** relativistic ionization energies are now available from
  the SCF (`relativistic=True`), reproducing the F125 hydrogen anchor exactly and
  scaling as $Z^4$ in the core. The non-relativistic path is unchanged (F157
  regression intact).
- **The quantified ceiling for light elements is exchange-correlation**, not
  relativity. To reach chemical accuracy on IEs the next step is **exchange**
  (Hartree–Fock) and a relaxation/ΔSCF or correlation term — *not* a finer
  relativistic treatment. A self-consistent Dirac–Fock build would only matter
  for heavy/superheavy valence chemistry.
- This directly answers the element-prediction question (prior session): the
  construction **reproduces** known light-element IEs only at the Hartree tier
  (~30 % underbinding), so it is not yet a tool for predicting undiscovered
  elements; the gating physics is XC for light atoms and Dirac–Fock + nuclear
  shell structure for heavy/superheavy ones.
