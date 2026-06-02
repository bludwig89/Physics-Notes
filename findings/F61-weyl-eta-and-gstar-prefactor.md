# F61 — The Weyl heat-kernel coefficient $\eta=1/12$ and the mode count $g_*$: turning $P_\text{pre}$ into a number

**Date:** 2026-05-30 - 15:55
**Status:** Confirmed for the fermionic sector — $\eta_\text{Weyl}=1/12$ derived exactly (Seeley–DeWitt + statistics, rational arithmetic); $g_*$ fixed from the model's first-generation content; $P_\text{pre}$ and $(a,\tau)$ produced as numbers. Gauge-boson contributions to $g_*$ are a flagged, separate additive piece (not yet included). 3/3 checks PASS.
**Module:** new `ca-simulation/forks/gr_fork_F61_weyl_eta_gstar.py` (self-contained; exact rationals + a real-arithmetic lattice check).
**Tests:** `model-tests/test_F61_weyl_eta_gstar.py`; results `test-results/F61_weyl_eta_gstar.json`.

## The question

F59 left $P_\text{pre}=\sqrt{2\pi\,\eta\,g_*}$ with $\eta=1/12$ (used as "the minimal-scalar value") and $g_*=2$ (assumed). F61 derives the per-Weyl heat-kernel coefficient $\eta$ properly and counts $g_*$ from the actual field content.

## Part A — $\eta_\text{Weyl}=1/12$ from the Seeley–DeWitt $a_1$ coefficient

The F59 convention is $\frac{1}{16\pi G}\big|_\text{per dof}=\eta\int\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}$. The flat-space integral $\int_{|k|<\Lambda}\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}=\frac{\Lambda^2}{8\pi^2}$ (with $c=1$) is **spin-independent** — it is the same vacuum-mode integral for a scalar or for each Weyl component, because the BCC Weyl $2\times2$ unitary $U(k)$ has eigenphases $\pm\omega$ of **equal magnitude**, so each spinor component contributes the same $1/(2\omega)$ as a scalar with that dispersion. (Lattice check: $\big|\,|\arg\lambda_1|-|\arg\lambda_2|\,\big|$ over a 4000-point BZ sample $=4.4\times10^{-16}$, machine precision.) So all spin dependence sits in the heat-kernel coefficient, via $\eta_\text{dof}=c_\text{dof}/2$, where $c=a_1/R$ (statistics-signed) is normalised so a minimal real scalar has $c_0=1/6$.

For a Laplace-type operator $-\Box+E$ on a bundle, $a_1=\tfrac16 R\,\mathrm{tr}\,\mathbb1-\mathrm{tr}\,E$:

| field | operator / $E$ | $a_1/R$ | $c$ (stat-signed) | $\eta=c/2$ |
|---|---|---|---|---|
| minimal real scalar | $E=0$, $\mathrm{tr}\,\mathbb1=1$ | $+\tfrac16$ | $+\tfrac16$ | $\tfrac1{12}$ |
| Dirac fermion | Lichnerowicz $\slashed D^2=-\Box+\tfrac R4$, $\mathrm{tr}\,\mathbb1_4=4$, fermion sign $-1$ | $-\tfrac13$ | $+\tfrac13$ | $\tfrac16$ |
| **2-component Weyl** | half a Dirac | $-\tfrac16$ | $+\tfrac16$ | $\boxed{\tfrac1{12}}$ |

So $\eta_\text{Weyl}=\tfrac1{12}$ exactly — **F59's placeholder was the correct per-Weyl value, not an approximation.** (Both scalar and Weyl give $c=1/6$; the Weyl $a_1/R=-1/6$ is flipped positive by the fermionic determinant sign.) The Weyl contribution to $1/G$ is positive — gravity attractive — as required.

## Part B — $g_*$, the gravitating Weyl count

Everything that propagates and carries energy–momentum sources the induced term. Counting 2-component Weyl fields in the model's first generation (`first-gen-completeness.md` Table 1, Higgs-free SU(2)):

