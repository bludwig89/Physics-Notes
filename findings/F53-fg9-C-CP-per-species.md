# F53 — FG-9: antiparticle / per-species C and CP

**Date:** 2026-05-29 - 21:10
**Status:** Confirmed — 6/6 parts PASS (P1–P4 exact / bit-for-bit, P5–P6 at machine ε)
**Verification script:** `model-tests/test_FG9_C_CP_per_species.py`
**Results:** `test-results/FG9_C_CP_per_species.json`
**Builds on:** `test_13_QFT8_CPT.py` (CPT mass equality), F27 (chiral SU(2), θ pure gauge), F34/FG-3 (right-handed decoupling), F48/F35 (per-species Z couplings), F38/FG-1 (anomaly cancellation)
**Closes:** first-gen-completeness §3 item 7 and §5.1 row FG-9 — the last open Tier-A structural item

---

## 1. Result

The discrete-symmetry content of the first generation is now verified species by species, putting the antiparticle sector on the same footing as the particle sector. The existing CPT test (`test_13`) proved only the mass equality $\omega_0(+m)=\omega_0(-m)$; FG-9 adds explicit $C$, $P$, and $CP$ on every first-generation Weyl species.

The headline statement is the standard chiral-gauge-theory pattern, realised exactly on the lattice:

$$\boxed{\;C \text{ maximal},\quad P \text{ maximal},\quad CP \text{ exact (single generation)}\;}$$

Charge conjugation $C$ maps each species to its antiparticle, negating every additive charge and flipping chirality, $C:(T_3,Q,Y,\chi)\to(-T_3,-Q,-Y,-\chi)$. Because the model's charged current couples to the **left** sector alone (F27/F34/FG-3 — the right-handed $\chi$ is decoupled bit-for-bit), the $C$-image of a left-handed particle is a right-handed antiparticle that does not couple, so $C$ is **maximally** violated; parity $P$ (chirality swap alone) is likewise maximal. The combination $CP$ — which maps a left particle to a left antiparticle — is preserved. With a single generation the CKM matrix is $1\times1$ and carries no physical phase, $N_{\rm phase}=(n-1)(n-2)/2=0$, so there is no CP-violating parameter at all; the only candidate, the F27 complex-mass phase $\theta(x)$, is pure gauge and drops out of the spectrum.

---

## 2. The six parts

| Part | Statement | Tier | Residual |
|---|---|---|---|
| **P1** | $C$ antiparticle table: $(T_3,Q,Y)\to(-T_3,-Q,-Y)$, chirality flips, and Gell-Mann–Nishijima $Q=T_3+Y/2$ holds for **both** particle and antiparticle, all 8 species | 1 (exact rational) | exactly 0 |
| **P2** | $C$ maximally violated by the charged current: the $C$-image (right sector) of each left doublet sources zero isospin current ⇒ $A_C=1$ | 1 (bit-for-bit) | $\|J\|_{\rm right}=0.0$ |
| **P3** | $P$ maximally violated: doublet $g_L=1$, singlet $g_R=0$ ⇒ $A_P=(g_L-g_R)/(g_L+g_R)=1$ for $\nu_L,e_L,u_L,d_L$ | 1 (exact rational) | exactly 1 |
| **P4** | $CP$ conserved: (a) $\lvert g_{\rm cc}(f_L)\rvert=\lvert g_{\rm cc}(\bar f_L)\rvert$; (b) NC relation $g_R^{\bar f}=-g_L^f\Rightarrow\lvert g_L^f\rvert=\lvert g_R^{\bar f}\rvert$ for all 7 chiralities; (c) single-generation Jarlskog $J=0$ exactly | 1 (exact) | $\le$ 0 |
| **P5** | CP-phase $\theta$ pure gauge: (a) one-tick eigenphase spectrum θ-independent over $\theta\in\{0,\pi/3,\pi/2,2,\pi\}$ and 4 momenta per species; (b) bit-for-bit chiral gauge removal $\theta\text{-step}\equiv(\theta{=}0)\text{-step}$ | 2 (machine ε) | $3.3\times10^{-16}$ (a); $9.0\times10^{-16}$ (b) |
| **P6** | CPT per species: $\omega(+m)=\omega(-m)$ (algebraic + numerical, 300 ticks) and $\lVert C\psi\rVert^2=\lVert\psi\rVert^2$ | 1/2 | $0.0$ (numerical & norm) |

