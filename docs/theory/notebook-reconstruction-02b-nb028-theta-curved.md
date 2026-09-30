# Notebook Reconstruction — NB-028: the Curved-Spacetime Energy–Momentum Tensor $\Theta^{\mu\nu}$

Date-time stamp: 2026-09-22 - 16:40

Full reconstruction of the covariant matter stress tensor that the notebook sets up at p.21
(NB-028, `references/physics-notes-complete.md` lines 476–483), using the pages it draws on:
p.15 (Sachs' $\Omega_\mu$, eq. 3.88), p.16 (the $q^\mu,\tilde q^\mu$ tetrad and the boxed
covariant matter Lagrangian), p.17 (covariant derivatives, $\Omega^{(\chi)}$ eqs. 3.77/3.79b),
p.18 ($G_{\mu\nu}=8\pi T_{\mu\nu}$), p.20 (NB-025/026: symmetrized $\mathcal L_M$ and the flat
$\Theta^{\mu\nu}$), p.21 (NB-027/028), and pp.24–25 (NB-033/034: the variations and the
field equation). Companion to batch 02 (`notebook-reconstruction-02-weyl-and-sachs-lagrangian.md`).

Verification script: `tests/runners/notebook-recon/run_NB-026_027_028_theta_curved.py`
(sympy, exact) → `test-results/notebook-recon/NB-026_027_028_theta_curved.json`.

---

## 1. What the notebook wrote

p.20 (NB-026), from $\mathcal L_M=\tfrac i2(\eta^+q^\mu\partial_\mu\eta-\partial_\mu\eta^+q^\mu\eta)+(\chi,\tilde q)$:

$$\Theta^{\mu\nu}=\tfrac i2\big(\eta^+q^\mu\partial^\nu\eta\;{\color{red}+}\;(\partial^\nu\eta^+)q^\mu\eta
+\chi^+\tilde q^\mu\partial^\nu\chi\;{\color{red}+}\;(\partial^\nu\chi^+)\tilde q^\mu\chi\big)$$

p.21 (NB-027): $\mathcal H_M=\Theta^{00}$ with the same signs; the author flags that it "doesn't
show any interaction of $\eta$ & $\chi$ with curvature." p.21 (NB-028) — the fix:

$$\Theta^{\mu\nu}=\eta^{+;\nu}\frac{\partial\mathcal L}{\partial\eta^+_{;\mu}}+\frac{\partial\mathcal L}{\partial\eta_{;\mu}}\eta^{;\nu}
+\chi^{+;\nu}\frac{\partial\mathcal L}{\partial\chi^+_{;\mu}}+\frac{\partial\mathcal L}{\partial\chi_{;\mu}}\chi^{;\nu}-g^{\mu\nu}\mathcal L$$

$$\mathcal L_M=\tfrac i2(\eta^+q^\mu\eta_{;\mu}-\eta^+_{;\mu}q^\mu\eta)+\tfrac i2(\chi^+\tilde q^\mu\chi_{;\mu}-\chi^+_{;\mu}\tilde q^\mu\chi)$$

$$\Theta^{00}=\tfrac i2\big(\eta^+q^0\eta_{;0}\;{\color{red}+}\;\eta^+_{;0}q^0\eta+\chi^+\tilde q^0\chi_{;0}\;{\color{red}+}\;\chi^+_{;0}\tilde q^0\chi\big)$$

The general definition (line 1 of NB-028) is right. The evaluated $\Theta^{00}$ carries a sign
error inherited from p.20 (red), and the tensor is left in canonical (non-symmetric) form. Both are
repaired below.

## 2. Ingredients and conventions

- Signature $(+,-,-,-)$; units of p.18 ($G=c=1$, $G_{\mu\nu}=8\pi T_{\mu\nu}$).
- Tetrad: $q^\mu$ Hermitian ($q^{\mu+}=q^\mu$, assumed on p.16/p.20), flat limit $q^\mu\to\sigma^\mu=(I,\boldsymbol\sigma)$;
  $\tilde q^\mu\to\tilde\sigma^\mu=(I,-\boldsymbol\sigma)$. With this sign of $\tilde q$,
  $$\tfrac12\big(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu\big)=g^{\mu\nu}I .$$
  (Sachs' $\tilde q$ carries the opposite overall sign — p.16's $-\sigma_0q^\mu_4$ — which is where
  the $-\tfrac12$ of his (3.59′) comes from. Nothing below depends on that choice beyond this sign.)
- Covariant derivatives (p.17): $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$, $\chi_{;\mu}=\partial_\mu\chi+\Omega^{(\chi)}_\mu\chi$,
  and by conjugation $\eta^+_{;\mu}=\partial_\mu\eta^++\eta^+\Omega_\mu^+$. Indices raised with $g$: $\eta^{;\nu}=g^{\nu\lambda}\eta_{;\lambda}$.
