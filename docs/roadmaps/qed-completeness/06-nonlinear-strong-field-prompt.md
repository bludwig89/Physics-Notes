# Session prompt — nonlinear and strong-field QED: Euler–Heisenberg light-by-light and Schwinger pair production

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Build the **nonlinear / non-perturbative** corner of QED — the physics that has no classical Maxwell analogue:

1. **The Euler–Heisenberg effective Lagrangian** — the one-loop four-photon effective action from integrating out the electron, giving **light-by-light scattering** ($\gamma\gamma\to\gamma\gamma$) and strong-field vacuum birefringence.
2. **Schwinger pair production** — the non-perturbative rate of $e^+e^-$ creation from a strong static electric field, $\propto\exp(-\pi E_\text{crit}/E)$ with the critical field $E_\text{crit}=m^2c^3/e\hbar$.

## Why this is tractable now (read first)

- **F251** (`ca-simulation/ca_vacuum_polarization.py`) — the electron loop with photon external legs; Euler–Heisenberg is the same electron loop with **four** external photon legs (the box), in the low-frequency/constant-field limit. Reuse the fermion-loop machinery.
- **F250 / F69** (`ca_photon_pair.py`) — the external photons are the even-law paired photon; the light-by-light amplitude must respect the F250 transverse structure and gauge invariance (the amplitude vanishes when any photon polarization → its momentum).
- **F27/F46** (`ca_bcc.py`) — the internal electron loop; Schwinger production is this fermion in a background $E$-field (the Sauter–Schwinger tunneling of the Dirac sea).
- **F249** B1 — zero *linear* vacuum birefringence (confirmed); Euler–Heisenberg gives the *nonlinear* field-induced birefringence — the physical, non-zero effect, distinct and consistent.

## What to build

1. **Euler–Heisenberg effective Lagrangian — algebraic gate.** From the one-loop electron determinant in a constant EM background, the leading four-field term is
   $$\mathcal L_\text{EH}=\frac{2\alpha^2}{45 m^4}\Big[(\mathbf E^2-\mathbf B^2)^2+7(\mathbf E\cdot\mathbf B)^2\Big].$$
   Derive the coefficients $2\alpha^2/45$ and the relative weight $7$ (the box-diagram result) — sympy where possible. These are the targets.
2. **Light-by-light $\gamma\gamma\to\gamma\gamma$ — quantitative + gauge gate.** From $\mathcal L_\text{EH}$ (low-energy limit), the cross section $\sigma_{\gamma\gamma}\propto\alpha^4\omega^6/m^8$; reproduce the low-energy coefficient and verify Bose symmetry + gauge invariance (Ward on all four photons — exact gate). Note the high-energy regime (full box) and the ATLAS PbPb observation of $\gamma\gamma\to\gamma\gamma$ as the measured contact point.
3. **Field-induced vacuum birefringence — quantitative.** From $\mathcal L_\text{EH}$, the two polarizations of a probe photon in a strong background $B$ acquire different refractive indices $n_\parallel-1=\tfrac{7}{2}\cdot\tfrac{2\alpha^2}{45}\tfrac{B^2}{m^4}$, $n_\perp-1=\tfrac{4}{2}\cdot(\dots)$ (ratio $7\!:\!4$). Reproduce the $7\!:\!4$ birefringence ratio — the nonlinear counterpart of F249's zero *linear* birefringence.
4. **Schwinger pair-production rate — quantitative/non-perturbative.** The vacuum persistence / pair-creation probability per unit volume-time,
   $$w=\frac{(eE)^2}{4\pi^3}\sum_{n=1}^\infty \frac{1}{n^2}\exp\!\Big(-\frac{n\pi m^2}{eE}\Big),$$
   with critical field $E_\text{crit}=m^2/e\simeq1.32\times10^{18}\,\text{V/m}$. Reproduce the exponent $\pi m^2/eE$ and $E_\text{crit}$; you may compute it as the imaginary part of the effective action or as Dirac-sea tunneling in a background-$E$ CASIM run.

## Method + hygiene

- Exactness ladder: the $2\alpha^2/45$ and $7\!:\!1$ / $7\!:\!4$ coefficients (sympy), then light-by-light + birefringence quantitatively, then the Schwinger exponent/critical field. Record in `docs/status/exactness-inventory.md`.
- The four-photon amplitude must be transverse and gauge-invariant on the F250 paired photon; check Ward on every leg. No `eig` on chiral matrices.
- The Schwinger rate is non-perturbative — either the ImL route (analytic) or a background-field CASIM tunneling run; if the latter exceeds the sandbox, emit a `tests/runners/run_*` JSON per CLAUDE.md.
- Deliverables: `ca-simulation/ca_euler_heisenberg.py`, `ca-simulation/ca_schwinger_pair.py`, tests, JSON, finding. `grep` the true max first (suggested F263). Regen indexes, changelog, exactness-inventory.

## Definition of done

The Euler–Heisenberg coefficients $2\alpha^2/45$ and the $7\!:\!1$ invariant weight derived; light-by-light cross section + the $7\!:\!4$ field-induced birefringence ratio reproduced with gauge invariance exact; and the Schwinger exponent $\pi m^2/eE$ with $E_\text{crit}=m^2/e$ reproduced. The model then covers nonlinear and non-perturbative QED, not just perturbative diagrams.

## External references

- W. Heisenberg & H. Euler, *Z. Phys.* 98, 714 (1936) — the effective Lagrangian (English translation arXiv:physics/0605038).
- V. Weisskopf, *Kong. Dansk. Vid. Selsk. Math-fys. Medd.* 14, 6 (1936) — the effective action / charge renormalization.
- J. Schwinger, *Phys. Rev.* 82, 664 (1951) — "On Gauge Invariance and Vacuum Polarization"; pair production and the effective action.
- ATLAS Collaboration, *Nature Phys.* 13, 852 (2017) — evidence for light-by-light scattering $\gamma\gamma\to\gamma\gamma$ in Pb+Pb collisions (measured contact point).
- G. V. Dunne, "Heisenberg–Euler effective Lagrangians," in *From Fields to Strings* (2004), arXiv:hep-th/0406216 — modern review (light-by-light, birefringence, Schwinger).
