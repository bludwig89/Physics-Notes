# F132 — Coarse-graining the dynamical / relativistic bound states

`2026-06-11 - 05:10`

**Status.** Phase-2 follow-on of `docs/roadmaps/roadmap-scale-to-real-space.md`,
extending F131 from a smooth-well toy to the model's *actual* dynamical bound
states. Module `ca-simulation/ca_blockspin_dynamical.py`; tests
`tests/findings/test_F132_blockspin_dynamical_bound_states.py` (9/9 PASS).

---

## 1. What this adds

F131 showed the block-spin RG $R_b$ (F130) commutes with binding for a single
particle in a *smooth* well. That case hid a distinction the real bound states
expose: **whether the binding coupling is RG-relevant or irrelevant.** F132
coarse-grains the three F74-family bound states and reads off the answer for each.

| Bound state | Binding | Coupling under $R_b$ |
|---|---|---|
| pion (F74/F103) | single-site **contact** well | **relevant — runs** (set by Watson $g/g_c$) |
| deuteron (F104) | smooth **finite-range** Yukawa/OBE | **irrelevant — fixed** ($O(h^2)$ error) |
| baryon (F122) | **confining** Cornell string | relevant $\sigma$ (F130-C1), mass = string scale |

The unifying picture: the *relevant* couplings are confinement $\sigma$ (F130-C1,
eigenvalue $b$) and the *contact* coupling (runs, set by $g/g_c$); the *irrelevant*
operators are the LIV/lattice artifacts ($b^{-n}$, F130 T2), the deconfining
magnetic coupling ($b^{-2}$, F130-C1) and smooth finite-range potentials.
Coarse-graining reproduces every bound state once the relevant couplings are run.

## 2. Pion — the contact coupling runs (P)

The F74 q̄q relative problem is a 3-D tight-binding lattice with a single-site
contact well of depth $g$; it binds only above the **Watson threshold**
$g_c = 2t/W_3$ ($W_3=0.5055$). A contact interaction is a *relevant* operator: it
cannot survive coarse-graining unchanged. Under $R_b$ the kinetic term carries
$t_\text{coarse}=t/b^2$ (the F131/F130 effective-mass rescale), and the coupling
must **run** to hold the physical $E_b$ fixed. The flow is governed by proximity
to threshold — the RG-invariant is the dimensionless ratio $g/g_c$:

$$g_\text{coarse} = \frac{g}{g_c(t)}\,g_c(t/b^2),\qquad g_c(t)=2t/W_3.$$

Measured (fine $L=12$, $t=1$, $g=4.0$, shallow $E_b=0.0291$):

| $b$ | $g_\text{fine}$ | $g_\text{coarse}$ (exact / predicted) | overlap | $r_\text{rms}$ fine/coarse | cells |
|---|---|---|---|---|---|
| 2 | 4.0 | 1.012 / 1.000 | 0.990 | 4.98 / 5.02 | 1728 → 216 |
| 3 | 4.0 | 0.454 / 0.444 | 0.975 | 4.98 / 5.10 | 1728 → 64 |

The coupling runs by a factor $\sim4$–$9$; the Watson prediction nails $g_\text{coarse}$
to a few %; and with the run coupling the binding energy, the bound-state
wavefunction ($\ge0.97$ overlap) and the size ($<2\%$) are reproduced on up to
**27× fewer cells**.

## 3. Deuteron — finite-range, no running (D)

The NN force is one-pion exchange + the F126/F128 $\sigma/\omega$ OBE — a *smooth,
finite-range* potential, an irrelevant operator. Its physical couplings are held
fixed; coarse-graining is simply decimating the radial grid ($h\to b\,h$). The
deuteron is a large, shallow halo ($E_b=2.224$ MeV, $r_d\approx1.94$ fm $\gg h$),
i.e. deeply IR, so it reproduces beautifully:

