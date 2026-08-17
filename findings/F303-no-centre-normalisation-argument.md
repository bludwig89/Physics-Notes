# F303 — There is **no argument** for centre-normalising F144's bare coupling: three candidates closed exactly (scheme constant off by 26×, the three-link plaquette the BCC graph provably lacks, the Cartan reading's Landau pole), F144 steps 1–2 survive and **step 3 is the break**

**Date:** 2026-08-06 - 19:58
**Numbering:** **F303**, taken as `NEXT FREE NUMBER` — **renumbered from F300 mid-session**: 300, 301 and 302 were spent by concurrent sessions between this session's two `casim index` calls. The stale `test-results/F300_coupling_normalisation.json` is in `test-results/_to_delete/`, where the F301 session had already put its own two collisions. **Re-check the max F-number immediately before writing, not at the start of the session.**
**Status:** Confirmed — **8/8 PASS**, both declared controls verified red at exactly the checks declared. N1/N2/N3/N3b/N5 are exact (sympy over ℚ, plus exhaustive enumeration); N4/N6/N7 are quantitative comparisons against F144's own measured A4 residual and the PDG coupling.
**Verdict:** **The argument F299 asked for does not exist, and this finding is mostly a list of ways it cannot be built.** *What survives of F144:* steps 1–2. The rotor lemma's residual factorises as $(r-1)\times$sine with $r=a/b$, so orthogonality at generic tick holds **iff $a=b$ whatever the scale** — the lemma constrains a *ratio* and carries no representation content, and by F91/decision-5 the gluon uses the same even rotation law as the photon, so the $\chi=1$ lock transfers to colour legitimately rather than being an EM result reused. *What breaks:* step 3, which reads the rotor's $\hat E^2$ spectrum as the integer $m^2$ of a compact U(1)/$\mathbb Z_N$ ladder. **The dispute is one rational number**: at $N=3$ the two ladders are exactly proportional with constant $C_F=4/3$ (F298), so there is nothing to interpret. Three candidate reconciliations are closed: (1) **not** a scheme constant — the shift is $26\times$ F144's entire *measured* A4 residual; (2) **not** a three-link plaquette — the BCC nearest-neighbour graph has no closed 3-bond loop, by parity and by exhaustive enumeration; (3) **not** the Cartan projection — it gives a Landau pole above $M_Z$. What remains is a genuine fork the tree cannot currently choose between, and it is named in §6.
**Modules:** `src/casim/engine/gauge/derive_coupling_normalisation.py` (new)
**Test / results:** record `F303-coupling-normalisation` (tier gate, entry `check_coupling_normalisation`) → `test-results/F303_coupling_normalisation.json`
**Cross-references:** [[F299-casimir-scaling-discriminator-reinstated]] (the measurement that made this the open item, and that moved it from F110 to F144), [[F298-casimir-ladder-c7-rerun]] (the exact proportionality of the two ladders at $N=3$), [[F294-c7-chi-map-ncolour-audit]] (H1/H2), [[F144-route-a-alpha-s-dimensional-transmutation]] (the chain audited: A1 steps 1–2 stand, step 3 breaks; A4 is the residual N4 uses), [[F115-coupling-magnitudes-running-rotor]] (CM3, the lock traced), [[F101-strong-coupling-sigma-compact-rotor]] (the rotor, and the A-vs-C caveat named at the source on 2026-06-05), [[F110-realtime-link-hamiltonian-confinement]] (C7, and $\hat E$ as the *integer* electric field), [[F91-propagator-parity-classification]] (the gluon's even law, which is why the lock transfers), [[F265-composite-sc-plaquette-bianchi]] (the BCC minimal loop), CL022 (the $\alpha_s(M_Z)$ tension whose $2.1\sigma$ framing is contingent on H1), CL257.

---

## 1. The question, stated so it can be answered

F299 closed with one item and moved it off F110:

> Either an argument that the model's coupling is normalised on the **centre** — which would have to explain why the running then uses the $SU(N_c)$ $\beta$-function — or acceptance that F144's agreement is a coincidence.

This finding looks for that argument. **It does not find one.** What it produces instead is a located break and three closed doors, which is more useful than a shrug, because each door is closed by a computation someone can re-run.

---

## 2. What survives: $\chi=1$ is group-blind, and the lock legitimately transfers to colour

F144's A1 has three steps. The first two are fine, and it is worth being precise about *why*, because it is what makes step 3 the only suspect.

**Step 1** — the rule's per-mode $(\mathbf E,\mathbf B)$ map is an exact circular rotation (residuals $<10^{-15}$ on all modes). Unchanged.

**Step 2** — the rotor lemma. Re-derived symbolically here, and the useful form is the factorisation. Writing $a=rb$, every entry of $M^{\rm T}M-\mathbb 1$ comes out as

$$[0,0]=(r-1)\sin^2\!\big(b\sqrt r\,t\big),\qquad [0,1]=[1,0]=(1-r)\,\frac{\sin\!\big(2b\sqrt r\,t\big)}{2\sqrt r},\qquad [1,1]=-(r-1)\frac{\sin^2\!\big(b\sqrt r\,t\big)}{r}.$$

**Every entry carries an explicit factor $(r-1)$**, so orthogonality at generic tick holds **iff $r=1$, whatever $b$ is.** The lemma constrains the electric/magnetic stiffness *ratio* and nothing else. (`solve` also returns roots like $r=\pi^2/(b^2t^2)$; every one of them contains $t$ — they are ticks landing on a half-period, where the flow is $\pm\mathbb 1$ for *any* stiffness. Those are not conditions on the stiffness, and the check requires them to be $t$-dependent so that the distinction is enforced rather than asserted.)

Because the condition is a ratio, it is **group-blind**: no Casimir, no dimension, no representation content. So $\chi=1$ is *not* what H1 vs H2 is about, and any attempt to fix the problem by revisiting the circularity argument is looking in the wrong place.

**And the transfer to colour is legitimate.** One might worry that `ca_wmu._f26_rotation_step` is the *photon's* law and that F144 imported an EM result into the colour sector. It is not an import: by F91 and decision 5 the gluon propagator is **even** — forced, colour coupling branch-blind — i.e. the same rotation law. So the circularity holds in the colour channel on its own account.

---

## 3. What breaks: step 3, and the dispute is a single rational number

Step 3 is F110's C7 matching, and it reads the rotor's $\hat E^2$ spectrum as the **integer** $m^2$ of a compact U(1)/$\mathbb Z_N$ ladder — which is exactly what `link_hamiltonian.py` implements ("$\hat E_\ell$ the integer (compact) electric field"). For $SU(3)$ the electric operator's eigenvalue on a link carrying irrep $R$ is $C_2(R)$.

At $N=3$ these two ladders are **exactly proportional**:

| model level $m$ | $s(m)^2$ | lowest irrep of that triality | $C_2$ | ratio |
|---:|---:|---|---:|---:|
| 1 | 1 | $(1,0)$ | 4/3 | **4/3** |
| 2 | 1 | $(0,1)$ | 4/3 | **4/3** |

One distinct ratio, exactly $C_F$, over ℚ. **So this is not a matter of interpretation.** The model's $\mathbb Z_3$ Hamiltonian is a *correct* effective description of the $SU(3)$ ladder at $N=3$ — same shape, differing by one constant — and that constant is the whole of H1 vs H2. Either it is 1 or it is 4/3, and no amount of reading resolves a number.

The two branches, run to $M_Z$ at one loop:

| reading | $\chi$ | $g_s$ | $\alpha_s(\mu_0)$ | $\alpha_s(M_Z)$ | vs PDG 0.1180 |
|---|---:|---:|---:|---:|---:|
| **H1** integer flux | 1 | $\tfrac12$ | $1/(16\pi)$ | 0.11858 | $+0.5\%$ |
| **H2** Casimir | 1 | $\tfrac{\sqrt3}{4}=0.43301$ | $1/(16\pi C_F)$ | **0.03970** | $\mathbf{-66.4\%}$ |

**This is falsification-grade, not a tension.** And inverting instead for what the data demands: $\chi_{\rm required}=1.000828$ — **the derived $\chi=1$ to $0.083\%$** — where the Casimir reading needs $\chi=1/C_F=0.75$, off by $33\%$. The model's derived number is the one the measurement wants, and the model's own $SU(3)$ engine (F299) says it should not be.

---

## 4. Three candidate reconciliations, each closed

### 4.1 "The Casimir is absorbed into F144's scheme constant." No — by a factor of 26

F144's A4 *measured* the gap between the rule's $1/\alpha_0=16\pi$ and what the measured $\alpha_s(M_Z)$ demands at $\mu_0$: $\Delta(1/\alpha)=0.64$, i.e. $\Lambda_{\rm scheme}/\Lambda_{\rm rule}=1.78$ (against 28.81 for the Wilson action — the rule is already 16× closer to continuum).

The Casimir shift is $16\pi(C_F-1)=16\pi/3=16.755$.

| | $\Delta(1/\alpha)$ | $\Lambda$ ratio |
|---|---:|---:|
| F144 A4, **measured** | 0.64 | 1.78 |
| Wilson action, for scale | 4.03 | 28.81 |
| **what the Casimir demands** | **16.755** | $\mathbf{3.4\times10^{6}}$ |

$26\times$ the entire measured residual, and a $\Lambda$ ratio five decades past the Wilson action's. F298 said the $C_F$ is not absorbable because it sits in the exponent; this is the number that says so.

### 4.2 "The colour plaquette has three links, not four." The prettiest candidate, and the lattice refuses it

This is the only reconciliation that would keep **both** $g_s=\tfrac12$ **and** the Casimir, and it is genuinely elegant. C7 with a Casimir reads $\chi=1/(n\,g^2C_F)$ for a plaquette with $n$ exclusive boundary links, so

$$n\,C_F=4\quad\text{reproduces the abelian answer exactly},\qquad C_F=\tfrac43\ \Longrightarrow\ n=3 .$$

Better still, inverting at $n=3$ for the group: $3\cdot\frac{N^2-1}{2N}=4$ gives $3N^2-8N-3=0$, whose roots are $N=3$ and $N=-\tfrac13$ — so **$N_c=3$ uniquely**, and B10 would have gained a second structural leg for free.

**The BCC lattice does not have a 3-bond loop.** The proof is one line of parity: the nearest-neighbour hops are the eight $(\pm1,\pm1,\pm1)$, so each Cartesian component of a sum of *three* hops is a sum of three odd numbers, hence odd, hence never zero. Checked here against exhaustive enumeration as well — **0 of the $8^3$ hop triples close; 216 of the $8^4$ quadruples do** — and `bcc_action.py` has carried the statement since F265: *"no 3-bond closed loops exist, so the minimal gauge loop is a 4-bond [rhombus]."*

So $n=4$ is **derived geometry**, not a convention, and it cannot be traded for the Casimir. Recorded here as a *closed* candidate precisely because it is attractive enough to be re-derived by someone who does not know the lattice forbids it.

**Control (declared).** `--param assume_three_bond_loop=True` pretends the graph supplies one; N3 goes red. A geometric exclusion that cannot fail is not an exclusion.

### 4.3 "The integer ladder is the abelian-projected Cartan charge." No, and it fails the other way

If the model's integer flux were the maximal-abelian-projection charge, the normalisation would be the fundamental's Cartan weight length. With $T^3=\tfrac12\mathrm{diag}(1,-1,0)$ and $T^8=\tfrac1{2\sqrt3}\mathrm{diag}(1,1,-2)$, all three weights have $\lvert\lambda\rvert^2=\tfrac13$ **exactly** (rational, though $T^8$ is not). That gives $\alpha_0=3/(16\pi)=0.0597$, and the coupling hits a **Landau pole above $M_Z$** — it never reaches the $Z$ at all.

So the three candidate normalisations are $1$ (integer flux), $4/3$ (Casimir) and $1/3$ (Cartan), and **only the one with no group factor whatsoever lands the data.** That is either a strong hint or a strong coincidence, and §6 refuses to pretend it knows which.

---

## 5. The caveat is two months old and has been load-bearing the whole time

Worth recording, because it changes how much weight the $0.083\%$ can carry. F101 §7 wrote this on **2026-06-05**:

> **U(1) rotor vs $\mathbb Z_3$ centre.** …the precise centre projection at intermediate coupling carries the same **A-vs-C / Casimir caveat** as F98–F100 ($\sigma_2=2\sigma_1$ Abelian vs $\sigma_1$ Casimir).

F144 was built on top of that caveat a week later, F115's CM3 before it, and F294/F298/F299 rediscovered it as "H1 vs H2" two months on. **The tree flagged this at the source and then derived a headline number across it without choosing.** Nothing here is a surprise that arrived from outside; it is a deferral coming due.

---

## What this closes and what remains

**Closes.** F299's named open item, in the negative and with reasons: there is no argument for centre normalisation, and the three candidate ways to build one are each closed by an exact computation (26×, no 3-bond loop, Landau pole). F144's A1 is audited step by step, with steps 1–2 verified group-blind and step 3 isolated as the break — so the *location* of the problem is no longer in dispute even though its resolution is.

**Remains — and this is now a fork, not a gap.**

1. **Branch A: F144's $0.083\%$ is a coincidence.** Then the model's bare coupling is $g_s=\sqrt3/4$, $\alpha_s(M_Z)=0.0397$, and F144's headline result, F119's 19-decade hierarchy channel and CL022's "largest open tension at $2.1\sigma$" all need rewriting — the tension would be $-66\%$, not $2.1\sigma$. **Nothing in the tree currently supports this branch except structure.**
2. **Branch B: the colour sector is genuinely not $SU(N_c)$-normalised.** Then $\chi=1$ and $g_s=\tfrac12$ stand, and the thing that must be rebuilt is the *running*: what $\beta$ function does an integer-flux/centre theory have, and does it still deliver 19 decades? The model would be a $\mathbb Z_3$ theory whose effective description is $SU(3)$, and the matching between them at $\mu_0$ — not a scheme constant, an actual matching — is the missing object. **Nothing in the tree currently supports this branch except the measurement.**
3. **What would decide it.** A one-loop background-field computation of the model action's own $\Lambda$-ratio (F144 A4 named it as "the model-action analogue of the Hasenfratz constant"). Under Branch A it must come out $\approx3.4\times10^6$; under Branch B, $\approx1.78$. Those differ by six decades, so the computation cannot be ambiguous — which makes it the single highest-value open item in the strong sector.
4. **B10's grade does not move**, and neither does CL022's status. CL022 gains a history note that its $2.1\sigma$ framing is contingent on H1; CL257 gains this finding.
