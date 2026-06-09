# F115 — Gauge coupling magnitudes $e$, $g$, $g_s$: the electroweak sector reduces to one magnitude, $g_s$ is locked by the rotor stiffness, and the +12% Weinberg gap is a low-scale matching, not a running effect

**Date:** 2026-06-08 - 14:40
**Status:** Partial — half structural reduction, half a sharp negative. 4/4 check blocks PASS (CM1 exact rationals; CM3 exact lock; CM2 a decisive numerical result; CM4 a notation no-go). Addresses audit C.5 (`project-audit-inputs-dynamism-2026-06-06.md`, open input #5) and uses F110's rotor identity.
**Script:** `model-tests/test_F115_coupling_magnitudes.py` (<0.2 s, numpy + fractions)
**Results:** `test-results/F115_coupling_magnitudes.json`
**Cross-references:** [[F45-sigma-tau-swap-weinberg-angle]] (the ratio $g'/g$ this builds on), [[F48-dynamical-Z-neutral-current]] (the +12% gap appears identically in $\sin^2\theta_W$, $m_Z/m_W$, $g_V^{e_L}$), [[F110-realtime-link-hamiltonian-confinement]] (the $\chi=1/(4g_s^2)$ rotor identity that locks $g_s$), [[F100-gamma-from-transfer-operator]]/[[F101-strong-coupling-sigma-compact-rotor]] ($\sigma_1=\tfrac14\langle1/\Omega\rangle_\text{BZ}$), [[F79-structural-newton-constant]]/[[F107-canonical-a-adoption-L4-grb-gate]] (the lattice scale $1/a=M_\text{Pl}/6.5978$), [[F95-B-derived-C-localized]] (the $E_g$ sextic $e^6\cos^23\delta$ whose "$e$" is NOT the electric charge).

---

## 1. What this addresses

Audit input #5: *"Gauge coupling magnitudes $e$, $g$, $g_s$ — free (ratio $g'/g$ derived via F45; magnitudes not); no RG running, so the +12% gap $\sin^2\theta_W=1/4$ vs PDG 0.2232 is unexplained."* This finding takes each of the three proposed avenues (C.5 items 1–3) and reports what each actually yields.

## 2. CM1 — the electroweak sector is a one-parameter family (exact)

At the bare swap angle $\sin^2\theta_W=\tfrac14$ (F45) the standard tree relations $e=g\sin\theta_W=g'\cos\theta_W$, $g_Z=g/\cos\theta_W$ collapse the three electroweak couplings onto a **single** magnitude. With $\sin\theta_W=\tfrac12$, $\cos\theta_W=\tfrac{\sqrt3}{2}$, $\tan\theta_W=\tfrac1{\sqrt3}$:

$$\boxed{\;e=\tfrac12\,g,\qquad g'=\tfrac{1}{\sqrt3}\,g,\qquad g_Z=\tfrac{2}{\sqrt3}\,g\;}$$

verified as exact rationals ($(e/g)^2=\tfrac14$, $(g'/g)^2=\tfrac13$, $(g_Z/g)^2=\tfrac43$). So the model does **not** have three free EW magnitudes — it has **one**. The geometry (F45) fixes every ratio; only the overall scale is undetermined. This is a real (if modest) reduction: open input #5 in the EW sector is *one* number, not three.

## 3. CM2 — the +12% gap is NOT a desert-running effect (decisive)

The audit's first avenue is RG running: "even a leading-log lattice computation would be decisive (it must close the same gap in all three observables simultaneously)." We implemented the one-loop running and the result is decisive — **against** the running hypothesis.

**Setup.** Boundary at the lattice (UV) scale $\mu_L=1/a=M_\text{Pl}/6.5978=1.85\times10^{18}$ GeV (F79/F107): $\sin^2\theta_W=\tfrac14$, i.e. $\alpha_1^{-1}:\alpha_2^{-1}=9:20$ in GUT normalization. One free magnitude, fixed by matching $\alpha_\text{em}(M_Z)^{-1}=127.95$. Run down with the one-loop SM RGEs (and the Higgs-free, 3-generation variant the model actually has: $b_1=4$, $b_2=-\tfrac{10}{3}$, $b_3=-7$).

**Result (negative).** Running the bare angle from the Planck scale **overshoots catastrophically**: $\sin^2\theta_W(M_Z)\to0.059$ (SM) / $0.055$ (Higgs-free) — a $-74\%$ miss, not the $+12\%$ gap. $\alpha_s(M_Z)$ comes out negative (the SU(2)/SU(3) couplings cross a Landau pole). The reason is structural: on the SM trajectory $\sin^2\theta_W$ *increases* with scale toward the SU(5) value $3/8=0.375$ at $\sim10^{16}$ GeV and beyond, so at the Planck scale the SM wants $\sin^2\theta_W>3/8$, far **above** the lattice's $1/4$. Running the bare angle the GUT way makes the disagreement worse, not better.

**The honest positive (CM2b).** Asking instead at what scale the *measured* SM trajectory passes through $\sin^2\theta_W=\tfrac14$ — running up from the $M_Z$ data, no Planck anchor — gives

$$\mu_\star \approx 3.7\ \text{TeV (SM)},\qquad 3.4\ \text{TeV (Higgs-free)},$$

and at $\mu_\star$ all three observables coincide with the bare values simultaneously and exactly (they are algebraically locked): $\sin^2\theta_W=0.2500$, $m_Z/m_W=2/\sqrt3=1.1547$, $g_V^{e_L}=0$. So the "one number in three observables" cross-check the audit demanded is automatically satisfied at a single matching scale.

**Verdict.** The +12% gap ($0.25$ vs $0.2232$) is far too small to be 16 decades of running — it is a **low-scale ($\sim$ few-TeV) matching offset**, not a desert effect. The bare swap value is best read as the tree value the running curve passes through near a few TeV, *not* a Planck-scale boundary condition that then runs down. This neither derives the EW magnitude nor closes the gap by running; it falsifies the running explanation and relocates the gap to a TeV matching. The EW magnitude (equivalently $\alpha$) remains the one genuine input — consistent with the audit's option (a), "treat $\alpha$ as the second external ruler alongside $a$."

## 4. CM3 — $g_s$ is locked by the rotor stiffness (the internal route)

The audit's second avenue: the confinement chain (F100/F101/F110) ties $\sigma$ and the dispersion to one operator; matching fixes the bare colour coupling internally. F110 proved, as a **matrix identity** (its check C7), that the Kogut–Susskind link Hamiltonian's electric stiffness is

$$\chi=\frac{1}{4g_s^2}.$$

The QCA rule's $(\mathbf E,\mathbf B)$ rotation is the *symmetric* rotation, normalised to $\chi=1$ (F101 §7). Therefore the rule **locks the combination**

$$\boxed{\;g_s^2\,\chi=\tfrac14\;\Longrightarrow\;g_s=\tfrac12\ \ (\chi=1,\ \text{bare lattice})\;}$$

$g_s$ is **not an independent input**: once the rule sets the magnetic/electric stiffness of the plaquette rotor, the strong coupling is fixed. The cross-check is F100's $\sigma_1=\tfrac14\langle1/\Omega\rangle_\text{BZ}=0.2015$ (2D): because the rule's rotation rate $\Omega(k)$ is fixed, the lattice string tension in lattice units is a **pure number** with no free $g_s$ in it. The magnitude problem for $g_s$ is therefore solved at the lattice (bare) level in the same sense the ratios are for EW — the rule fixes it.

**Scope.** $g_s=\tfrac12$ is the *Hamiltonian-lattice* coupling in the rule's stiffness normalisation, not continuum $\alpha_s(M_Z)$. Translating to $\alpha_s(M_Z)$ requires lattice$\to$continuum scale-setting via the physical string tension (F94's Monte-Carlo $\sigma$), which carries its own ruler — the same one ruler as $a$. The structural content is that $g_s$ is removed as an *independent* knob, not that $\alpha_s(M_Z)$ is predicted without a ruler.

## 5. CM4 — the electric charge magnitude: a notation no-go

The audit's third avenue (C.5 item 3b): "whether the F87 charge-linearity + paired-photon normalization plus the F95 sextic's $e^6$ appearance over-determines $e$." It does not. The "$e$" in F95's sextic $e^6\cos^23\delta$ is the **second-shell $E_g$ condensate order-parameter amplitude** (a generation-space quantity, F93/F95/F108), **not** the electromagnetic coupling. The two are unrelated by anything established in the model; identifying them would be an unjustified notation collision. The honest conclusion stands: the electric charge magnitude $e$ has **no internal route** and remains the irreducible electroweak input (equivalently $\alpha_\text{em}$, the "second ruler" of audit C.1/C.5).

## 6. Net effect on the open ledger

| Coupling | Before | After F115 |
|---|---|---|
| $g'/g$ ratio | derived (F45) | unchanged |
| $e,g,g',g_Z$ magnitudes (EW) | "three free" | **one** free magnitude ($\equiv\alpha_\text{em}$); $e=g/2$, etc. (CM1) |
| +12% $\sin^2\theta_W$ gap | "assigned to running" | **not** running (overshoots); a few-TeV matching offset (CM2) |
| $g_s$ magnitude | free | **locked** by the rotor: $g_s^2\chi=\tfrac14$ (CM3) |
| $e$ (electric charge) | free | irreducible input; F95 $e^6$ is a *different* $e$ (CM4) |

Open input #5 is sharpened, not eliminated: the electroweak sector now carries exactly **one** undetermined magnitude (the fine-structure constant / the "second ruler"), $g_s$ is internally fixed at the lattice scale, and the Weinberg gap is reattributed from running to a TeV-scale matching.

## 7. Check summary (4/4)

| Check | Statement | Tier | Result |
|---|---|---|---|
| CM1 | $e=g/2$, $g'=g/\sqrt3$, $g_Z=2g/\sqrt3$ at $\sin^2\theta_W=\tfrac14$; one EW magnitude | exact (rationals) | PASS |
| CM2 | Planck-scale running overshoots ($\to0.059$); measured trajectory hits $1/4$ at $\sim$3.7 TeV | numeric (decisive) | PASS |
| CM3 | $g_s^2\chi=\tfrac14$ from F110 $\chi=1/(4g_s^2)$ + rule $\chi=1$ → $g_s=\tfrac12$ bare | exact | PASS |
| CM4 | F95 $e^6\cos^23\delta$ "$e$" is the $E_g$ amplitude, not electric charge — no over-determination | identification | PASS (no-go) |

## 8. Honest scope

- CM2 is one-loop and uses the standard SM (and Higgs-free) $b_i$; two-loop and threshold effects shift $\mu_\star$ by $O(1)$ but not the qualitative verdict (Planck running overshoots; the gap is small and low-scale). The Higgs-free $b_i$ are the model-correct content; both variants give the same conclusion.
- CM3's $g_s=\tfrac12$ is convention-locked to $\chi=1$; the invariant statement is the *combination* $g_s^2\chi=\tfrac14$ removing the independent knob. Continuum $\alpha_s(M_Z)$ still needs the F94 ruler.
- The EW magnitude and the electric charge $e$ remain genuine inputs; this finding reduces their *count* (3→1 in EW) and *reattributes* the Weinberg gap, but does not conjure $\alpha$ from structure.

## 9. Provenance

- New content: the one-magnitude EW reduction (CM1), the Planck-vs-TeV running computation and the few-TeV crossing (CM2/CM2b), the $g_s$ rotor lock $g_s^2\chi=\tfrac14$ (CM3), and the $e^6$-notation no-go (CM4).
- Reused: F45 ratio, F48 three-observable lock, F110 C7 matrix identity, F100/F101 $\sigma_1$, F79/F107 lattice scale, F95 sextic.
- Verification: `model-tests/test_F115_coupling_magnitudes.py` (2026-06-08, 4/4 PASS), results `test-results/F115_coupling_magnitudes.json`.