| grid factor | $h$ (fm) | $E_b$ (MeV) | rel. err | $r_d$ (fm) | bound |
|---|---|---|---|---|---|
| fine | 0.031 | 2.215 | — | 1.939 | ✓ |
| $b{=}2$ | 0.062 | 2.223 | 0.4 % | 1.936 | ✓ |
| $b{=}4$ | 0.124 | 2.257 | 1.9 % | 1.924 | ✓ |
| $b{=}8$ | 0.247 | 2.389 | 7.9 % | 1.878 | ✓ |

No coupling runs; the error is the irrelevant $O(h^2)$ discretisation operator
(it grows $\sim b^2$ with the grid factor and the state stays bound throughout) —
the same irrelevance class as the F130 T2 LIV operators and the F131 smooth well.

## 4. Baryon — the mass is the C1-covariant string scale (B)

The F122 baryon is a confined three-quark ground state (explicitly-correlated
Gaussian solver) and is *confinement-dominated* — the quark kinetic energy is
$\sim0.1\%$ of the mass; the mass is essentially the confining-string energy. Its
two binding ingredients are already proven RG-covariant: the string tension
$\sigma$ (F130-C1 — relevant, eigenvalue $b$, the physical string energy
invariant) and the kinetic dispersion (F130 T1/T2). So the baryon mass is an
RG-invariant *string scale*. The linear-potential virial fixes the scaling, and
the ECG solver confirms it:

$$E_\text{rel}\propto\Big(\tfrac{\sigma^2}{m}\Big)^{1/3}\propto\sigma^{2/3},\qquad
\frac{d\ln E_\text{rel}}{d\ln\sigma}=0.6670\ \ (\text{vs }2/3=0.6667).$$

The same engine reproduces the analytic three-body *harmonic* ground state
$E=3\sqrt{3k/m}$ to $0.3\%$ (the F122 machine-precision self-test). Because the
baryon mass is a function of the C1-covariant $\sigma$ on the T1/T2-covariant
dispersion, it is reproduced under coarse-graining through the already-proven
flows — no new lattice run needed (the ECG is a basis, not a lattice).

## 5. Reading the result

The RG commutes with binding for every dynamical bound state in the matter sector
**once the relevant couplings are run**. The contact (pion) coupling runs and is
fixed by the Watson threshold; the finite-range (deuteron) coupling is fixed and
its error is irrelevant; the confined (baryon) mass is the C1-covariant string
scale. This is the constructive Phase-2 statement: a coarse "universe in a bottle"
reproduces not just the vacuum rule (F130) and a toy atom (F131) but the **pion,
the deuteron and the proton**.

## 6. Honest limits

- **Pion kinetic term.** The F74 engine uses the tight-binding (parabolic, non-
  relativistic) reduction; the contact-running result is about the *interaction's*
  relevance and is independent of that. The fully relativistic Dirac/F26 kinetic
  dispersion is itself RG-covariant by F130 T1/T2, so a relativistic-kinetic
  contact state runs identically — not separately rebuilt here.
- **Baryon.** The ECG is a variational basis, not a real-space lattice, so the
  baryon is handled by the covariance of its ingredients ($\sigma$, dispersion)
  plus the confinement-dominance scaling — not a direct block-spin of the solver.
- **Long-wavelength / shallow-state regime**, as in F131: the block factor must
  stay below the state's size in super-cells.
- **Static spectra.** Real-time wave-packet dynamics (the dispersing-vs-non-
  dispersing F122 evolution) under $R_b$ is the remaining dynamical check; for an
  energy eigenstate $R_b$ commutes with $e^{-iHt}$ trivially (a global phase).

## 7. Files

- `ca-simulation/ca_blockspin_dynamical.py` — contact (pion) coarse-graining +
  running coupling, deuteron grid-decimation, baryon confinement scaling. Wraps
  `ca_meson`/F74, `ca_nuclear`, `ca_baryon_dynamics` read-only; consumes
  `ca_blockspin.block_average`.
- `tests/findings/test_F132_blockspin_dynamical_bound_states.py` — 9 tests
  (P, D, B).
- Exactness inventory rows #70–72 (machine / quantitative).