Representative (uncalibrated, Tier-A) masses $m_e=0.20,\ m_u=0.15,\ m_d=0.18$ were used for the numerical parts; the symmetry statements are independent of the values.

---

## 3. Why P5 is spectral, not propagation-based

The first draft measured $\omega(\theta)$ by propagating a packet, and it reported a spurious $\sim\!10^0$ θ-dependence. That is a **measurement artefact**: feeding the $\theta=0$ eigenvector into the $\theta$-rotated stepper projects onto a mix of the $\pm\omega$ branches, so the overlap phase is not a single frequency. The physically correct statement is that the **spectrum** of the one-tick operator is θ-independent, which is what F27 T3 established. The θ-phases cancel in the product of the off-diagonal mass blocks,

$$\bigl(i\,m\,e^{+i\theta}\bigr)\bigl(i\,m\,e^{-i\theta}\bigr)=-m^2,$$

θ-free (verified symbolically). Equivalently, a chiral rephasing $\chi\to e^{+i\theta}\chi$ maps the $\theta$ mass-step onto the $\theta=0$ mass-step bit-for-bit (P5b, $9\times10^{-16}$). Both routes show $\theta$ is unphysical, so the lone candidate CP-odd parameter in one generation does not produce CP violation.

---

## 4. Consistency with the rest of the model

- The antiparticle charge table is the exact negation of the F38/FG-1 anomaly-cancellation content, so $\sum\bar Y=-\sum Y=0$ and the antiparticle generation cancels its anomalies whenever the particle generation does (P1).
- $A_C=A_P=1$ is the same left-only coupling that F27/F34/FG-3 established as the right-handed $\chi$ decoupling; FG-9 reads it as the maximal $C$/$P$ violation it physically is.
- The NC CP relation in P4(b) uses the F48/F35 per-species table $(g_L^f,g_R^f)=(T_3^f-Q^f s_W^2,\,-Q^f s_W^2)$ at the F45 bare angle $\sin^2\theta_W=1/4$; note $g_L^{e_L}=-1/2-(-1)(1/4)=-1/4$ (and the F48 Z11 vanishing is of $g_V$, not $g_L$).
- P6 reproduces `test_13_QFT8_CPT` per species at $0.0$ numerical residual, so FG-9 supersets the old CPT regression.

---

## 5. Limitations / scope

This is a **Tier-A structural** closure: it certifies the discrete-symmetry *structure* of one generation with symbolic charges. It does **not** address (and does not claim) any of the following, which remain Tier B / multi-generation:

1. **Observed CP violation** ($\epsilon_K$, $\sin2\beta$, the Jarlskog $J\approx3\times10^{-5}$) requires **three** generations — out of scope for a single-generation model by construction. FG-9's $J=0$ is the *correct* one-generation answer, not a deficiency.
2. **Strong CP** ($\bar\theta$ of QCD) is a separate phase in the gluon sector (F43), untouched here.
3. **Absolute masses/couplings** are uncalibrated (Tier B, blocked on CO-1 SI units).

---

## 6. New exactness-inventory entries

- **Tier 1 (algebraic exact):** antiparticle GMN closure (P1); $A_C=1$ maximal $C$ violation (P2); $A_P=1$ maximal $P$ violation (P3); NC CP magnitude relation $\lvert g_L^f\rvert=\lvert g_R^{\bar f}\rvert$ (P4b); single-generation Jarlskog $J=0$ (P4c); CPT $\omega(+m)=\omega(-m)$ algebraic (P6).
- **Tier 2 (machine precision):** one-tick eigenphase θ-independence $3.3\times10^{-16}$ (P5a); bit-for-bit chiral gauge removal $9\times10^{-16}$ (P5b); $\lVert C\psi\rVert^2$ conservation and per-species numerical $\omega(+m)=\omega(-m)$ at $0.0$ (P6).