$$L=(\nu,e)_L:2,\quad e_R:1,\quad Q=(u,d)_L:2\times3=6,\quad u_R:3,\quad d_R:3\ \Rightarrow\ g_*=15,$$

plus the sterile $\nu_R$ the model carries (F47 see-saw) $\Rightarrow g_*=16$ per generation; $g_*=48$ for three generations.

## Part C — the number

With $\eta=\tfrac1{12}$ per Weyl, $P_\text{pre}=\sqrt{2\pi\sum_i\eta_i}=\sqrt{2\pi\cdot\tfrac1{12}g_*}=\sqrt{\pi g_*/6}$:

| $g_*$ | $P_\text{pre}$ | $a/\ell_P$ ($d{=}3$) | $\tau/t_P$ | $\sqrt{a\,c\tau}/\ell_P$ |
|---|---|---|---|---|
| 2 (minimal) | $1.023$ | $1.347$ | $0.778$ | $1.023$ |
| 15 (charged + active $\nu$) | $2.802$ | $3.688$ | $2.129$ | $2.802$ |
| **16 (one gen, incl $\nu_R$)** | $\mathbf{2.894}$ | $\mathbf{3.809}$ | $\mathbf{2.199}$ | $\mathbf{2.894}$ |
| 48 (three gen) | $5.013$ | $6.598$ | $3.809$ | $5.013$ |

So for the model's one full generation the lattice cell is $a\approx3.8\,\ell_P$ and the tick $\tau\approx2.2\,t_P$, with the $d$-independent invariant $\sqrt{a\,c\tau}\approx2.9\,\ell_P$. The clean "$a\approx\ell_P$" of the minimal $g_*=2$ case in F59 was a coincidence of minimal content and does **not** survive realistic field content: the cell is several Planck lengths, the tick a couple Planck times. The $d^{1/4}$ split (F59/F60) is unchanged; only the overall scale $P_\text{pre}$ is now pinned (for the fermionic sector).

## What is derived vs what remains

- **Derived exactly:** $\eta_\text{Weyl}=1/12$ (Seeley–DeWitt $a_1$ + Lichnerowicz + fermionic statistics, rational); the spin-independence of the flat phase-space integral (lattice ratio $1.000000$).
- **Fixed from content:** $g_*=16$ per generation (15 charged + active $\nu$, $+1$ sterile $\nu_R$).
- **Not yet included:** the **gauge sector** (photon, $W$, $Z$, 8 gluons) also gravitates, with spin-1 heat-kernel coefficients (a different $c_1$, and with ghosts) — an additive contribution to $g_*\eta$ not computed here. Because $P_\text{pre}\propto\sqrt{\sum\eta}$, it is a mild ($\sqrt{\cdot}$) correction, but it will raise $P_\text{pre}$ and hence $a/\ell_P$.
- **Still assumed (from F59):** the $B=I_\text{lat}/a^2$ convention ("the cell is the only length") and the loop-channel selection (F60). The induced-$G$ absolute prefactor is now scheme-fixed on the lattice (compact BZ, no regulator freedom — F57), so the residual uncertainty is the field count, not a renormalization scheme.

## Caveats

- $\eta_\text{Weyl}$ uses the standard continuum Lichnerowicz $E=R/4$ curvature coupling; the flat lattice cannot see that $R$-term directly, so Part A's lattice check only verifies the spin-independence of the *phase-space* factor, not the $R/4$ coefficient (which is imported from the heat kernel). Deriving $E$ from the F46/F50 rest-leg curved-background dispersion is the way to make even that lattice-native — a follow-up.
- $g_*$ counts fermionic polarizations; the gauge and (absent) scalar sectors are separate.

## Relation to other findings

Completes the F59 prefactor ($\eta$, $g_*$ were its open inputs) and is unaffected by the F60 channel choice (which fixed the $c_\text{lat}$-power, not the count). Uses the first-generation content of `first-gen-completeness.md` (F40–F49) and the $\nu_R$ of **F47**. Confirms the F59/F60 $d^{1/4}$ selection with a now-quantitative scale: $a\approx3.8\,\ell_P$, $\tau\approx2.2\,t_P$ for one generation.