- **Tetrad postulate.** For $\eta^+q^\mu\eta$ to differentiate as a vector (Leibniz rule), the
  covariant derivative of $q^\mu$ has to be
  $$q^\mu{}_{;\rho}=\partial_\rho q^\mu+\Gamma^\mu_{\rho\lambda}q^\lambda-\Omega_\rho^+q^\mu-q^\mu\Omega_\rho=0,$$
  and likewise for $\tilde q^\mu$ with $\Omega^{(\chi)}$. This is the "$q^\mu_{;\mu}=0$" that NB-034 cites from
  notebook 2; it fixes $\Omega$ up to a trace $iA_\mu I$ — the U(1) potential in Sachs' unification.
  The traceless part is (corrected 2026-09-22 - 17:25, see §7.4 — the transcribed p.15 (3.88) and
  p.17 (3.77) have the factors in the reverse order, which only matters when the tetrad rotates):
  $$\Omega_\rho=\tfrac14\tilde q_\mu(\partial_\rho q^\mu+\Gamma^\mu_{\tau\rho}q^\tau),\qquad
  \Omega^{(\chi)}_\rho=-\tfrac14(\partial_\rho q^\mu+\Gamma^\mu_{\tau\rho}q^\tau)\tilde q_\mu
  =\tfrac14 q_\mu(\partial_\rho\tilde q^\mu+\Gamma^\mu_{\tau\rho}\tilde q^\tau)\ \text{(= p.17's 3.79b as written)}.$$
- Consequence (verified, B3): $\nabla_\mu(\eta^+q^\mu\eta)=\eta^+_{;\mu}q^\mu\eta+\eta^+q^\mu\eta_{;\mu}$ for any $\eta$.
- $\mathcal L_M$ is a scalar; the action is $S_M=\int\sqrt{-g}\,\mathcal L_M\,d^4x$ (p.16's boxed form carries the $\sqrt{-g}$).
  p.16 writes the kinetic term with $i$ rather than $\tfrac i2$; p.20's $\tfrac i2$ is the correctly
  normalized one (it gives energy $\omega$ per quantum, A4/B5), and is used here.

## 3. Reconstruction

**Step 1 — the canonical momenta.** $\mathcal L_M$ is linear in the covariant derivatives, so

$$\frac{\partial\mathcal L_M}{\partial\eta_{;\mu}}=\tfrac i2\,\eta^+q^\mu,\qquad
\frac{\partial\mathcal L_M}{\partial\eta^+_{;\mu}}=-\tfrac i2\,q^\mu\eta,$$

and the same with $(\chi,\tilde q)$. The minus sign on the second is the whole issue: it comes from
the antisymmetrized form the author himself adopted at p.20 to escape NB-025's $\mathcal H\equiv0$.

**Step 2 — NB-028's canonical tensor, evaluated correctly.** Substituting into NB-028's definition:

$$\Theta^{\mu\nu}=\tfrac i2\big(\eta^+q^\mu\eta^{;\nu}-\eta^{+;\nu}q^\mu\eta\big)
+\tfrac i2\big(\chi^+\tilde q^\mu\chi^{;\nu}-\chi^{+;\nu}\tilde q^\mu\chi\big)-g^{\mu\nu}\mathcal L_M .$$

The last term vanishes on shell: the field equations $q^\mu\eta_{;\mu}=0$, $\eta^+_{;\mu}q^\mu=0$
(NB-034) kill each half of $\mathcal L_M$ separately (A2, B5). With the notebook's "+" sign the
bracket becomes $\tfrac i2\nabla^\nu(\eta^+q^\mu\eta)$ — an imaginary total derivative, not an energy.

**Step 3 — symmetrize: the tensor that sources gravity.** $G_{\mu\nu}$ is symmetric; the
canonical $\Theta^{\mu\nu}$ is not. Its antisymmetric part is the spin density coupled to the
connection (in the FRW test, B5: $\Theta^{[12]}=a'/2a^7$ for a spinor moving along $z$ — the
helicity spin, sitting in the $xy$ plane, times the expansion rate). The source of the Einstein
equation is the metric (Hilbert) tensor, $T_{\mu\nu}=\frac{2}{\sqrt{-g}}\frac{\delta S_M}{\delta g^{\mu\nu}}$,
which for spinors means varying $S_M$ with respect to the tetrad $q^\mu$ — the variation the
notebook is preparing at NB-032 ($\partial\sqrt{-g}/\partial\tilde q^\lambda$). That variation gives
the Tetrode tensor — the symmetric part of Step 2 (Tetrode 1928; Birrell & Davies §3.8). The
tetrad variation is carried out in the notebook's $q^\mu$ language in §7.

## 4. Result

$$\boxed{\;T^{\mu\nu}=\frac i4\Big(\eta^+q^\mu\eta^{;\nu}+\eta^+q^\nu\eta^{;\mu}-\eta^{+;\nu}q^\mu\eta-\eta^{+;\mu}q^\nu\eta\Big)
+\frac i4\Big(\chi^+\tilde q^\mu\chi^{;\nu}+\chi^+\tilde q^\nu\chi^{;\mu}-\chi^{+;\nu}\tilde q^\mu\chi-\chi^{+;\mu}\tilde q^\nu\chi\Big)
-g^{\mu\nu}\mathcal L_M\;}$$

with $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$, $\chi_{;\mu}=\partial_\mu\chi+\Omega^{(\chi)}_\mu\chi$,
$\Omega,\Omega^{(\chi)}$ from §2 (ordering per §7.4), and $\mathcal L_M=0$ on shell. It enters

$$\boxed{\;R_{\mu\nu}-\tfrac12g_{\mu\nu}R=8\pi\,T_{\mu\nu}\;},\qquad \nabla_\mu T^{\mu\nu}=0\ \text{(on shell)}.$$

The energy density (the corrected NB-027/028 $\Theta^{00}$) is

$$T^{00}=\tfrac i2\big(\eta^+q^0\eta^{;0}-\eta^{+;0}q^0\eta\big)+\tfrac i2\big(\chi^+\tilde q^0\chi^{;0}-\chi^{+;0}\tilde q^0\chi\big),$$

and what an observer with 4-velocity $u^\mu$ measures is $\rho=T_{\mu\nu}u^\mu u^\nu$. In flat space
this reduces exactly to the Legendre Hamiltonian density $\pi_\eta\dot\eta+\dot\eta^+\pi_{\eta^+}-\mathcal L_M$
(A3) — the thing NB-025 was after — and the curvature coupling the author found missing at NB-027
lives in $\Omega_\mu$ and in the $g^{\mu\nu}$ inside $\eta^{;\nu}$. Adding the p.17 mass coupling
between $\eta$ and $\chi$ changes nothing here: a non-derivative term only enters through
$-g^{\mu\nu}\mathcal L_M$, which still vanishes on shell (standard; not separately run).

## 5. Verification (all exact, sympy)

| Check | Setting | Result |
|---|---|---|
| A1 canonical Θ from p.20's own $\mathcal L_M$ | flat, generic η | = corrected form (minus sign); notebook "+" form differs by $i\,\eta\,\partial^\nu\eta^*$ |
| A2 $\mathcal L_M$ on shell | flat | 0 |
| A3 Legendre $\mathcal H$ vs corrected $\Theta^{00}$ | flat | identical; notebook $\Theta^{00}=\tfrac i2\partial_0(\eta^+\eta)$ |
| A4 plane wave, $\omega=k$ | flat | corrected $\Theta^{00}=k$; notebook form $=0$ |
| B1 $\tfrac12\{q^\mu,\tilde q^\nu\}=g^{\mu\nu}$ | FRW, $g=a^2(\tau)\eta$ | holds |
| B2 Ω solved from the tetrad postulate | FRW | $\Omega_i=\tfrac{a'}{2a}\sigma_i$, $\Omega^{(\chi)}_i=-\tfrac{a'}{2a}\sigma_i$, $\Omega_0=0$; matches (3.88) for η and (3.77)=(3.79b) for χ — **in FRW only** (no frame rotation); for a general tetrad only (3.79b) survives, §7.4 |
| B3 Leibniz identity | FRW, arbitrary η, χ | residual 0 |
| B4 $q^\mu\eta_{;\mu}=0$ by $\eta=a^{-3/2}u\,e^{-ik(\tau-z)}$ | FRW | residual 0 (both sectors) |
| B5 corrected tensor | FRW, on shell | real; $\mathcal L_M=0$; $\Theta^{[12]}=\pm a'/2a^7\neq0$; $T$: $\nabla_\mu T^{\mu\nu}=0$, $T^\mu{}_\mu=0$, $\rho=k/a^4$ (radiation scaling) — null dust $T^{00}=T^{03}=T^{33}=k/a^6$ |
| B7 notebook's written NB-028 $\Theta^{00}$ | FRW, on shell | $-\tfrac{3i}{2}a'/a^7$: purely imaginary, independent of $k$ |

B2 was a first check of the Sachs formulas batch 02 marked NOT-TESTABLE (NB-020). It passed in FRW,
but FRW has no frame rotation. The general-tetrad test in §7.4 shows (3.79b) is right as written,
while (3.77) and both forms of (3.88) are the Hermitian conjugates of what the notebook's
convention requires.

## 6. Verdicts and what stays open

- **NB-026 — INCORRECT (as transcribed) / SOLID-WITH-CORRECTION.** Sign of the $\partial^\nu\eta^+$ and $\partial^\nu\chi^+$ terms. The dropped $-g^{\mu\nu}\mathcal L$ is legitimate on shell.
- **NB-027 — INCORRECT (as transcribed) / SOLID-WITH-CORRECTION.** As written $\Theta^{00}=\tfrac i2\partial_0(\eta^+q^0\eta)$: imaginary, a total derivative, zero for a plane wave. The self-critique (no curvature coupling) is correct and is exactly what NB-028 fixes.
- **NB-028 — SOLID-WITH-CORRECTION.** The covariant definition is right; the evaluated $\Theta^{00}$ inherits the sign; the canonical tensor must be symmetrized (Tetrode) before it can source $G_{\mu\nu}$.
- These supersede batch 02's "SOLID" for NB-026/027/028, which were assessed structurally and never evaluated.
- ~~**Open:** the tetrad-variation derivation of the Tetrode form in the notebook's own $q^\mu$ language (continuing NB-032) is cited, not redone.~~ **Done 2026-09-22 - 17:25, §7.** The antisymmetric spin part dropped in Step 3 is what couples to torsion in Einstein–Cartan–Sciama–Kibble — the same place NB-037's disagreement with Sachs sits (NEEDS-WORK, ECSK-grounded), so closing one likely closes the other.
- Model relevance: this $T^{\mu\nu}$ is the massless-fermion piece of the full stress-energy source that key decision 4 (F178) makes the canonical gravity law. It is standard physics recovered, not a new claim, so it carries no claim card.


---

## 7. Tetrad-variation derivation in the notebook's $q^\mu$ language (continuing NB-032)

Date-time stamp: 2026-09-22 - 17:25

Verification script: `tests/runners/notebook-recon/run_NB-032_tetrad_variation_tetrode.py`
(sympy, exact; `flat` and `frw` modes) →
`test-results/notebook-recon/NB-032_tetrad_variation_tetrode_{flat,frw}.json`.

NB-032 (p.23) sets up the program: treat $q^\mu,\tilde q^\mu,\Omega_\mu,\Omega^{(\chi)}_\mu$ as the
independent fields, differentiate with the matrix rule $\partial\,\mathrm{Tr}(AB)/\partial B=\tilde A$
(transpose), and starts with $\partial(-g)^{1/2}/\partial\tilde q^\lambda$. This section finishes
the step that turns that program into the gravitational source: the variation of $S_M$ with
respect to $q^\mu$.

### 7.1 Dictionary and the defining formula

$q^\mu=e^\mu{}_a\sigma^a$, $\tilde q^\mu=e^\mu{}_a\tilde\sigma^a$, and so $e^\mu{}_a=\tfrac12\mathrm{Tr}(q^\mu\tilde\sigma_a)$ (from
$\mathrm{Tr}(\sigma^a\tilde\sigma^b)=2\eta^{ab}$). The lowered tetrad is $q_\lambda=g_{\lambda\nu}q^\nu=e_{\lambda a}\sigma^a$. Both $q^\mu$ and
$\tilde q^\mu$ are built from the one real tetrad $e^\mu{}_a$, so "vary $q^\mu$ and $\tilde q^\mu$" means
varying $e^\mu{}_a$.

From $T_{\mu\nu}=\frac2{\sqrt{-g}}\frac{\delta S_M}{\delta g^{\mu\nu}}$ and $g^{\mu\nu}=\eta^{ab}e^\mu{}_ae^\nu{}_b$:

$$\sqrt{-g}\,T_{\lambda\nu}=e_{\lambda a}\frac{\delta S_M}{\delta e^\nu{}_a}.$$

In the notebook's matrix calculus, $\delta S/\delta e^\nu{}_a=\mathrm{Tr}\big[(\delta S/\delta q^\nu)^T\sigma^a\big]$, and
$e_{\lambda a}\sigma^a=q_\lambda$. So in $q$-language:

$$\boxed{\;\sqrt{-g}\,T_{\lambda\nu}=\mathrm{Tr}\!\Big[\Big(\frac{\delta S_M}{\delta q^\nu}\Big)^{T}q_\lambda\Big]\quad(\text{plus the same with }\tilde q^\nu,\tilde q_\lambda\text{ for the }\chi\text{ sector})\;}$$

Off shell this can have an antisymmetric part. That part is the local-Lorentz Ward identity, and
it vanishes on shell (§7.3c).

### 7.2 The $\sqrt{-g}$ derivative (NB-032's line)

$\delta\sqrt{-g}=-\tfrac12\sqrt{-g}\,g_{\mu\nu}\delta g^{\mu\nu}=-\sqrt{-g}\,e_{\mu a}\delta e^{\mu a}$, i.e.
$$\delta\sqrt{-g}=-\tfrac12\sqrt{-g}\,\mathrm{Tr}(\tilde q_\mu\,\delta q^\mu),\qquad
\frac{\partial\sqrt{-g}}{\partial\tilde q^\lambda}=-\tfrac12\sqrt{-g}\;q_\lambda^{\,T}\ \ (\text{all dependence put in }\tilde q).$$
Verified (V1): $\partial\sqrt{-g}/\partial e^\mu{}_a=-\sqrt{-g}\,e_\mu{}^a$ at a generic numerical tetrad.

Compare the notebook's $\big(\tfrac14q_\lambda(-g)^{-1/2}\big)^*$:
- $^*$ equals $^T$ for Hermitian $q$ — fine.
- $\tfrac14$ in place of $\tfrac12$ is right if $\sqrt{-g}$ is read as depending symmetrically on $q^\mu$ and $\tilde q^\mu$ (each carries half).
- The overall sign flips with Sachs' opposite-sign $\tilde q$ — fine.
- **The power is wrong.** Rescale $e^\mu{}_a\to s\,e^\mu{}_a$. Then $\partial\sqrt{-g}/\partial\tilde q$ scales as $s^{-5}$ and $\sqrt{-g}\,q_\lambda$ also scales as $s^{-5}$, but $(-g)^{-1/2}q_\lambda$ scales as $s^{+3}$.

Corrected: $\partial(-g)^{1/2}/\partial\tilde q^\lambda=\big(\tfrac14q_\lambda(-g)^{+1/2}\big)^*$ (Sachs sign, symmetric split). The
likely slip: $\partial(-g)/\partial\tilde q$ carries a factor $(-g)$, which was dropped before dividing by $2(-g)^{1/2}$.

### 7.3 The variation

$S_M=\int\sqrt{-g}\,\tfrac i2\big[\eta^+q^\mu(\partial_\mu+\Omega_\mu)\eta-(\partial_\mu\eta^++\eta^+\Omega_\mu^+)q^\mu\eta\big]d^4x+(\chi,\tilde q,\Omega^{(\chi)})$
depends on the tetrad in three places: (a) the explicit $q^\mu$, (b) $\sqrt{-g}$, and (c) $\Omega_\mu[q]$.

**(a)+(b) — $\Omega$ held fixed (the notebook's "independent $\Omega$" program).**
$$\delta S^{(a+b)}=\int\sqrt{-g}\Big\{\mathrm{Tr}\big[\delta q^\mu\,\tfrac i2(\eta_{;\mu}\eta^+-\eta\,\eta^+_{;\mu})\big]-\tfrac12\mathcal L_M\,\mathrm{Tr}(\tilde q_\mu\delta q^\mu)\Big\}.$$
Feeding this into the §7.1 trace formula (using $\mathrm{Tr}(\tilde q_\nu\sigma^a)=2e_\nu{}^a$):
$$T^{(a+b)}_{\lambda\nu}=\tfrac i2\big(\eta^+q_\lambda\eta_{;\nu}-\eta^+_{;\nu}q_\lambda\eta\big)-g_{\lambda\nu}\mathcal L_M+(\chi)\;=\;\Theta_{\lambda\nu}.$$
This is **exactly NB-028's canonical tensor, off shell.** It is what NB-032's first-order program
produces. It is not symmetric.
Verified: V3a (flat background, arbitrary tetrad perturbation, arbitrary off-shell $\eta,\chi$) and
V4 (FRW, on shell, reproducing $\Theta^{[12]}=\pm a'/2a^7$ of §5).

**(c) — $\Omega=\Omega[q]$ (torsion-free, second-order).** $\Omega$ enters only through
$\tfrac i2\eta^+(q^\mu\Omega_\mu-\Omega_\mu^+q^\mu)\eta$. Split the tetrad change as
$\delta e^\mu{}_a=e^\mu{}_b(s^b{}_a+\lambda^b{}_a)$: $s$ symmetric (a real metric change), $\lambda$ antisymmetric (a
local Lorentz rotation of the frame).
- **Metric part $s$.** Varying the tetrad postulate gives $\delta\Omega$ built from $\nabla s$. The
  combination $q^\mu\delta\Omega_\mu-\delta\Omega_\mu^+q^\mu$ picks out only the totally antisymmetric part of
  the connection change, $\propto\nabla_{[\rho}s_{\nu\mu]}=0$. So (c) adds **nothing** to the
  symmetric part. Verified in its consequence: the $\Omega$-part of the variation has
  symmetric part $\equiv0$ off shell (V3b).
- **Rotation part $\lambda$.** $S_M$ is invariant under a simultaneous local rotation of tetrad and
  spinor ($\eta\to S\eta$, $\Omega\to S\Omega S^{-1}-\partial S\,S^{-1}$). On shell the spinor variation drops
  out, so the tetrad derivative contracted with any antisymmetric $\lambda$ vanishes:
  $T_{[\lambda\nu]}=0$ on shell. Off shell it is proportional to the field equation (V3b).

Together: the (c) term removes exactly the antisymmetric part of $\Theta$ on shell and leaves the
symmetric part alone:

$$\boxed{\;T_{\lambda\nu}=\frac{1}{\sqrt{-g}}\,\mathrm{Tr}\!\Big[\Big(\frac{\delta S_M}{\delta q^\nu}\Big)^{T}q_\lambda\Big]=\Theta_{(\lambda\nu)}
=\frac i4\big(\eta^+q_\lambda\eta_{;\nu}+\eta^+q_\nu\eta_{;\lambda}-\eta^+_{;\nu}q_\lambda\eta-\eta^+_{;\lambda}q_\nu\eta\big)+(\chi)\quad\text{(on shell)}\;}$$

— the Tetrode tensor of §4, now derived rather than cited.
Verified: V3b (flat background, **every** on-shell field, since the field equation is
substituted symbolically rather than a sample solution used; the canonical antisymmetric part is
nonzero there, so the symmetrization is doing real work) and V4 (FRW: full variation = the §5
Tetrode matrix $T^{00}=T^{03}=T^{33}=k/a^6$, even though $\Theta^{[12]}\neq0$).

### 7.4 Correction found on the way: operator ordering in (3.88) and (3.77)

Solving the tetrad postulate $q^\mu{}_{;\rho}=0$ at first order for an **arbitrary** tetrad perturbation
(16 free functions), with the U(1) trace projected out, gives uniquely:

$$\Omega_\rho=\tfrac14\tilde q_\mu(\partial_\rho q^\mu+\Gamma^\mu_{\tau\rho}q^\tau)=-\tfrac14(\partial_\rho\tilde q^\mu+\Gamma^\mu_{\tau\rho}\tilde q^\tau)\,q_\mu,$$
$$\Omega^{(\chi)}_\rho=-\tfrac14(\partial_\rho q^\mu+\Gamma^\mu_{\tau\rho}q^\tau)\,\tilde q_\mu=\tfrac14q_\mu(\partial_\rho\tilde q^\mu+\Gamma^\mu_{\tau\rho}\tilde q^\tau).$$

| Notebook formula | As transcribed | General-tetrad postulate (V2) |
|---|---|---|
| p.15 (3.88), 2nd form | $+\tfrac14(\partial q+\Gamma q)\tilde q$ | fails — Hermitian conjugate of the correct $\Omega$ |
| p.15 (3.88), 1st form | $-\tfrac14q(\partial\tilde q+\Gamma\tilde q)$ | fails — Hermitian conjugate |
| p.17 (3.77) | $-\tfrac14\tilde q(\partial q+\Gamma q)$ | fails — Hermitian conjugate |
| p.17 (3.79b) | $+\tfrac14q(\partial\tilde q+\Gamma\tilde q)$ | **passes** |

A Hermitian conjugate keeps the boost (Hermitian) part of $\Omega$ and flips the sign of the
rotation (anti-Hermitian) part. That is why FRW, which only has a boost-type connection, could
not tell them apart (§5 B2). With the notebook's convention $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$ and the
Lagrangian $\eta^+q^\mu\eta_{;\mu}$, Leibniz consistency fixes the ordering above. The transcribed
orderings would be right for the conjugate convention, which is plausibly Sachs' own; that can't
be settled without the book. Practical consequence: any background whose tetrad rotates (rotating
frames, Kerr) would get the spin–rotation coupling with the wrong sign if (3.88) were used as
transcribed. §§1–6 are unaffected, because they solved $\Omega$ from the postulate directly.

### 7.5 First-order (Palatini) reading — where NB-037 comes in

NB-032's own program keeps $\Omega$ independent. Then the $q$-variation of $S_M$ is the canonical,
non-symmetric $\Theta$ of (a)+(b), and the symmetric source reappears only after $\Omega$ is
eliminated through its own field equation. Because the gravitational $R$ depends on $\Omega$, that
equation forces torsion proportional to the spin density. Substituting back gives the Tetrode
tensor plus an $O(G)$ contact spin–spin term: Einstein–Cartan–Sciama–Kibble (Hehl & Datta 1971 —
cited, not computed here). The second-order and first-order routes therefore agree on the
symmetric part and differ only by torsion. That residual is NB-037's disagreement with Sachs,
which stays NEEDS-WORK.

### 7.6 Verification summary

| Check | Setting | Result |
|---|---|---|
| V0 scalar-field calibration of sign/indices | flat, co-frame perturbation | $T=\partial\varphi\partial\varphi-g\mathcal L$ exactly |
| V1 $\partial\sqrt{-g}/\partial e^\mu{}_a=-\sqrt{-g}\,e_\mu{}^a$ | generic numerical tetrad | exact; NB-032 power $(-g)^{-1/2}$ excluded by scaling weight |
| V2 tetrad postulate at $O(\epsilon)$ | arbitrary 16-function perturbation | derived Ω, Ω^(χ) and (3.79b) pass; (3.77) and both (3.88) forms fail (Hermitian conjugates); U(1) trace 0 |
| V3a Ω fixed | flat, arbitrary off-shell η, χ | $T=\Theta$ (NB-028 canonical), exact |
| V3b Ω = Ω[q] | flat, arbitrary η, χ | Ω-part symmetric part ≡ 0 off shell; on shell $T=$ Tetrode, $T_{[\lambda\nu]}=0$, while $\Theta_{[\lambda\nu]}\neq0$ |
| V4 | FRW, on-shell wave, both sectors | full variation = Tetrode ($k/a^6$ null dust); Ω-fixed variation = canonical with $\Theta^{[12]}=\pm a'/2a^7$ |

### 7.7 Verdicts

- **NB-032** — trace identity SOLID (unchanged). The $\partial(-g)^{1/2}/\partial\tilde q^\lambda$ line is INCORRECT (as transcribed) / SOLID-WITH-CORRECTION: the power should be $(-g)^{+1/2}$.
- **NB-020 / NB-017 cited Ω formulas** — no longer NOT-TESTABLE. (3.79b) SOLID. (3.77) and p.15's (3.88) are INCORRECT in the notebook's own convention (reverse the operator order); likely a convention mismatch with Sachs, not an error in his book.
- **NB-028** — the canonical tensor is now shown to be the $q$-variation at fixed $\Omega$ (a genuine
  derivation, not only a definition), and its symmetrization is shown to be the $\Omega[q]$ term.
  Verdict stays SOLID-WITH-CORRECTION (the sign, §6).

---

## 8. NB-037 (pp.28–29): the Ω field equation against ECSK, term by term

Date-time stamp: 2026-09-22 - 18:30

Verification script: `tests/runners/notebook-recon/run_NB-037_ecsk_spin_source.py` (sympy,
exact, ~5 s) → `test-results/notebook-recon/NB-037_ecsk_spin_source.json`.

**The notebook's equation (p.28):**
$$\tfrac12\big(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho\big)_{;\nu}=-\tfrac i2\,\eta^+q^\rho\eta ,$$
with the remark "Sachs gets 0 on the LHS & gets usual relation of Ω to q… but apparently this
doesn't hold!" Batch 02 read this as structurally ECSK (torsion sourced by spin) but left the
term-by-term match open. It is closed here. **Result: the LHS is exactly Cartan's
modified-torsion tensor; the RHS is the wrong projection of the correct source.** The notebook's
scalar is the U(1)/charge part of the source, which cannot balance the traceless LHS. The
missing traceless part is the ECSK spin tensor.

### 8.1 Setting

- Everything is evaluated at one point, in a local Lorentz frame ($q^\mu=\sigma^\mu$, Levi-Civita part of $\Omega$ zero).
  The Ω equation is algebraic in the non-Riemannian part of Ω, and the terms linear in it with
  derivatives are total derivatives at that point, so nothing is lost.
- Signature $(+,-,-,-)$, $\varepsilon_{0123}=+1$, $\kappa=8\pi G$.
- Gravity term: $\mathcal L_G=-\frac1{2\kappa}\sqrt{-g}\,R$. This is the sign that gives $G_{\mu\nu}=+\kappa T_{\mu\nu}$ with the §7 $T$. The notebook writes $+R$ with unit coefficient; the effect of that choice on the final equation is given in §8.5.
- $R$ in $q$-language, in a Lorentz-covariant ordering:
  $$R=-\tfrac12\mathrm{Tr}\big(K_{\mu\nu}\tilde q^\mu q^\nu+K^+_{\mu\nu}q^\nu\tilde q^\mu\big).$$
  Verified equal to the tensor Palatini scalar $e^\mu{}_ae^\nu{}_bR_{\mu\nu}{}^{ab}(\omega)$ for an arbitrary connection (E0, both sectors).
  The transcribed p.23/p.26 four-term forms mix orderings such as $K\,q\,\tilde q$ that are not Lorentz covariant for this generator. They are flagged, not used.
- Generators, fixed by §7.4:
  $$\Omega_\rho=\tfrac12\omega_{\rho ab}\Sigma^{ab},\quad \Sigma^{ab}=\tfrac14(\tilde\sigma^a\sigma^b-\tilde\sigma^b\sigma^a)\ (\eta);\qquad
  \Omega^{(\chi)}_\rho=\tfrac12\omega_{\rho ab}\Sigma_\chi^{ab},\quad \Sigma_\chi^{ab}=\tfrac14(\sigma^a\tilde\sigma^b-\sigma^b\tilde\sigma^a)\ (\chi).$$
- The notebook's p.26 margin says "treat Ω & Ω⁺ as separate variables". Here Ω is a general complex 2×2 matrix (8 real components per ρ, 32 in all), varied as real parameters. That is equivalent to the margin's rule and also covers the trace (U(1) and dilation) directions.

### 8.2 The exact source (E2, E3)

The notebook's own rule $\partial\,\mathrm{Tr}(AB)/\partial B=\tilde A$, applied to $\tfrac i2\eta^+q^\rho\Omega_\rho\eta=\tfrac i2\mathrm{Tr}(\Omega_\rho\,\eta\eta^+q^\rho)$, gives a **matrix**, not a scalar:
$$\frac{\partial\mathcal L_M}{\partial\Omega_\rho}=\tfrac i2\big(\eta\eta^+q^\rho\big)^{T}.$$
The Fierz identity for a 2-spinor, $\eta\eta^+=\tfrac12 j^a\tilde\sigma_a$ with $j^a=\eta^+\sigma^a\eta$ and $j^aj_a=0$, splits it:
$$\eta\eta^+q^\rho=\underbrace{\tfrac12\big(\eta^+q^\rho\eta\big)\,I}_{\text{trace}}\;+\;\underbrace{j_a\Sigma^{a\rho}}_{\text{traceless}} .$$
- The **trace** is the notebook's $\eta^+q^\rho\eta$. So the notebook wrote the trace of the source, not the source.
- The **traceless** part pairs with the Lorentz (spin-connection) part of Ω. That is where ECSK lives.

### 8.3 The ECSK spin tensor for $\eta$, $\chi$ and Dirac matter (E1, E4, E7)

The matrix identity that does the work (exact, all index values):
$$\sigma^c\Sigma^{ab}-\Sigma^{ab\,+}\sigma^c=-i\,\varepsilon^{cabd}\sigma_d,\qquad
\tilde\sigma^c\Sigma_\chi^{ab}-\Sigma_\chi^{ab\,+}\tilde\sigma^c=+i\,\varepsilon^{cabd}\tilde\sigma_d .$$
The symmetric pieces cancel, so only the totally antisymmetric ε structure survives. The spin
tensor $S^{\rho ab}=\partial\mathcal L_M/\partial\omega_{\rho ab}$ is therefore totally antisymmetric:
$$S_\eta^{\rho ab}=+\tfrac12\varepsilon^{\rho abd}j^\eta_d,\qquad S_\chi^{\rho ab}=-\tfrac12\varepsilon^{\rho abd}j^\chi_d .$$
With $\psi=(\chi,\eta)$ and $\gamma^\mu=\begin{pmatrix}0&\sigma^\mu\\\tilde\sigma^\mu&0\end{pmatrix}$, $\gamma^5=\mathrm{diag}(-1,1)$:
- vector current $\bar\psi\gamma^\mu\psi=j_\eta^\mu+j_\chi^\mu$;
- axial current $\bar\psi\gamma^\mu\gamma^5\psi=j_\eta^\mu-j_\chi^\mu$;
- $S^{\rho ab}_{\rm Dirac}=\tfrac12\varepsilon^{\rho abd}J^5_d$, the textbook ECSK form: axial and totally antisymmetric.

**This answers batch 02's worry directly.** "Built from an axial bilinear, not the vector
current" is a Dirac-field statement. For a single 2-spinor, the vector bilinear $\eta^+\sigma^\mu\eta$
*is* its axial current, up to the chirality sign. So the structure of the notebook's
$\eta^+q^\rho\eta$ is the right one. What is wrong is where it sits: it is placed in the trace
slot, and ECSK needs it in the traceless slot contracted with ε.

### 8.4 Solving the connection equation (E5, E6, E8)

The equation was solved two independent ways, with the same answer (E5b):
- (a) standard ECSK in tensor variables $\omega_{\rho ab}$ (24 real unknowns);
- (b) the notebook's own variable Ω (all 32 real components).

$$K_{\rho ab}=-\tfrac14\kappa\,\varepsilon_{\rho abd}\,j^d,\qquad T_{\lambda\tau\nu}=-\tfrac12\kappa\,\varepsilon_{\lambda\tau\nu d}\,j^d .$$
The torsion is read off the tetrad postulate with the solved Ω, and the resulting Γ is metric
compatible. For trace-free spin this is **exactly the Cartan equation** $T_{\lambda\tau\nu}=\kappa S_{\lambda\tau\nu}$, with ratio $+1$.

The remaining directions of Ω behave differently:
- **Real trace (dilation):** its equation is $0=0$. It is pure gauge and absent everywhere.
- **Imaginary trace (the U(1) direction, $\Omega\supset iA_\mu I$):** absent from $R$ (the commutator and $\mathrm{Tr}(\tilde q^{[\mu}q^{\nu]})$ both vanish), but present in the matter term. Its equation is $0=-j^\rho$, a constraint no nonzero spinor satisfies.

**The notebook's LHS.** At the point, $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}=\tfrac12[\Omega_\nu,\tilde\sigma^\rho\sigma^\nu-\tilde\sigma^\nu\sigma^\rho]\equiv N^\rho$. For an **arbitrary** metric-compatible connection (E8):
$$N^\rho=-\,C^{\rho}{}_{ab}\,\Sigma^{ab},\qquad C^{\rho ab}=T^{\rho ab}+\eta^{\rho a}T^b-\eta^{\rho b}T^a ,$$
which is Cartan's modified-torsion tensor. Further checks:
- $N^\rho$ is traceless.
- The map Ω(Lorentz) → $N$ has rank 24 (E6), so $N=0\iff T=0$.
- The Euler–Lagrange derivatives are $\partial\mathcal L_G/\partial\omega_{\rho ab}=\tfrac1\kappa\mathrm{Re\,Tr}(N^\rho\Sigma^{ab})$ and $\partial\mathcal L_M/\partial\omega_{\rho ab}=2\,\mathrm{Re\,Tr}\big(\tfrac i2\eta\eta^+q^\rho\,\Sigma^{ab}\big)$. The trace part drops out because $\mathrm{Tr}\,\Sigma=0$.

The p.28 "first way… appears to all go to 0" is the torsion-free assumption. It is exactly Sachs'
"0 on the LHS", and it is equivalent to discarding the spin source.

### 8.5 The corrected NB-037 equation

$$\boxed{\;\tfrac12\big(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho\big)_{;\nu}=-2\kappa\cdot\tfrac i2\Big[\eta\eta^+q^\rho-\tfrac12\big(\eta^+q^\rho\eta\big)I\Big]\;+\;(\chi:\ \tilde q,\ \Sigma_\chi)\;}$$

- It holds as a full 2×2 matrix identity at the solution (E8).
- In the notebook's normalization, $\mathcal L=\sqrt{-g}\{+R+\mathcal L_M\}$, the prefactor $-2\kappa$ becomes $+1$.
- Written in tensor form, it is the Cartan equation $C^{\rho ab}=\kappa S^{\rho ab}$ with $S^{\rho ab}=\tfrac12\varepsilon^{\rho abd}j_d$.

Term-by-term comparison with the notebook:

| Piece | Notebook p.28 | Correct |
|---|---|---|
| LHS | $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}$ | same — Cartan tensor $-C^\rho{}_{ab}\Sigma^{ab}$, traceless |
| RHS, traceless part | absent | $-i\kappa\,j_a\Sigma^{a\rho}\ \leftrightarrow\ $ ECSK spin $\tfrac12\varepsilon^{\rho abd}j_d$ |
| RHS, trace part | $-\tfrac i2\eta^+q^\rho\eta$ | belongs to the U(1) equation, whose gravitational LHS is identically 0 |

Where the slip sits: the p.28 line "$\partial\mathcal L/\partial\Omega_\rho=\tfrac i2\eta^+q^\rho\eta\sqrt{-g}$" applies
the trace rule but keeps the scalar $\eta^+q^\rho\eta$ instead of the outer product $(\eta\eta^+q^\rho)^T$.

### 8.6 What this does to the physics

- **Sachs vs the notebook.** Both are partly right. Sachs' LHS = 0 is the torsion-free (Riemannian) theory, which is consistent only if the spin source is dropped. The notebook is right that the LHS need not vanish, but it paired the LHS with the wrong source. The correct statement is ECSK: torsion equals spin, is algebraic, and is non-propagating.
- **Hehl–Datta contact term (E7).** Substituting the solution back gives $\mathcal L_{\rm eff}=\tfrac3{16}\kappa\,J^5_aJ^{5a}=\tfrac{3\pi G}{2}J^5\!\cdot\!J^5$. The magnitude is the standard ECSK coefficient; the sign follows the conventions above.
  - For a single 2-spinor the contact term vanishes identically, because $j^aj_a=0$ for a commuting 2-spinor. The torsion is still nonzero.
  - For Dirac matter, $J^5\!\cdot\!J^5=-2\,j_\eta\!\cdot\!j_\chi$.
  - These are classical commuting fields; Grassmann ordering would change the Fierz step.
- **The U(1) direction.** In this Lagrangian, $\mathrm{Tr}\,\Omega$ has no kinetic term, so varying it forces $j^\rho=0$. Either it is not an independent variable (set to the pure-gauge value), or a Maxwell term $-\tfrac14F^2$ with $F=\partial\,\mathrm{Im}\,\mathrm{Tr}\Omega$ must be added. In the second case the notebook's scalar $\eta^+q^\rho\eta$ becomes exactly the electric current source $\partial_\nu F^{\nu\rho}\propto j^\rho$. That is a clean home for the notebook's RHS and fits Sachs' aim of getting electromagnetism out of the spinor connection, but it has to be put in; it does not follow from $R$.
- **Model relevance.** In the CA model, gravity is the induced Einstein equation (key decision 4 / F178) with no independent connection, i.e. the torsion-free branch. ECSK torsion would add only the $O(G)$ contact term above, an energy density $\sim G\,n^2$ for spin density $n$. That is negligible at any laboratory or astrophysical density short of the extreme early universe. This is recovered standard physics, not a model claim; no claim card.

### 8.7 Verification summary

| Check | Result |
|---|---|
| E0 $R$ in $q$-language = tensor Palatini $R(\omega)$, generic connection, η and χ | exact |
| E1 $\sigma^c\Sigma^{ab}-\Sigma^{ab+}\sigma^c=-i\varepsilon^{cabd}\sigma_d$ (χ: $+i\,\tilde\sigma_d$) | exact, all components |
| E2 Fierz $\eta\eta^+=\tfrac12j^a\tilde\sigma_a$, $j^2=0$ | exact |
| E3 $\partial\mathcal L/\partial\Omega_\rho=\tfrac i2(\eta\eta^+q^\rho)^T$; trace = notebook scalar; traceless = $j_a\Sigma^{a\rho}$ | exact |
| E4 $S^{\rho ab}=\pm\tfrac12\varepsilon^{\rho abd}j_d$, totally antisymmetric | exact, all 64 components |
| E5 contorsion $-\tfrac14\kappa\varepsilon j$, torsion $-\tfrac12\kappa\varepsilon j$, spinor solve = tensor solve, Cartan ratio $+1$, Γ metric-compatible | exact |
| E5 U(1) equation $0=-j^\rho$; dilation $0=0$ | exact |
| E6 EL projections; rank(Ω → LHS) = 24; trace directions absent from $R$ | exact |
| E7 $J=j_\eta+j_\chi$, $J^5=j_\eta-j_\chi$, $S_{\rm Dirac}=\tfrac12\varepsilon J^5$, $\mathcal L_{\rm eff}=\tfrac3{16}\kappa J^5\!\cdot\!J^5$, single Weyl $\mathcal L_{\rm eff}=0$ | exact |
| E8 LHS $=-C^\rho{}_{ab}\Sigma^{ab}$ (generic connection); corrected equation holds as full 2×2 | exact |

### 8.8 Verdict

**NB-037: NEEDS-WORK → SOLID-WITH-CORRECTION (resolved).** The LHS and the author's suspicion
that it need not vanish are both correct: it is the Cartan tensor. The RHS is the trace (U(1))
projection of the true source $\tfrac i2(\eta\eta^+q^\rho)^T$; the spin (traceless) projection was dropped.
With the correction, NB-037 is the ECSK Cartan equation, term by term.

---

## 9. NB-038 (p.29): the $q^\lambda$ field equation and the missing equations of motion

Date-time stamp: 2026-09-22 - 19:30

Verification script: `tests/runners/notebook-recon/run_NB-038_q_field_equations.py` (sympy,
exact, ~12 s; imports the §8 machinery) →
`test-results/notebook-recon/NB-038_q_field_equations.json`.

**What p.29 has.** Two partial derivatives and a note, then the page stops. Page 30 is blank,
and page 31 starts a new topic:
$$\frac{\partial\mathcal L}{\partial q^\lambda}=(-g)^{1/2}\Big(-\tfrac12\big(K^+_{\lambda\rho}\tilde q^\rho+\tilde q^\rho K_{\lambda\rho}\big)^*+\tfrac14R\,\tilde q^*_\lambda\Big),\qquad
\frac{\partial\mathcal L_M}{\partial q^\lambda}=\big(\tfrac i2\eta^+\eta_{;\lambda}-\tfrac i2\eta^+_{;\lambda}\eta\big)(-g)^{1/2},$$
"Need $\tilde\Omega^{(\chi)}_\rho=-\Omega^{x+}_\rho=\Omega_\rho$."

**What is missing.** Three things were never written:
- the $q^\lambda$ field equation itself;
- the χ equation (NB-034 did only η);
- the connection-coupled matter equations once NB-037's torsion is kept.

All three are constructed here and checked against each other.

### 9.1 The two p.29 derivatives, corrected (G1, G3)

**Gravity piece.** With the Lorentz-covariant $R=-\tfrac12\mathrm{Tr}(K_{\mu\nu}\tilde q^\mu q^\nu+K^+_{\mu\nu}q^\nu\tilde q^\mu)$ of §8.1, differentiating directly gives
$$\frac{\partial R}{\partial q^\lambda}\Big|_{\tilde q}=\tfrac12\big(K_{\lambda\rho}\tilde q^\rho+\tilde q^\rho K^+_{\lambda\rho}\big)^{T}.$$
The p.29 bracket has $K$ and $K^+$ on the opposite sides. It does not match with either overall
sign; the swap follows from the non-covariant $R$ ordering transcribed on p.23 (flagged in §8.1).
The $\tfrac14R\,\tilde q^*_\lambda$ term is the $\sqrt{-g}$ derivative. Its form is consistent with §7.2
(the symmetric split, Sachs' sign), and here it carries the correct power $(-g)^{+1/2}$ as an overall factor.

**Matter piece.** The trace rule gives a matrix, not a scalar:
$$\frac{\partial\mathcal L_M}{\partial q^\lambda}=\tfrac i2\big(\eta_{;\lambda}\eta^+-\eta\,\eta^+_{;\lambda}\big)^{T}\sqrt{-g}.$$
The p.29 expression is its trace. This is the same scalar-for-outer-product slip as NB-037's p.28 line (§8.5).
Contracted with the tetrad, $\mathrm{Tr}\big[(\partial\mathcal L_M/\partial q^\nu)^Tq_\lambda\big]=\tfrac i2(\eta^+q_\lambda\eta_{;\nu}-\eta^+_{;\nu}q_\lambda\eta)$ is exactly
the canonical $\Theta_{\lambda\nu}$ of §7 (the $-g\mathcal L_M$ part comes from $\partial\sqrt{-g}$).

### 9.2 The $q^\lambda$ field equation (G2)

$q^\mu$ and $\tilde q^\mu$ are one tetrad, so NB-032's "treat them independently" has to be recombined as
$e_{\lambda a}\,\partial/\partial e^\nu{}_a=\mathrm{Tr}[(\partial/\partial q^\nu)^Tq_\lambda]+\mathrm{Tr}[(\partial/\partial\tilde q^\nu)^T\tilde q_\lambda]$. With Ω held fixed, for an arbitrary connection:
$$\mathrm{Tr}\Big[\Big(\frac{\partial(\sqrt{-g}R)}{\partial q^\nu}\Big)^{T}q_\lambda\Big]+\mathrm{Tr}\Big[\Big(\frac{\partial(\sqrt{-g}R)}{\partial\tilde q^\nu}\Big)^{T}\tilde q_\lambda\Big]
=\sqrt{-g}\,\big(2R_{\lambda\nu}-g_{\lambda\nu}R\big)=2\sqrt{-g}\,G_{\lambda\nu}(\Omega),$$
with $R_{\lambda\nu}=R^\mu{}_{\lambda\mu\nu}(\Omega)$. The fit was exact, with coefficients $(2,0,-1)$. Adding the matter piece, the
missing NB-038 equation is:

$$\boxed{\;G_{\lambda\nu}(\Omega)=\kappa\,\Theta_{\lambda\nu}(\Omega),\qquad
\Theta_{\lambda\nu}=\tfrac i2\big(\eta^+q_\lambda\eta_{;\nu}-\eta^+_{;\nu}q_\lambda\eta\big)+\tfrac i2\big(\chi^+\tilde q_\lambda\chi_{;\nu}-\chi^+_{;\nu}\tilde q_\lambda\chi\big)-g_{\lambda\nu}\mathcal L_M\;}$$

This is the Sciama–Kibble tetrad equation. It is not symmetric: $G_{\lambda\nu}(\Omega)$ is the Einstein tensor
of the connection with torsion, and $\Theta$ is NB-028's canonical tensor with the full Ω. In the
notebook's normalization ($\mathcal L=\sqrt{-g}\{R+\mathcal L_M\}$) replace κ by $-\tfrac12$.

### 9.3 The complete system and its consistency (G4–G6)

Together with NB-034 and the corrected NB-037, the first-order theory has three field
equations:

| Variable | Equation | Source page |
|---|---|---|
| η | $q^\mu\eta_{;\mu}=0$ (full Ω, torsion included) | NB-034 |
| χ | $\tilde q^\mu\chi_{;\mu}=0$ (full $\Omega^{(\chi)}$) | missing — constructed here |
| Ω | $\tfrac12(\tilde q^\rho q^\nu-\tilde q^\nu q^\rho)_{;\nu}=-i\kappa[\eta\eta^+q^\rho-\tfrac12(\eta^+q^\rho\eta)I]+(\chi)$, i.e. $C^{\rho ab}=\kappa S^{\rho ab}$ | NB-037 (corrected, §8.5) |
| $q^\lambda$ | $G_{\lambda\nu}(\Omega)=\kappa\Theta_{\lambda\nu}(\Omega)$ | NB-038 — constructed here |

Substituting the Ω solution ($K_{\rho ab}=-\tfrac14\kappa\varepsilon_{\rho abd}J_5^d$, $J_5=j_\eta-j_\chi$) splits $\Omega=\mathring\Omega+\Omega^K$ and reduces the system to Riemannian form:

**(i) Antisymmetric part of the $q$ equation.** This is not a new equation. At $O(\kappa)$, the part of $G_{[\lambda\nu]}$ linear in $\partial K$ equals $\kappa\Theta_{[\lambda\nu]}$ **on the matter shell, identically**. It is the Belinfante–Rosenfeld identity combined with the Cartan equation. The identity fails off shell (G5, flat background, generic Dirac field, all components). At $O(\kappa^2)$ both $G^{KK}_{[\lambda\nu]}$ and $\Theta^K_{[\lambda\nu]}$ vanish identically, because K and S are both ε-type (G4). So the $q$ equation's antisymmetric part carries no information beyond the matter and Ω equations. That is the consistency the batch-02 ledger asked for.

**(ii) Symmetric part: the effective Einstein equation.**
$$\boxed{\;\mathring G_{\mu\nu}=\kappa\Big[T^{\rm Tetrode}_{\mu\nu}-g_{\mu\nu}\,\tfrac3{16}\kappa\,J_5\!\cdot\!J_5\Big]\;}$$
Here $T^{\rm Tetrode}$ is §4's tensor built with $\mathring\Omega$ (including its $-g\mathcal L^0_M$, which no longer vanishes on the torsion-modified shell). Pointwise, as found (G4, G4b):
- $[\kappa\Theta^K-G^{KK}]_{(\mu\nu)}=+\tfrac3{16}\kappa^2g_{\mu\nu}J_5^2$;
- at the solution, $\mathcal L^K_M=\tfrac38\kappa J_5^2$ and $-R^{KK}/2\kappa=-\tfrac3{16}\kappa J_5^2$, so $\mathcal L_{\rm eff}=\tfrac3{16}\kappa J_5^2$;
- the boxed form follows exactly, agreeing with the metric variation of the Hehl–Datta effective action.

For a single 2-spinor the contact term drops out ($j^2=0$), leaving §7's result, $\mathring G=\kappa T^{\rm Tetrode}$.

**(iii) The matter equations with torsion — the missing χ analog of NB-034 (G6):**
$$\boxed{\;\sigma^\mu\mathring\nabla_\mu\eta-\tfrac{3i}{8}\kappa\,(J_5)_a\sigma^a\,\eta=0,\qquad
\tilde\sigma^\mu\mathring\nabla_\mu\chi+\tfrac{3i}{8}\kappa\,(J_5)_a\tilde\sigma^a\,\chi=0\;}$$
(written with the local-frame $\sigma^\mu$; in general $q^\mu,\tilde q^\mu$). The torsion term is computed directly as $\tfrac12(q^\mu\Omega^K_\mu-\Omega^{K+}_\mu q^\mu)$. It is identical to $\partial/\partial\eta^+$ of $\mathcal L_{\rm eff}$ (coefficient $2\cdot\tfrac3{16}=\tfrac38$), with the opposite sign for χ. In Dirac form this is the Hehl–Datta equation: a cubic axial self-interaction with coefficient $\tfrac38\kappa$. The overall sign of the Dirac-form term depends on the $\gamma^5$ convention and was not separately run; the 2-spinor forms above are the verified ones. With torsion off ($\kappa\to0$ in the contact term) they reduce to NB-034's boxed $q^\mu\partial_\mu\eta+q^\mu\Omega_\mu\eta=0$ and its χ twin $\tilde q^\mu\partial_\mu\chi+\tilde q^\mu\Omega^{(\chi)}_\mu\chi=0$.

### 9.4 The p.29 note resolved (G7)

"Need $\tilde\Omega^{(\chi)}_\rho=-\Omega^{x+}_\rho=\Omega_\rho$". With the §7.4 connections, for an arbitrary Lorentz connection:
$$\Omega^{(\chi)}_\rho=-\Omega_\rho^{\,+}\quad\Longleftrightarrow\quad -\big(\Omega^{(\chi)}_\rho\big)^+=\Omega_\rho ,$$
which is exactly the note's second equality. It is also the condition that p.17's $\chi=\varepsilon\eta^*$ ansatz is
covariant: $\varepsilon\Omega^*\varepsilon^{-1}=-\Omega^+=\Omega^{(\chi)}$, and $\tilde\sigma^\mu\varepsilon=\varepsilon\sigma^{\mu*}$, so η's equation maps onto χ's.
The first equality, read with $\tilde{}$ as transpose (or ε-conjugated transpose, either sign), is **false** in
all four readings tested. The note is right in content; the tilde there is unexplained. Consequence:
with $\chi=\varepsilon\eta^*$ the χ equation of 9.3 is not independent. It is the charge conjugate of the η
equation, and the χ half of each field equation duplicates the η half.

### 9.5 Verification summary

| Check | Result |
|---|---|
| G1 $\partial R/\partial q^\lambda=\tfrac12(K_{\lambda\rho}\tilde q^\rho+\tilde q^\rho K^+_{\lambda\rho})^T$ (brute force) | exact; p.29 ordering does not match (either sign) |
| G2 tetrad derivative of $\sqrt{-g}R$ = $\sqrt{-g}(2R_{\lambda\nu}-gR)$, generic connection | exact, fit $(2,0,-1)$ |
| G3 $\partial\mathcal L_M/\partial q^\lambda$ = outer product; p.29 = its trace; contraction = canonical Θ | exact |
| G4 $G^{KK}_{[\,]}=\Theta^K_{[\,]}=0$; $[\kappa\Theta^K-G^{KK}]_{(\,)}=\tfrac3{16}\kappa^2gJ_5^2$ | exact |
| G4b $\mathcal L^K_M=\tfrac38\kappa J_5^2$, $-R^{KK}/2\kappa=-\tfrac3{16}\kappa J_5^2$, $\mathcal L_{\rm eff}=\tfrac3{16}\kappa J_5^2$; effective Einstein eqn consistent | exact |
| G5 $G_{[\lambda\nu]}(\partial K)=\kappa\Theta_{[\lambda\nu]}$ on shell (flat, generic Dirac), fails off shell | exact, all components |
| G6 torsion terms $\mp\tfrac{3i}8\kappa J_5\!\cdot\!\sigma$ (η, χ) = $\partial\mathcal L_{\rm eff}/\partial\psi^+$ | exact |
| G7 $\Omega^{(\chi)}=-\Omega^+$; $\varepsilon\Omega^*\varepsilon^{-1}=\Omega^{(\chi)}$; $\tilde\sigma^\mu\varepsilon=\varepsilon\sigma^{\mu*}$; transpose readings false | exact |

### 9.6 Verdict

**NB-038: NEEDS-WORK → SOLID-WITH-CORRECTION (completed).**
- The two p.29 derivatives are structurally right. The gravity piece has $K\leftrightarrow K^+$ swapped (inherited from the non-covariant $R$ ordering). The matter piece writes the trace for the outer product.
- The missing equations are constructed: the $q^\lambda$ equation $G_{\lambda\nu}(\Omega)=\kappa\Theta_{\lambda\nu}(\Omega)$, the χ equation, and the torsion-coupled matter equations. They are consistent with NB-034 and the corrected NB-037.
- After eliminating torsion they reduce to Einstein + Tetrode + the Hehl–Datta contact interaction.
- The p.29 note is correct as $-\Omega^{(\chi)+}=\Omega$, and it is the covariance condition for $\chi=\varepsilon\eta^*$.

This completes the pp.15–29 Sachs-Lagrangian sequence as a closed first-order (ECSK) system.
