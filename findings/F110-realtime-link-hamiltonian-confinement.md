# F110 — Real-time link Hamiltonian evolution for the confinement sector: the F101 rotor made multi-plaquette and dynamical, with Gauss's law exact by construction

**Date:** 2026-06-06 - 23:55
**Status:** Confirmed — 7/7 checks PASS. C1/C2/C7 machine-precision/exact (direct-vs-dual spectral identity; λ=0 potential in integer arithmetic; rotor matrix identity); C3/C4 convergent/asymptotic (linear potential, strong-coupling PT); C5 machine-precision real-time unitarity; C6 quantitative (flux-tube localisation and persistence). **Closes audit B.2 item 2** ("real-time link Hamiltonian evolution (Kogut–Susskind-type) is not built; Wilson-loop tests run on frozen links").
**Module:** `ca-simulation/ca_link_hamiltonian.py`
**Script:** `tests/findings/test_F110_link_hamiltonian_realtime.py` (~30 s)
**Results:** `test-results/F110_link_hamiltonian_realtime.json`
**Cross-references:** [[F101-strong-coupling-sigma-compact-rotor]] (the single-plaquette rotor this makes multi-plaquette and real-time; χ map verified as a matrix identity), [[F100-gamma-from-transfer-operator]] (λ = χΩ² rule map), [[F99-sigma-as-centre-lagrange-multiplier]] / [[F97-baryon-no-go-centre-closure]] (why ℤ₃, the SU(3) centre, is the load-bearing group), [[F70-gradient-flow-confinement-string-tension]] (the frozen-link Euclidean area law this complements with energy-per-length), [[F94-lattice-gauge-mc-confinement-vs-F86]] (3+1D Euclidean σ, still the production route).

---

## 1. What this closes

Until now the confinement sector had three legs — the exact 2D Euclidean area law on frozen links (F70), the Monte-Carlo 3+1D σ (F94), and the exactly-solved single-plaquette transfer operator (F100/F101) — but **no real-time dynamics**: links never evolved under their own Hamiltonian, so questions like "does the flux string persist in time?" and the P2 dynamical-baryon dependency (audit C.8: confinement energy as a *dynamical* object) were out of reach. This finding builds that layer.

## 2. The construction

The Kogut–Susskind Hamiltonian on an open 2D spatial lattice (2+1D theory),

$$H=\frac{g^2}{2}\sum_\ell \hat E_\ell^2\;-\;\lambda\sum_p\cos\hat\phi_p,$$

is exactly the multi-plaquette generalisation of the F101 compact rotor $H=\frac{1}{2\chi}\hat E^2-\lambda\cos\hat\phi$: a single open plaquette has four exclusive boundary links, so $\frac{g^2}{2}\cdot4m^2=\frac{1}{2\chi}m^2$, i.e. $\chi=1/(4g^2)$, and $\lambda=\chi\Omega^2$ connects to the rule's rotation rate (F100/F101 S5). Verified as a **matrix identity** (C7, residual exactly 0).

**Gauss's law is solved, not imposed.** On the open lattice the constraint $(\mathrm{div}\,\hat E)(x)=q(x)$ is eliminated exactly by the dual (height) representation

$$\hat E_\ell=\hat m_{p^+(\ell)}-\hat m_{p^-(\ell)}+\eta_\ell,$$

with integer height operators $\hat m_p$ on plaquettes (outer face ≡ 0) and a fixed background $\eta$ (a string of $\eta=q$ links joining the static $\pm q$ charges, $\mathrm{div}\,\eta=q$). Every state of the height space is gauge-invariant; $\cos\hat\phi_p$ is the height raising/lowering operator. **C1 proves this is the gauge theory and not a model of it**: the full spectrum of the *direct* link-basis KS Hamiltonian restricted to the Gauss sector equals the dual spectrum to $1.9\times10^{-14}$, in vacuum **and** charged sectors, on ladder and 2×2 geometries.

**Groups.** ℤ₃ — the SU(3) centre that carries the area law (F97–F99) — has an *exact finite* Hilbert space (no truncation anywhere); compact U(1) — the F101 rotor's parent — is truncated at $|m|\le m_\text{max}$ with checked convergence ($3\times10^{-14}$, C7), the same policy as F101 S1.

## 3. Statics from the dynamical operator (C2–C4)

