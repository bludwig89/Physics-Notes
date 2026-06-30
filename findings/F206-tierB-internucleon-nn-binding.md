# F206 — Tier-B inter-nucleon NN one-boson-exchange binding (closes the F195 frontier)

**Date:** 2026-06-30 - 23:40
**Status:** Confirmed — 6/6 checks PASS (`test_F206_internucleon_nn_binding.py`). Closes the documented F195 Tier-B frontier: the live nucleons are now mutually bound by the model's own NN one-boson-exchange.
**Module:** `src/casim/particles/channel.py` — `ElementAtomChannel._setup_nn_potential` + `_apply_nn_binding` (wiring), `nn_binding`/`g_nn` config.
**Tests:** `tests/findings/test_F206_internucleon_nn_binding.py`
**Results:** `test-results/F206_internucleon_nn_binding.json`
**Cross-refs:** [[F195-blockspin-element-atom]] (the Tier-B atom whose frontier this closes), [[F104-p4-deuteron-tensor-bound-nucleus]] / [[F126-nn-intermediate-range-sigma-attraction]] / [[F128-nn-short-range-omega-repulsion]] / [[F113-nn-short-range-repulsive-core]] (the four OBE channels assembled), [[F136-realspace-scalar-confinement]] (the MIT-bag scalar-mass mechanism reused), [[F157-manybody-nuclei-and-electron-clouds]] (the static A-body variational cousin)

---

## Summary

F195 built a live block-spin atom in which each nucleon's three colour-Dirac
quarks are confined to their own centre of mass, but it left the **A nucleons
mutually unbound** — its own words:

> *"the inter-nucleon one-boson-exchange binding (σ F126 + ω F128 + π-tensor F104
> + quark-Pauli core F113) is not yet wired into Tier B … the A nucleons are not
> mutually bound. This is the documented Tier B frontier."*

This finding **wires and certifies** that binding. The model's static
nucleon–nucleon one-boson-exchange potential (already assembled and validated on
the deuteron in `ca_nuclear.py`) is now applied as a live, exactly-unitary force
between the live nucleon clusters. The two nucleons of the deuteron, started at
their unbound seed separation, are pulled to a **bounded equilibrium** and stay
there; the four nucleons of He-4 contract into a bound cluster; norm and charge
stay machine-precision throughout.

## The wired potential (model-native, no experimental nucleus)

The central pair potential cached per simulation is

$$V_\text{pair}(r) = V_\sigma(r) + V_\omega(r) + V_\text{core}(r) - V_0\,e^{-r^2/2R_0^2},\qquad R_0 = \hbar c/m_\pi,$$

with the three repulsive/attractive meson channels taken **unchanged** from their
own findings — σ-isoscalar attraction (F126), ω-isoscalar-vector repulsion
(F128), quark-Pauli colour-magnetic core (F113) — and the last term the folded
S=1,T=0 π-tensor attraction (F104). The single depth $V_0$ is fixed so the
two-body variational energy reproduces the **model's own** deuteron binding
($E_b = 2.234$ MeV, `ca_manybody._model_deuteron_binding`); **no measured nucleus
calibrates it**. The solved cache for this run:

| quantity | value |
|---|---|
| anchor $E_b$ (model deuteron) | 2.234 MeV |
| fitted depth $V_0$ | 167.7 MeV |
| range $R_0=\hbar c/m_\pi$ | 1.430 fm |
| well minimum $V_\text{pair,min}$ | −49.1 MeV |

## The mechanism — exactly-unitary scalar-mass binding

Each nucleon $i$ feels the superposed OBE field of the **other** nucleons as a
position-dependent **Lorentz-scalar mass** (the F136 MIT-bag mechanism — a scalar
mass binds to a standing state, whereas a vector kick would only heat / Klein-
tunnel):

$$S_i(\mathbf x) = g_\text{nn}\sum_{j\ne i} V_\text{pair}\big(|\mathbf x - \mathbf R_j|\big),\qquad \mathbf R_j = \text{live nucleon COMs},$$

applied as one $\eta\leftrightarrow\chi$ rotation $\theta = S_i$ per tick
(`_mix_eta_chi_3d`), operator-split after the channel's kinetic + intra-nucleon
confinement step. The rotation is norm-preserving for **any** $\theta$, so the
binding is added with **zero** cost to unitarity. The default coupling is
$g_\text{nn}=0.012$.

## Certification (6/6, `test_F206_internucleon_nn_binding.py`)

| # | check | result |
|---|---|---|
| C1 | exact unitarity under binding | quark-norm drift $9.4\times10^{-14}$ |
| C2 | charge conserved, +Z from live ρ_em | $Q=1.0000$ (deuteron), $2.0000$ (He) to $<10^{-12}$ |
| C3 | binding contracts the deuteron | sep $4.75\to2.56$ cells (ON) vs $4.75\to4.02$ (OFF) |
| C4 | bounded equilibrium (no collapse/divergence) | late-time sep $\{2.67,2.59,2.58,2.56\}$, variation $<2\%$ |
| C5 | repulsive core sets the floor | $g{=}0.03$ settles **wider** (2.77) than $g{=}0.012$ (2.56) |
| C6 | He-4 cluster binds | COM-RMS $\to0.61$ (ON) vs $1.07$ (OFF); norm $6\times10^{-14}$ |

The decisive checks are C4 and C5. The bound cluster **saturates** at a finite
separation rather than collapsing to a point, and a 2.5× stronger coupling
settles the deuteron at a **larger**, not smaller, separation — proof that the
equilibrium is governed by the model's **repulsive core** (F113 quark-Pauli +
F128 ω), exactly as a physical NN potential must behave, and not by the numerical
value of $g_\text{nn}$. The equilibrium np separation, $\approx 2.5$–2.8 cells
$\approx 2.5$–2.8 fm at the run's $1$ fm/cell scale, is the right order for the
deuteron (rms matter radius $\sim 2$ fm).

## Scope — what is certified vs residual

- **Certified:** a genuine, model-native, exactly-unitary inter-nucleon force is
  now live in Tier B; it binds both the 2-body (deuteron) and 4-body (He-4)
  clusters to a bounded equilibrium set by the model's own repulsive core, with
  charge/norm machine-precision and the potential calibrated only to the model
  deuteron.
- **Residual (separate frontier, NOT inter-nucleon):** the F195 "He breathes
  ~50 %" figure is dominated by **intra-nucleon** blob spread — each nucleon's
  three-quark cloud grows $\sim$+100 % over 80 ticks **even with the inter-nucleon
  force off** (com-RMS, the actual inter-nucleon coordinate, drifts only −6.5 %
  unbound). That spreading is soft F136 intra-nucleon confinement, a distinct
  issue this binding does not address (and the scalar-mass mixing mildly heats);
  tightening the single-nucleon Y-string is the next Tier-B item. The
  inter-nucleon binding itself is the deliverable and is clean.

## Decision

The model NN one-boson-exchange — σ(F126) + ω(F128) + quark-Pauli core(F113) +
π-tensor(F104), depth-anchored to the model deuteron — is the canonical Tier-B
inter-nucleon binder, applied as an exactly-unitary scalar-mass (F136) factor.
This closes the F195 Tier-B frontier line for the inter-nucleon sector and leaves
single-nucleon confinement stiffness as the remaining live-quark frontier.