- **Strong coupling exact (C2, Tier 1).** At $\lambda=0$: $V(R)=\frac{g^2}{2}q^2R$ in integer arithmetic, residual $0.0$ (ℤ₃ R=1–6, U(1) R=1–4).
- **Linear potential at finite coupling (C3).** Lanczos ground states with a charge pair on a 10×1 ladder: the increment estimator $V(R)-V(R-1)$ converges (Cauchy < 0.4%), giving the Hamiltonian (energy-per-length) tension $\sigma(\lambda)$: $0.4923,\ 0.4303,\ 0.2354$ at $\lambda=0.2,\ 0.5,\ 1.0$ ($g^2{=}1$) — positive and monotone-decreasing, confining at all tested couplings.
- **PT cross-check (C4, asymptotic).** Programmatic second-order strong-coupling PT gives $\sigma(\lambda)=\frac{g^2}{2}-c_2\lambda^2+O(\lambda^3)$ with $c_2=1/6$ on the ladder; the ED ratio Richardson-extrapolates to $0.9992$ (the $O(\lambda^3)$ remainder is the genuine ℤ₃ winding channel $0\to1\to2\to0$).

## 4. Real time (C5–C6) — the new capability

- **Unitarity and energy conservation (C5).** Krylov evolution of a superposed state on a 4×2 grid (dim 6561, $t\in[0,20]$): norm drift $3\times10^{-15}$, $\langle H\rangle$ drift $2\times10^{-14}$; the Krylov path certified against dense-eigendecomposition evolution to $5\times10^{-13}$.
- **The flux tube is real and it persists (C6).** Background-subtracted observable: excess electric energy over the same-coupling vacuum profile. (i) The charged *ground state* localises its excess flux on the string row: fraction $0.608$ at $\lambda=0.5$ vs $0.312$ at $\lambda=4.0$ (uniform share $0.182$). (ii) **Real-time quench**: a bare string (heights-zero basis state) evolved at confining coupling **persists as a positive flux excess** (time-averaged string-row share $0.361\approx2\times$ uniform; total excess stays positive, min $+4.8$), while at weak coupling it **melts below the vacuum fluctuation level** (total excess $-8.0$) — confinement vs dissolution watched in real time.

## 5. Honest scope

- **Pure gauge with static charges.** Dynamical (quark) matter is not yet coupled; that coupling is the next leg of the P2 chain (audit C.8) — the link layer it needs now exists. The casim production engine is untouched; this is a `ca-simulation` model module (engine wiring is engineering, listed in next steps).
- **ℤ₃ / U(1), not the SU(3) Casimir ladder.** The centre-projection argument (F97–F99) is why ℤ₃ carries the area law; the A-vs-C Casimir caveat of F98–F101 applies unchanged. 3+1D SU(3) σ remains F94's Euclidean MC.
- **2D spatial, open boundaries.** The dual height solution of Gauss's law as implemented is 2D; 3D needs either a tree-gauge or constrained-basis construction (known technology, not built).
- **Hamiltonian vs Euclidean tension.** $\sigma$ here is energy per length from $V(R)$; F70/F101's $-\ln\langle\cdot\rangle$ is the Euclidean (per-area) tension. They are related through the time spacing, not equal; the contact point verified is the operator itself (C7 matrix identity), which is the correct invariant statement.

## 6. Check summary (7/7)

| Check | Statement | Tier | Residual |
|---|---|---|---|
| C1 | direct Gauss-sector KS spectrum == dual height spectrum (vacuum + charged) | machine | $\le1.9\times10^{-14}$ |
| C2 | $\lambda=0$: $V(R)=\frac{g^2}{2}R$ exact | 1 | $0.0$ |
| C3 | linear $V(R)$ at finite λ; increment Cauchy < 1%; σ monotone in λ | convergent | $3.8\times10^{-3}$ |
| C4 | $\sigma=\frac{g^2}{2}-\frac{\lambda^2}{6}+O(\lambda^3)$, $c_2$ from programmatic PT | asymptotic | Richardson $0.9992$ |
| C5 | real-time norm/energy conservation; Krylov vs dense | machine | $\le5\times10^{-13}$ |
| C6 | flux-tube localisation (GS) + persistence/melting (quench) | quantitative | fracs $0.61/0.31$; $0.36$, melt $-8.0$ |
| C7 | 1-plaquette dual U(1) == F101 rotor, $\chi=1/(4g^2)$; $\sigma_1(\lambda{=}1)=0.29551$ | 1 + machine | matrix $0.0$; table $3.6\times10^{-6}$ |

## 7. Provenance

- New content: the dual height construction with exact Gauss law and static-charge backgrounds (§2), the direct-vs-dual spectral identity (C1), the Hamiltonian string tension and PT cross-check (C3/C4), real-time flux-tube persistence/melting (C6), the F101 χ-map matrix identity (C7).
- Reused: F101 rotor convention and table value $\sigma_1(\lambda{=}1,\chi{=}1)=0.29551$; F99/F97 centre-group rationale; F70/F94 as the Euclidean complements.
- Verification: `tests/findings/test_F110_link_hamiltonian_realtime.py` (2026-06-06, 7/7 PASS), results `test-results/F110_link_hamiltonian_realtime.json`.
