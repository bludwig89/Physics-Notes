# Chapter 22 — The Dark Sector

*Chapter 22 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F191-dark-matter-rotation-curves-bullet.md`, `findings/F194-emergent-gravity-bullet-falsification.md`,
`findings/F197-first-excitation-dark-source.md`, `findings/F198-angular-mode-relic-misalignment.md`,
`findings/F199b-amplitude-mode-stability-nogo.md`, `findings/F203-dark-sector-falsifiability-battery.md`,
`findings/F205-sterile-qke-boltzmann-margins.md`, `findings/F216-massive-spin2-dark-mode.md`,
`findings/F223-spin2-bound-state-binding-and-relic.md`, `findings/F228-geon-production-and-stability.md`,
`findings/F237-kev-sterile-resolution.md`, `findings/F238-geon-relic-abundance.md`,
`findings/F358-bullet-cluster-reexamination.md`, `findings/F365-geon-relic-gw-bounds-sharpen-k7.md`,
`findings/F366-geon-domain-wall-reopening.md` (the fifteen findings `00-plan.md` §2 assigns to this
chapter, all read in full). Checked against `docs/theory/supersessions.yaml`: record **S23**
(`S23-F194-bullet-cluster-clump-shape-claim`) is the one hit — F194 is superseded *in one sentence
only* by F358, not in its conclusion; see §22.3.1/§22.3.2 for the precise scope, taken directly from
S23's own `retained:`/`dead:` fields, not paraphrased. No other of this chapter's fifteen findings
appears in any `superseded:` list. Checked against `claims-index.md`: **CL166** (F191, `no_go`/`live`),
**CL168** (F194 **and** F358, `no_go`/`live`, `falsifier: stated` — the falsifier field F358 itself
filled in), **CL170/CL171** (F197/F198, `no_go`/`derivation`, both `open`), **CL173** (F199b,
`derivation`/`open`), **CL179** (F205, `no_go`/`open`, `quantitative`), **CL208** (F237, `no_go`/`open`),
**CL190** (F216, `prediction`/`open`), **CL197** (F223, `no_go`/`open`), **CL202** (F228, `no_go`/`open`),
**CL209** (F238, `no_go`/`open`, `quantitative`), **CL301** (F365, `prediction`/`open`, `bracketed`),
**CL302** (F366, `non_claim`/`open`, rolls up to CL209), **CL177** (F203, `no_go`/`open`,
`review_state: unreviewed-seed` — flagged as stale bookkeeping in §22.7, not treated as an
independent confirmation of F203's content). Notation and results are those of Chapters 1, 16, 18,
19, 20 and 21 (`01-postulates-and-ontology.md`, `16-neutrinos.md`, `18-gravity.md`,
`19-strong-field-and-wave-gravity.md`, `20-cosmology.md`, `21-cosmological-constant.md`) — $\nu_R$,
$M_R$, $K$, $G$, $M_\text{Pl}$, $a$, $\ell_P$, $\Omega_m$, $\Omega_\Lambda$, $z_\text{eq}$ — extended,
never redefined.*

## 22.0 What this chapter establishes

This chapter's central, unifying honesty point is stated up front rather than discovered at the
end: **the model has two structurally-motivated dark-matter candidates — a keV-scale sterile
right-handed neutrino ($\nu_R$, Chapter 16) and a Planck-mass graviton–graviton bound state ("the
geon," a black-hole remnant) — and *neither* has a derived relic abundance.** The sterile
neutrino's abundance depends on an unfixed lepton asymmetry and entropy-dilution history; the
geon's abundance depends on an unfixed primordial-black-hole formation fraction that traces back,
provably, to a primordial curvature spectrum the model has no sector to generate (Chapter 20's
inflaton no-go, F282, is the reason why). This is not a symmetric embarrassment: by the end of this
chapter the two candidates are *not* on equal footing. The keV sterile is mechanism-level
**excluded** as the sole (100%) dark-matter component (F237); the geon is the model's *only*
surviving 100%-dark-matter identity, cold and collisionless by construction, checked against every
kinematic screen the field uses, and *bounded* — though not fixed — by two independent 2025
gravitational-wave literature results (F365). The sterile neutrino survives only as a genuine,
falsifiable **sub-dominant** relic. A structurally distinct, non-inflationary production channel for
the geon (domain-wall collapse sourced by the model's own already-derived lepton-condensate
potential) is shown to be open in principle but not derived (F366). The chapter also revisits, and
precisely re-scopes, the one purely gravitational alternative to a dark *particle* — modified/
emergent gravity — which the Bullet Cluster excludes (F191/F194), with a 2026 literature
re-examination (F358) narrowing exactly one oversold sentence in that exclusion without touching
its verdict. A dedicated attempt to source both dark matter *and* dark energy from a single
near-vacuum lepton-condensate excitation is built and closed on two independent legs (F197/F198/
F199b). The chapter closes with the model's own falsifiability battery (F203), read against the
sharper computations (F205, F237, F228/F238, F365) that postdate it.

## 22.1 Inputs

**Postulates used.** **P4** (the per-cell state is a genuinely quantum, unitary object — the geon's
existence as a *bound state* of gravitons and the sterile neutrino's Majorana mass both rest on the
same quantized substrate) and **P6** (mass and hypercharge from the chiral $SU(2)$ connection $U(x)$
— the reason $\nu_R$ is a total gauge singlet at all, Chapter 16) are the two postulates this
chapter's constructions ultimately rest on (`01-postulates-and-ontology.md` §1.2). Neither is
re-argued here.

**Prior results used.**
- **Chapter 16 (R16.13, R16.14):** the keV-sterile texture's structural mechanism (a $\mathbb Z_3$
  cancellation node makes one $\nu_R$ eigenvalue parametrically light — F201) and its cosmological
  stability at viable mixing (F266) are the starting point for Group C below; Chapter 16's own
  text explicitly defers "the dark-matter candidate... both forward-cited to Chapter 22 for what
  belongs there instead" (§16.0) and states plainly that F266's falsifiability battery is "Chapter
  22's territory" (§16.7).
- **Chapter 18/19 (R18.13, R19.1, R19.6, R19.16–R19.17):** the induced Einstein equation with exact
  GR and constant $G$ (F178, the reason a purely gravitational "dark matter without dark matter"
  route is even a coherent question to ask — §22.3), the massless, luminal, non-birefringent
  transverse-traceless graviton with zero tree stiffness (F79/F180, the reason the *metric*
  graviton cannot itself be dark matter — Group D below), the exact Schwarzschild/Kerr black hole
  and its Hawking evaporation law $\tau\propto M^3$ (F183, the geon's eventual identity as a
  black-hole remnant), and the graviton/photon band-top and Planck-scale collision threshold
  (F357/F359, the wider gravitational-wave context F365 draws on).
- **Chapter 21 (R21.4, R21.6):** the F190 per-cell horizon-entropy coefficient $2\pi\sqrt3$ nats,
  used unmodified here to fix the geon's stable one-cell remnant mass (F228); Chapter 21's own
  disclosed open tension over *deriving* that coefficient from first principles (R21.6) is inherited,
  not resolved, by this chapter's use of it.
- **Chapter 20 (R20.2, R20.6–R20.7, R21.5's handoff):** the confirmed $\Lambda$CDM background
  ($z_\text{eq}=3433$, age $13.79$ Gyr, F182/F188) that every dark-matter candidate here must fit
  inside without disturbing, and — decisively for Group D — the proof that **no slow-roll inflaton
  field can exist on this lattice** (F282, R20.6) and that no principled initial-condition measure
  reproduces the observed spectral tilt (F285, R20.8). These two results are what force the geon's
  abundance question to terminate in "the model has no primordial-spectrum sector," rather than
  merely "no one has built one yet" (§22.5).

**Free inputs consumed, stated plainly.** **The relic abundance of *either* surviving dark-matter
candidate is a free input.** For the sterile neutrino this is the lepton asymmetry $L$ and any
post-production entropy-dilution factor $S$ (F205, F237). For the geon it is the primordial-black-
hole formation fraction $\beta(M_\text{form})$, which F238 proves traces to a primordial curvature
amplitude $\sigma(k_\text{PBH})$ the model has no sector to fix (§22.5). Both inputs are declared,
not hidden inside a fitted parameter.

## 22.2 The derivation

### Group A — Is gravity itself (without new particles) the dark-matter answer?

#### 22.2.1 F191 — rotation curves cannot decide; the Bullet Cluster can

Under Chapter 18's F178 adoption (exact GR, constant $G$), F191 builds the honest baseline
discriminator the rest of this chapter answers. A toy exponential-disk galaxy falls to
$v_{30\text{kpc}}/v_\text{max}=0.58$ on baryons alone; **both** an NFW collisionless dark halo and a
MOND-type modified-gravity reweighting flatten the curve to $>0.85$ — rotation curves alone cannot
distinguish a dark *source* from modified *gravity* (check D1). The discriminator is the Bullet
Cluster: a toy two-Gaussian cluster collision shows the collisional gas (X-ray) piling at the
centre while the collisionless mass passes through, producing a lensing (total-mass) peak offset
$0.34$ Mpc from the gas peak (check D2). Under exact GR with constant $G$, visible matter alone is
insufficient (check D3): **a dark gravitating source is required.**

$$\boxed{\;\text{rotation curves: NFW halo and MOND-type modified gravity both flatten to}>0.85\text{, indistinguishable; Bullet Cluster lensing/gas offset}=0.34\text{ Mpc (toy) breaks the degeneracy; under exact GR+constant }G\text{, a dark SOURCE is required}\;}\tag{R22.1}$$

(F191, checks D1–D3, 3/3 PASS; CL166, `no_go`, `live`.)

#### 22.2.2 F194/F358 — the model-native emergent-gravity route: falsified, then precisely re-scoped

F194 builds the one gravity-*side* candidate the catalog left open: because $G$ is *induced*
(Sakharov, $G=a^2c^3/8\pi\sqrt3\hbar$, F79), it could in principle be IR-enhanced at very low
accelerations, mimicking a dark halo with no new matter — the model-native cousin of Verlinde's
emergent gravity / QUMOND. The acceleration scale is not free: it is set by the model's own
vacuum/de Sitter sector (F164/F192), giving $a_0^\text{model}=1.16\times10^{-10}\ \text{m/s}^2$
against the empirical $1.2\times10^{-10}\ \text{m/s}^2$ (ratio $0.97$, check E1) — an appealing
coincidence tying the dark-energy and MOND acceleration scales to one number. From baryons alone
this reproduces a flat rotation curve (flatness $0.99$) and the baryonic Tully–Fisher relation
(ratio $1.0$, check E2), so it is a genuine dark-matter mimic at galaxy scales, not a strawman.

The falsifier is the Bullet Cluster. Because the QUMOND phantom density
$\rho_\text{dyn}=-\tfrac{1}{4\pi G}\nabla\!\cdot\!(\nu(|g_N|/a_0)g_N)$ is a **local functional of the
baryons**, and the toy cluster's baryons are dominated 6:1 by the X-ray gas, emergent gravity
predicts the lensing peak *on the gas* (offset $0.000$ Mpc). The observed peak sits on the
collisionless galaxies, $0.189$ Mpc away (Clowe et al. 2006, $8\sigma$); $\Lambda$CDM (a real
collisionless dark source) reproduces the observed offset ($0.343$ Mpc peak, matching the direction
of the discrepancy). **The model-native emergent-gravity route mispredicts the lensing-mass
location by the full galaxy–gas separation and is falsified** (checks E3–E5, 5/5 PASS).

**The precise partial supersession (S23, F358).** F194's own text went one sentence further than
its calculation supports, asserting the phantom-density peak "can never migrate to the offset
galaxies... **regardless of** $a_0$, the interpolation function, **or the clump shapes**" — framed
as a strict, geometry-independent topological impossibility. A 2026 literature re-examination
(F358) finds this specific framing does not survive: Hernandez (arXiv:2604.10811, 2026-04-12) shows
that because the QUMOND phantom density is the divergence of a nonlinear vector field, the
*compactness* of galaxy clumps versus diffuse gas can pull a disproportionate share (Hernandez's
own figure: "almost half") of the phantom-density signal toward the galaxies despite the galaxies
holding roughly a tenth of the baryonic mass — clump shape is exactly the lever F194 claimed was
irrelevant. This is a **real, published counterexample** to the strict sentence, not a re-reading of
F194's own toy model (which used smooth, roughly Gaussian clumps and never explored the compact
regime that produces the effect).

What does **not** move: F358 goes on to check the *quantitative* re-adjudication of the same
mechanism, done independently by a rival MOND specialist (Famaey, arXiv:2605.10022, 2026-05-11)
against the sharpest available (JWST-refined) lensing map, and finds it falls short by
$\kappa\sim0.5$ against an observed $\kappa\gtrsim1$ even after doubling assumed galaxy masses —
requiring a residual $\sim3.4\times10^{14}M_\odot$ of additional, mostly collisionless mass. A third
2026 paper's proposed closing move (Zhang et al., *Phys. Rev. D*, arXiv:2606.19454 — an
extrapolated, top-heavy stellar-remnant baryon budget) is independently disputed by named external
reviewers (Massey, Romer) as unverified. Per S23's own `retained:` field: **"EVERYTHING F194
CONCLUDES... the bottom-line verdict — the model-native emergent-gravity route is falsified and a
dark, collisionless gravitating source is required — is RETAINED IN FULL and is independently
reinforced"** by this same 2026 dispute reaching the identical bottom line by an outside route. Only
the single "regardless of clump shape" sentence is withdrawn (S23 `dead:` field); the finding's own
five checks (E1–E5) are untouched and the test file is marked `live`, not to be re-attacked.

$$\boxed{\;\text{model-native emergent gravity: FALSIFIED by the Bullet Cluster (lensing on gas, predicted; on galaxies, observed — full }0.19\text{ Mpc miss); the strict "regardless of clump shape" sentence is WITHDRAWN (S23}\to\text{F358) — a real 2026 counterexample exists — but the bottom-line dark-source requirement is RETAINED and independently reinforced by the same 2026 literature dispute's own outside adjudication}\;}\tag{R22.2}$$

(F194, checks E1–E5, 5/5 PASS; F358, analysis-only, no test record; CL168, `no_go`, `live`,
`falsifier: stated` — the falsifier F358 itself names: an independently-verified baryon-only
QUMOND/MOND match to the *full* $\kappa$ profile, not just the offset centroid, none surviving
scrutiny as of 2026-09.)

### Group B — The $E_g$ first-excitation attempt: a unified dark sector from the lepton condensate, closed on two legs

#### 22.2.3 F197 — the discriminator: a gapped branch is necessary, and the $E_g$ condensate has one

With Group A closed, the dark-matter question moves from "is gravity itself enough" to "what,
model-natively, could the dark *source* be." F197 builds the general discriminator: the equation of
state $w=p/\rho$ is fixed by *what kind* of excitation above vacuum a candidate is — a homogeneous
condensate VEV sits at $w=-1$ (dark energy, smooth); a **gapped** massive mode with velocity
dispersion $\sigma$ gives $w=\tfrac13(\sigma/c)^2\to0$ (cold dark matter, clustering); a **gapless**
mode gives $w=\tfrac13$ (radiation, neither). So a near-vacuum channel can be a *unified* dark
sector — both the Chapter 21 dark-energy residual and galactic dark matter — **iff it has a gapped
branch above its own vacuum.**

The Chapter 15 $E_g$ second-shell lepton-mass condensate (F93) qualifies: its Landau energy has
**two** gapped fluctuation modes at the minimum — a heavy amplitude (breathing) mode and a lighter
angular (phase) mode pinned by the small IR sextic $\lambda_6$ (mass ratio $0.34$, Chapter 15's own
architecture, F150/F154). The F69 paired-spinor photon channel (Chapter 8), by contrast, is
massless and marginally bound — gapless, hence excluded as a cold relic (it is radiation, and it
couples electromagnetically, hence collisional). Using the F106/F178 weak-field law
$\nabla^2\ln K=-\kappa T^{00}$, a homogeneous excitation is **non-normalizable** ($\ln K\to-\infty$
as $r^2$ — no local halo, only the Friedmann mode), while a localized gapped-mode clump is
normalizable and flattens a toy rotation curve to $0.93$ — the same field is dark energy in its
homogeneous mode and dark matter in its localized overdensity, purely as a consequence of
normalizability, not an assumption.

$$\boxed{\;\text{clustering dark matter} \Leftrightarrow \text{a gapped branch exists (kinematic, exact); the }E_g\text{ condensate has two gapped modes (angular }+\text{ amplitude), the F69 photon channel is gapless and excluded; homogeneous piece non-normalizable, localized clump normalizable + flattens a toy curve to }0.93 \;}\tag{R22.3}$$

(F197, checks E1–E5, 5/5 PASS; CL170, `no_go`, `open`. **Named obstruction:** the relic abundance
$\Omega_\text{DM}\approx0.26$ is not derived — the next two findings compute it and close it
negatively.)

#### 22.2.4 F198 — the angular mode under-produces by ~15 orders

F197 tentatively flagged the light angular mode (axion-like, mass set by $\lambda_6$) as the natural
candidate. F198 runs the standard vacuum-misalignment relic calculation and finds it fails badly.
The misalignment relic scales as $\Omega_a h^2\propto m_a^{1/2}f^2\theta_i^2$ with $f$ the
condensate's own decay-constant scale. The $E_g$ condensate's natural scale is the Chapter 15/12
Stueckelberg value $f\simeq v/2=123$ GeV — far below the $f\sim10^{13}$–$10^{16}$ GeV an axion-like
particle at any reasonable mass would need to reach $\Omega_\text{DM}$. Concretely, at the
representative light-mode mass ($\lambda_6=0.05$, $m_a\approx27$ MeV) the misalignment relic gives
$\Omega h^2=6.9\times10^{-17}$ — **under-producing by $1.8\times10^{15}$**, roughly fifteen orders
of magnitude. The other gapped mode of the same condensate — the heavy amplitude scalar — does not
misalign; it thermally freezes out, and with electroweak-strength coupling lands *near* the WIMP
window ($\Omega h^2\approx0.14$ at $m_\chi=3$ TeV, $g=1.0$), reversing F197's tentative
identification: if the $E_g$ sector is dark matter at all, it is the heavy amplitude mode via
freeze-out, not the light angular mode via misalignment.

$$\boxed{\;\text{light angular mode (misalignment): under-produces }\Omega_\text{DM}\text{ by}\sim1.8\times10^{15}\text{ (}\sim15\text{ orders) because the condensate's natural decay constant }f\simeq v/2=123\text{ GeV is}\sim10^{11}\times\text{too low; heavy amplitude mode (freeze-out) reaches the WIMP window at TeV scale — the candidate flips from angular to amplitude}\;}\tag{R22.4}$$

(F198, checks E1–E5, 5/5 PASS; CL171, `derivation`, `open`.)

#### 22.2.5 F199b — the amplitude mode fails first on stability, not abundance

The obvious next step — work out the amplitude mode's actual mass and couplings from F73/F93 and
see whether $\Omega_\text{DM}=0.26$ falls out — does not get that far. F199b separates two objects
F197/F198 had conflated as "the amplitude mode": Mode 1, the *electroweak* radial mode of the
symmetry-breaking condensate, is the observed 125 GeV Higgs (F73) — decays, seen at the LHC, not
dark matter, by direct observation. Mode 2, the *$E_g$ second-shell* amplitude mode F197/F198
actually meant, is the radial fluctuation of the condensate that Chapter 15's F93 O1 establishes
**is** the crystal field setting the charged-lepton mass hierarchy — so a fluctuation of its
amplitude couples linearly to the lepton mass operator, $g_\ell=m_\ell/f$, by the same mechanism
that gives leptons their masses in the first place. This coupling is not small: across the entire
EW–TeV mass range the resulting decay width gives a lifetime $\tau\sim10^{-21}$–$10^{-23}$ s — **38
to 40 orders of magnitude below cosmological time** ($t_0\approx4.4\times10^{17}$ s). A thermal
relic must be cosmologically stable; this one decays essentially instantaneously.

**Stability fails before abundance is ever reached — the F198 freeze-out window is moot**, because
the relic abundance is undefined for a state that decays before nucleosynthesis. The obstruction is
relocated from "how much is produced" to "what forbids the decay at all": a stable relic needs a
conserved charge under which it is the lightest carrier, and the $E_g$ condensate's amplitude mode
has none — it is even under the residual $D_{2h}$ stabilizer and couples linearly to leptons, with
nothing forbidding $S\to\ell\bar\ell$. This closes Group B as a genuine, two-legged negative result:
the angular mode fails on abundance (F198), the amplitude mode fails on stability before abundance
is even asked (F199b) — and the same finding that closes the route promotes the "sterile-sector
excitation" hint of F191 to the leading direction, handing off directly to Group C.

$$\boxed{\;E_g\text{ amplitude mode couples to leptons as }g_\ell=m_\ell/f\text{ (its defining lepton-mass role); lifetime}\sim10^{-21}\text{ s across EW–TeV, 38–40 orders below cosmological}\Rightarrow\text{no stable relic exists; }\Omega_\text{DM}=0.26\text{ is moot, not merely unfitted — the obstruction relocates to a missing conserved charge}\;}\tag{R22.5}$$

(F199b, checks (5/5) PASS; CL173, `derivation`, `open`. **Group B verdict: closed, honestly
failed, on two independent legs** — angular-mode abundance (F198) and amplitude-mode stability
(F199b) — neither rescuable by adjusting the condensate's own parameters, since both obstructions
are set by scales (the Stueckelberg $f\simeq v/2$; the lepton-mass Yukawa coupling itself) the
condensate is defined by, not free to retune without ceasing to be the object that sets lepton
masses.)

### Group C — The sterile-neutrino candidate, continuing from Chapter 16

#### 22.2.6 F205 — the full Boltzmann computation: quantified, real pressure

Chapter 16 (F201, R16.13) supplied the structural mechanism (a $\mathbb Z_3$ cancellation node makes
one $\nu_R$ eigenvalue parametrically light) and (F266, R16.14) the identity and cosmological
stability of a keV-scale sterile neutrino at viable mixing, explicitly deferring the abundance
computation and observational status to this chapter. F205 builds the full momentum-resolved
quantum-kinetic (Boltzmann) production calculation — non-resonant Dodelson–Widrow and resonant
Shi–Fuller (via a lepton asymmetry $L$) active$\to$sterile oscillation, damped by collisions, with
free-streaming mapped to a thermal-equivalent WDM mass via the standard Viel relation.

For the non-resonant channel, matching $\Omega_\text{DM}$ at $m_s=7.1$ keV needs
$\sin^22\theta_\text{DW}=6.1\times10^{-9}$ (matching the literature to within the known factor-2 QCD
normalization) — **2.55 dex above** the aggregate current X-ray line bound
($\sim1.7\times10^{-11}$): non-resonant production is X-ray excluded. Resonant production, driven
by a lepton asymmetry, can reach $\Omega_\text{DM}$ at mixing up to $\sim580\times$ smaller,
clearing the X-ray bound for $L\gtrsim2\times10^{-3}$ — but in the fixed-$L$ pass, the X-ray-allowed
point is *warm* ($\langle\varepsilon\rangle\approx3.0$) and the coldest spectrum
($\langle\varepsilon\rangle=1.57$) requires X-ray-*excluded* mixing: the two regimes do not
coincide, precisely the known "7.1 keV sterile at the edge" tension. Mapping the frozen spectrum to
a Lyman-$\alpha$ mass floor gives $\sim41$ keV for the non-resonant channel and $\sim9$–$15$ keV
for the coldest achievable resonant spectrum. **The model's 5.6 keV (F201) and the 7.1 keV
$\nu$MSM benchmark sit below every one of these floors.**

$$\boxed{\;\text{non-resonant DW: X-ray excluded by 2.55 dex; resonant Shi–Fuller reaches }\Omega_\text{DM}\text{ at X-ray-allowed mixing only for a WARM spectrum; coldest-resonant + conservative Lyman-}\alpha\text{ floor}=9\text{–}15\text{ keV }>\text{ model's 5.6–7.1 keV}\;}\tag{R22.6}$$

(F205, checks V1–V8, 8/8 PASS; CL179, `no_go`, `open`, `quantitative`. Narrows F203 T1/T2 from
order-of-magnitude to computed, without relieving the pressure — see §22.7.)

#### 22.2.7 F237 — clean exclusion as 100% dark matter; hand-off to the geon

F205 left one open door: could the full lepton-number-*depleted* quantum-kinetic evolution thread
the cold-and-X-ray-allowed corner the fixed-$L$ pass forbids? F237 attacks that door with the
standard additional lever it omitted — **post-production entropy dilution** from a late-decaying
heavy species (the GeV-scale $N_{2,3}$ steriles of the same F201 texture, decaying after keV-sterile
freeze-in but before BBN). Entropy dilution by a factor $S$ pulls in *opposite* directions: the
mixing needed to reach $\Omega_\text{DM}$ after dilution scales as $\sin^22\theta_\text{needed}
\propto S$ (X-ray line rate — worse), while the effective frozen momentum cools as
$\langle\varepsilon\rangle_\text{eff}\propto S^{-1/3}$, so the Lyman-$\alpha$ floor improves as
$m_\text{floor}\propto S^{-4/9}$ (better). These are **verified exact rational exponents** ($+1$ and
$-\tfrac49$ in $\log S$), not fitted slopes.

Because the exponents have opposite sign, **no value of $S$ improves both constraints
simultaneously.** A full $(L,S)$ grid of 154 points clears neither window at either 5.6 or 7.1 keV.
Even the most generous possible assumption — that a full $L$-depletion QKE could place the coldest
achievable spectrum exactly at the X-ray-allowed mixing (a corner the fixed-$L$ computation
forbids) — still needs $S\approx6$–$10$ to pass Lyman-$\alpha$, which costs $+0.8$ to $+1.0$ dex
*over* the X-ray bound by the dilution's own X-ray-worsening exponent. **The door F205 left open is
closed even under the most model-favourable assumption.**

**The keV sterile is therefore excluded as 100% dark matter through the entire resonant +
entropy-dilution production space, a mechanism-level exclusion (opposite-sign scaling exponents),
not a grid artifact.** The dark-matter identity migrates explicitly: F237 hands off 100%-DM to the
graviton–graviton geon (Group D, already closed by the time F237 was written), while the keV
sterile survives as a genuine, bounded **sub-dominant** component — the F47/F200/F201 singlet still
exists, is still long-lived, and is still produced; it simply cannot be *all* of dark matter. A
future sub-critical X-ray line at $m_s/2$ would be direct confirmation of that surviving
sub-dominant role.

$$\boxed{\;\text{X-ray margin worsens as }S^{+1}\text{, Lyman-}\alpha\text{ floor improves only as }S^{-4/9}\text{: opposite signs}\Rightarrow\text{no }S\text{ co-satisfies both; 0/154 grid points viable at 5.6 or 7.1 keV; best-case door-closed at }+0.8\text{–}1.0\text{ dex; keV sterile EXCLUDED as 100\% DM; hands off to the geon; survives as a bounded sub-dominant relic}\;}\tag{R22.7}$$

(F237, checks (7/7) PASS; CL208, `no_go`, `open`. **This is the chapter's decisive result for
Group C**: the sterile neutrino's *identity* question — Chapter 16's open item — is now answered
in full: real, stable, produced, but not the whole of dark matter.)

### Group D — The geon: a graviton–graviton bound state

#### 22.2.8 F216 — the metric graviton stays massless; a massive spin-2 must be a bound state

Chapter 18/19 established the emergent metric graviton as an exactly massless (2 helicity dof:
$h_+,h_\times$), luminal, non-birefringent transverse-traceless mode, sharing the single lattice
light cone $c_\text{lat}=1/\sqrt3$ with the photon (F79/F180). F216 asks whether the induced gravity
sector nonetheless admits (a) a native massive bound mode or (b) a second propagating polarization
branch, and finds **no** on both counts, by two independent exact arguments: because $K$ carries
zero tree stiffness (source-free Maxwell is conformally invariant, F79), the graviton's entire
inverse propagator *is* the one-loop induced self-energy, which F180 already showed depends on
external momentum only through $\Pi(q)\propto Q^2\equiv c_\text{lat}^2|\mathbf q|^2-q_0^2$, vanishing
exactly at $q=0$ — a mass would require $\Pi(0)\neq0$ (transversality, exact). Separately, no local
diffeomorphism-invariant graviton mass exists, so any candidate mass must come from diff-breaking
lattice operators, which the Chapter 18/19 block-spin RG (F130) drives to zero as an irrelevant
operator ($\lambda_n=b^{-n}$, a factor $7.5\times10^{-37}$ over 60 coarse-graining steps).

The negative result has a constructive corollary: a massive spin-2 must therefore be a **composite
bound state** of gauge-neutral constituents — the model supplies exactly two candidates, the sterile
$\nu_R$ (total SM singlet) or the graviton itself (a spin-2 "gravball" of two gravitons). Weinberg–
Witten forbids only a massless composite spin-2 with a Lorentz-covariant conserved current; a
massive composite is allowed. Such an object carries 5 polarizations ($h=\pm2,\pm1,0$; the
helicity-0 mode is exactly the $\tfrac12\ln K$ conformal breathing mode F79 already identified) and,
because gravity is still mediated by the massless metric graviton, there is **no vDVZ discontinuity
and no fifth force**: the massive spin-2 would be dark *matter*, not modified *gravity* — clearing
the same hurdle that killed Group A. Its kinematic screens (cold equation of state at low $k$,
purely gravitational coupling, self-interaction $\sigma/m\lesssim10^{-66}\,\text{cm}^2/\text{g}$)
all pass, satisfying the Bullet-Cluster dark-source requirement that Group A failed.

$$\boxed{\;\text{metric graviton: exactly massless (UV transversality }\Pi(0)=0\text{, exact) and no propagating second branch (IR block-spin irrelevance, }\lambda_n=b^{-n}\text{); a massive spin-2 must be a bound state of gauge-neutral constituents (}\nu_R\nu_R\text{ or graviton–graviton), coupling gravitationally only, no vDVZ/fifth force, passing every collisionless-DM screen}\;}\tag{R22.8}$$

(F216, checks A1–A2/B1–B2/C1–C3, 7/7 PASS; CL190, `prediction`, `open`. **Named obstruction:** does
it actually bind, at what mass, and with what abundance — closed in sequence by the next two
findings.)

#### 22.2.9 F223 — the graviton–graviton geon binds at the Planckian virial mass; the $\nu_R\nu_R$ channel is a clean no-go

The two-body gravitational potential between any two constituents of mass $m$ is not posited: it is
the linearisation of the same induced Einstein–Hilbert action fixing $G$ (F79/F178/F180),
$V(r)=-Gm^2/r$, giving a gravitational "fine structure constant" $\alpha_g=(m/M_\text{Pl})^2$. A pure
$1/r$ potential **always** admits bound states at every angular momentum; the lowest $J=2$
(D-wave) level appears at principal quantum number $n=L+1=3$. Solving the radial equation with a
hand-rolled real tridiagonal solver reproduces the analytic Coulomb spectrum
$E_3=-m_\text{red}\alpha_g^2/18$ to $1.3\times10^{-5}$ — **two gravitons do bind to $J=2$.**

The fractional binding $E_b/mc^2=\alpha_g^2/36=(m/M_\text{Pl})^4/36$ is minuscule for any
sub-Planckian $m$, so the bound state is genuinely self-bound only at $m\sim M_\text{Pl}$. Since the
constituents are massless gravitons, there is no sub-Planckian constituent scale to appeal to at
all — the only self-consistent scale is set by the relativistic self-gravitating **geon virial**,
$\mu\simeq\sqrt N M_\text{Pl}\xrightarrow{N=2}\sqrt2\,M_\text{Pl}\approx1.73\times10^{19}$ GeV, the
WIMPzilla/Planckian regime. The competing $\nu_R\nu_R$ $J=2$ channel is a **clean, exact-algebraic
no-go**: across the model's entire range of Majorana masses (1 keV to $10^{14}$ GeV), the maximal
fractional binding is $1.3\times10^{-22}$ — no self-bound sub-Planckian $\nu_R\nu_R$ state exists,
because the only inter-particle force available to two Majorana singlets is gravity itself (the
Majorana mass is a one-body self-energy, not a two-body force). **The graviton–graviton channel
carries the whole result.**

Every kinematic dark-matter screen passes at $\mu\simeq\sqrt2M_\text{Pl}$: cold (reduced de Broglie
wavelength $\sim1.7\times10^{-32}$ m $\ll$ kpc), non-fuzzy (49 orders above the fuzzy-DM floor),
$\Delta N_\text{eff}\approx0$, collisionless ($\sigma/m\approx1.7\times10^{-50}\,\text{cm}^2/\text{g}$,
satisfying the same Bullet-Cluster requirement Group A failed). At $\mu\sim M_\text{Pl}$ the object
is, by construction, a **Planck-mass relic** — dynamically indistinguishable from a Planck-mass
black-hole remnant, the connection F228 makes precise.

$$\boxed{\;\text{graviton–graviton }J{=}2\text{ D-wave BINDS (machine-precision, }1.3\times10^{-5}\text{); self-binding forces }\mu\simeq\sqrt2\,M_\text{Pl}\approx1.73\times10^{19}\text{ GeV (virial, order-of-magnitude); }\nu_R\nu_R\to J{=}2\text{ is a clean no-go (}E_b/M_Rc^2\le1.3\times10^{-22}\text{ for every model mass); every DM kinematic screen passes}\;}\tag{R22.9}$$

(F223, checks S1–S6, 6/6 PASS; CL197, `no_go`, `open`. **Named obstruction:** the abundance —
gravitational production under-produces by $\sim10^5$ orders because $\mu\gg H_\text{inf}^\text{max}$
— closed by the next finding into a *mechanism* (production channel and stability), then by F238
into a *proof of non-derivability*.)

#### 22.2.10 F228 — stable as a one-cell Planck-mass remnant; PBH remnants are the sole production channel

F223 left production open: cosmological gravitational particle production (CGPP) is exponentially
suppressed for $\mu\gg H_\text{inf}$, and the geon's virial mass sits $\mu/H_\text{inf}^\text{max}
\approx2.9\times10^5$ above the CMB tensor-bound ceiling $H_\text{inf}^\text{max}\lesssim6\times
10^{13}$ GeV. F228 first gates the candidate on **stability**: the perturbative $J=2$ geon is an
*excited* D-wave state ($n=3,L=2$), not the $1/r$ ground state ($n=1,L=0$), so a light
($m\ll M_\text{Pl}$) perturbative geon radiatively cascades to $J=0$ by graviton emission and is
neither stable as spin-2 nor self-bound there. This forces the stable dark-matter candidate to be
the fully Planckian object, where the level picture is superseded: the object sits at its own
Schwarzschild radius, i.e. it *is* a Planck-mass black hole.

A Planck-mass hole would naively Hawking-evaporate in a Planck time — the potentially fatal channel
— but the F190/F107 lattice horizon-cell structure ($a^2=8\pi\sqrt3\,\ell_P^2$ per cell, Chapter
21's own horizon-entropy machinery) forbids a horizon tiling **fewer than one cell**, fixing an
absolutely stable remnant mass in closed form,
$$M_\text{rem}=\left(\tfrac{\sqrt3}2\right)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}\approx1.14\times10^{19}\ \text{GeV},$$
exact-algebraic (F190 area law + the F107 canonical cell), agreeing with the virial $\mu=\sqrt2M_\text{Pl}$
to within a factor $\approx1.5$ — inside the order-of-magnitude precision of the virial estimate
itself. **A geon and the Planck-mass black-hole remnant are the same tensor-dark object under two
descriptions.**

Every field-theoretic production channel — CGPP (a Bogoliubov integrator validated to
$1.0\times10^{-12}$ against the exactly-solvable Bernard–Duncan case before being applied), UV
freeze-in, graviton coalescence — is exponentially forbidden because assembling a Planck mass from
a sub-Planckian bath in a single interaction is, by the object's own definition, impossible: the
form factor cuts at the Planck scale because the object literally sits at its own Schwarzschild
radius. **Only the evaporation-endpoint route — PBH remnants — survives**, with the abundance set by
$$\Omega_\text{rem}h^2=M_\text{rem}\,\beta\,\tfrac34\,\frac{T_\text{form}}{M_\text{form}}\,\frac{s_0}{\rho_c/h^2},$$
requiring an initial PBH collapse fraction $\beta\approx6.6\times10^{-15}$–$6.6\times10^{-9}$ across
formation masses $M_\text{form}=10^4$–$10^8$ g (all evaporating before BBN, so
$\Delta N_\text{eff}\approx0$ is preserved and the ΛCDM background of F182/F188 is untouched).

$$\boxed{\;\text{a light perturbative geon cascades to }J{=}0\text{, not stable; the Planckian object IS stable as the exact one-cell remnant }M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}\text{ (F190/F107 horizon-cell floor); every field-theoretic channel forbidden by }\mu\gg\text{ every scale; PBH remnants are the SOLE production route, }\beta\propto M_\text{form}^{3/2}\text{, }\beta\sim10^{-15}\text{–}10^{-9}\text{ needed}\;}\tag{R22.10}$$

(F228, checks (9/9) PASS; CL202, `no_go`, `open`. **Named residual:** one external number, $\beta$
— is it derivable? F238 answers no, and pins exactly why.)

#### 22.2.11 F238 — the abundance is provably not derivable: a missing inflaton sector, not a missing calculation

F228 reduced the geon's abundance to one unpinned number, $\beta(M_\text{form})$. $\beta$ is not a
free knob of the geon sector itself — it is the fraction of horizon patches whose primordial
curvature fluctuation exceeds the collapse threshold, governed by Press–Schechter,
$\beta(M)=\tfrac12\,\text{erfc}(\delta_c/\sqrt2\,\sigma(M))$. Inverting the F228 $\beta$-band for the
required small-scale amplitude gives $\sigma(k_\text{PBH})\sim0.06$–$0.08$ — roughly $2\times10^6$
times the measured CMB-scale amplitude $\sqrt{A_s}=4.6\times10^{-5}$.

**The scale-invariant no-go is the acceptance test itself.** The one spectrum shape needing no
extra inflaton knob — exact scale invariance ($n_s=1$) anchored to the observed CMB amplitude —
under-produces the geon relic by $\sim2\times10^{7}$ orders of magnitude
($\beta_\text{HZ}\sim10^{-2.1\times10^7}$). Lifting the small-scale spectrum to the required
amplitude needs a boost $(\sigma_\text{req}/\sqrt{A_s})^2\approx1.6$–$3.0\times10^6$ — a strong blue
tilt or a localized spectral spike, directly contradicting the measured near-scale-invariance
($n_s=0.965<1$) on CMB scales, so the boost would have to be an engineered small-scale departure,
not a global tilt. There is no dynamical attractor to select $\beta$ instead: $\beta(\sigma)$ is
strictly monotone with no interior fixed point, so deriving $\beta$ *requires* deriving $\sigma(k)$,
full stop.

**The structural reason this stays free, not merely unfitted:** a search of the model's own content
finds no inflaton finding, no preheating finding, and no primordial-power-spectrum module — the
model's cosmology (F182/F188) starts at the hot Big Bang and takes the radiation content as given.
This is not a temporary gap awaiting a calculation; Chapter 20's own subsequent results (F282, R20.6)
prove no slow-roll inflaton field can exist on this lattice at all (every compact CA direction has
$M_\text{Pl}^2/f^2\ge\sqrt3$), so the missing sector is not merely unbuilt but, on the standard
route, provably absent. **The geon relic abundance $\Omega_\text{DM}h^2=0.12$ is a free cosmological
initial condition, not a derivable particle-physics coupling — for a stated, specific, checkable
reason, not an unexamined placeholder.**

$$\boxed{\;\beta\text{ traces to a required small-scale amplitude}\sigma\sim0.06\text{–}0.08\approx2\times10^6\times\text{the measured CMB amplitude; the tuning-free (scale-invariant) spectrum under-produces by}\sim2\times10^7\text{ orders; }\beta(\sigma)\text{ has no attractor; the model has (and, per F282, CAN have) no inflaton/primordial-spectrum sector}\Rightarrow\text{abundance is a free cosmological initial condition, structurally, not an unfitted number}\;}\tag{R22.11}$$

(F238, checks S1–S6, 7/7 PASS; CL209, `no_go`, `open`, `quantitative`. This is the chapter's second
central honesty result, the geon-side mirror of F237's sterile-neutrino exclusion: the *identity*
question is answered completely; the *abundance* question is answered with a proof of
non-derivability, which is itself the strongest available form of honest closure.)

#### 22.2.12 F365 — two 2025 gravitational-wave results bound, without fixing, the free abundance input

F365 checks the F228/F238 geon scenario against two 2025 papers not previously compared to this
thread. First, $M_\text{rem}\approx2\times10^{-5}$ g sits roughly 22 orders below the "asteroid mass
window" that current PBH-dark-matter reviews treat as the presently unconstrained compact-object
range — as a *fixed relic mass* with purely gravitational coupling and an astronomically large
number density ($n\approx1.7\times10^{-20}\,\text{cm}^{-3}$, one particle per $(40\,\text{km})^3$),
it is not reachable by any existing microlensing, dynamical, or evaporation-gamma-ray mass-window
plot — those bound the *progenitor* PBH mass function, not the fixed relic mass. The falsifiable
structure instead comes from constraints on **how** the relic forms.

Cross-checking F228's own $\beta(M_\text{form})$ formula against an independently-built external
formula sharing the identical $M_\text{form}^{3/2}$ scaling (Cheek, Ghoshal & Heurtier,
arXiv:2506.16154) finds a constant ratio of $11.7\times$ across all three worked masses — the
expected level of agreement for two independently-normalized order-of-magnitude estimates of the
same mechanism, not by itself strong confirmation (both share the scaling by construction).
Combining the same paper's own gravitational-wave bound on PBH-binary mergers before evaporation
(the DLS bound) with the abundance-matching requirement, a hand-rolled bisection locates a **formation-mass ceiling**,
$$M_\text{form}\lesssim1.6\times10^8\ \text{g}\quad(\text{order-of-magnitude, contingent on the source paper's own stated monochromatic-mass-function assumption}),$$
under which F228's own third worked example ($10^8$ g) sits only $2.9\times$ below the ceiling —
marginal rather than safely interior, sharpening (not overturning) F228's illustrative table. A
second, weaker check compares the model's own required small-scale amplitude $\sigma_\text{req}$
against a 2025 LIGO result excluding *Gaussian*-statistics Planck relics: after a review-pass
correction (the original draft overstated this leg — see below), the model's required amplitude is
found to sit at or near the edge of, rather than cleanly inside, the LIGO-excluded band, depending
on which of that paper's own two internally-stated $\sigma\leftrightarrow P_\mathcal R$ conventions
is used — a same-order-of-magnitude plausibility placement, not a quantitative hit.

$$\boxed{\;M_\text{rem}\text{ sits}\sim22\text{ orders below every current compact-object mass-window plot (detection structurally hopeless); a 2025 GW early-merger bound gives an order-of-magnitude formation-mass ceiling }M_\text{form}\lesssim1.6\times10^8\text{ g (F228's own }10^8\text{ g example now marginal); a weaker, convention-sensitive non-Gaussianity plausibility argument places the required spectrum near, not cleanly inside, a 2025 LIGO Gaussian-exclusion band}\;}\tag{R22.12}$$

(F365, checks S1–S6, 6/6 PASS; CL301, `prediction`, `open`, `bracketed`. Reviewed and corrected at
the review-finding attack pass, 2026-09-04: the original non-Gaussianity claim was found overstated
and rewritten to the weaker, honestly-scoped form given here — recorded so the correction is not
silently lost. **Net effect on K7:** grade unchanged at PARTIAL; the free input is now bounded along
two named axes of unequal strength rather than left undifferentiated.)

#### 22.2.13 F366 — a structurally distinct production channel is open in principle, not derived

F238's non-derivability argument is a five-link causal chain specific to the **inflaton/
Press–Schechter route**: $\Omega_\text{DM}\leftarrow\beta(M_\text{form})\leftarrow\sigma(k_\text{PBH})
\leftarrow$ primordial curvature spectrum $\leftarrow$ inflaton potential (absent). F366 checks
whether the subsequent hardenings of that route (F282's proof no slow-roll inflaton can exist at
all; F285's proof no measure fixes the observed tilt) close the abundance question generally, or
only along this one channel — and finds only the latter. A structurally distinct,
**non-inflationary** production channel exists inside the model's own already-derived content: the
Chapter 15 $E_g$ lepton-condensate clock potential $V(\delta)=\lambda_6e_\text{sat}^6\cos^23\delta$
(F150/F175/F234, unmodified, no new constant introduced) possesses an **exact discrete $\mathbb Z_6$
symmetry** — $\cos6\delta=-1$ has exactly six solutions, evenly spaced, and $V(\delta+\pi/3)\equiv
V(\delta)$ identically for every $\delta$, checked symbolically by two independent simplification
paths. Six exactly-degenerate discrete vacua under an exact discrete symmetry is precisely the
textbook Kibble-mechanism precondition for a domain-wall network: if $\delta$ settles into one of
the six wells independently in causally-disconnected patches, a $\mathbb Z_6$ wall network forms,
and domain-wall collapse is an established (if here unbuilt-on-this-lattice) PBH-formation
mechanism in the literature.

Chapter 20's own inflaton no-go (F282 §6) excludes one adjacent mechanism — "causal seeds" generating
the CMB's own large-scale power spectrum — on the specific historical grounds that sub-horizon,
incoherent sources cannot reproduce the observed coherent acoustic-peak structure. This does *not*
reach domain-wall-collapse PBH formation, which is never asked to explain the CMB: it operates
entirely at the wall network's own formation scale (the F228 $M_\text{form}\sim10^4$–$10^8$ g
range, some 20+ orders of magnitude in energy above anything the CMB probes), leaving the
Chapter 20/21 $\Lambda$CDM sector untouched. Separately, F285's own generic-measure argument (that a
locally-correlated lattice field has no reason to agree with itself across super-horizon distances,
originally applied to the density field) applies with identical force to the condensate angle
$\delta$ once F282/F285 have already closed off the mechanisms (inflation, causal super-horizon
coherence) that would otherwise correlate it — suggestive that the precondition is not merely
*available* but *expected to activate*, though this is an argument, not a computation.

**Nothing here promotes the grade.** Turning this into a derived $\beta(M_\text{form})$ needs four
separate, unresolved pieces: a causally-early dynamics showing $\delta$ actually settles into a
well via a horizon-limited process; confirmation the settling is a genuine phase transition (no
finite-temperature $E_g$ potential exists in the model yet); the wall tension in physical units
(blocked on the same open canonical-kinetic-term question F282's own 2026-09-04 update, F363,
flags); and a network-collapse-fraction computation together with a resolution of the generic
domain-wall-overclosure problem (either an explicit vacuum-degeneracy-breaking bias, itself new
physics requiring its own derivation, or a demonstration the walls collapse to PBHs before ever
reaching the overclosing scaling regime).

$$\boxed{\;\text{F238's non-derivability is provably SCOPED to the inflaton/Press–Schechter route; a structurally distinct }\mathbb Z_6\text{ domain-wall-collapse channel, sourced by the model's own already-derived }E_g\text{ clock potential, is not excluded by F238/F282/F283/F284/F285; its Kibble-mechanism precondition (exact discrete}\mathbb Z_6\text{ symmetry, 6 degenerate vacua) is confirmed exact-algebraically at zero new-physics cost; four further pieces, none small, remain unbuilt — no abundance is computed}\;}\tag{R22.13}$$

(F366, checks C1–C4, 4/4 PASS; CL302, `non_claim`, `open`, rolls up to CL209. **K8 grade unchanged
(EXCLUDED for the inflaton route, correctly)** — this finding narrows the *characterization* of the
free input from "no route can ever derive this" to "the standard route is provably and permanently
closed; a structurally distinct route is open in principle, with a real but unfinished precondition.")

### Group E — The falsifiability battery

#### 22.2.14 F203 — six quantified, currently-evaluable tests, read against what postdates it

F203 turns the dark sector's qualitative claims into six dated, sourced, quantified tests
(status vocabulary: `consistent`, `under_pressure`, `falsified`), as of 2026-06-30. At the time of
writing: **T1** (keV-sterile X-ray line) and **T2** (Lyman-$\alpha$ warm-DM cutoff) were both
`under_pressure` — the predicted radiative rate sat $1.9$ dex below the then-current XRISM 3σ limit,
but the combined X-ray+Lyman-$\alpha$ 100%-DM floor ($\sim41$ keV) already sat above the model's
5.6–7.1 keV. **T3** (strict $w=-1$ dark energy) was `under_pressure` against DESI DR2's
$2.8$–$4.2\sigma$ rejection of the cosmological constant (Chapter 21's own territory, unresolved
there too — R21.5's $\Omega_\Lambda\equiv1-\Omega_m$ residual). **T4** (Bullet-Cluster lensing on
the collisionless component) and **T5** (relic is a keV sterile, not a GeV–TeV WIMP or QCD axion)
were `consistent`. **T6** ($a_0=cH_0/6$, a diagnostic coincidence with the emergent-gravity route's
own acceleration scale) was `consistent` but explicitly flagged as a shared-scale hint surviving
the route's own falsification (F194), not a mechanism.

**Read against this chapter's own later results, three of the six need an explicit update, though
none needs a re-run of F203 itself:**

- **T1/T2** are sharpened from order-of-magnitude to computed by F205 (§22.2.6, 2.55 dex X-ray
  exclusion for non-resonant production; 9–15 keV coldest-resonant Lyman-$\alpha$ floor), and then
  **closed, not merely narrowed**, by F237 (§22.2.7): the keV sterile is mechanism-level excluded
  as 100% dark matter. F203's `under_pressure` classification for T1/T2 was correct as written and
  is superseded in substance (not formally, per `supersessions.yaml` — no record names F203) by
  this sharper verdict. The falsifier F203 itself named for T1 ("a confirmed line pinning $m_s$
  outside the texture's reach") is subsumed by F237's cleaner, mechanism-level exclusion.
- **T5** ("relic is a keV sterile — not a WIMP/axion") is the test whose *framing*, not its
  content, is now stale: F237/F228 redirect the model's 100%-dark-matter identity to the geon, a
  Planck-mass object that is neither a keV sterile, a GeV–TeV WIMP, nor a QCD axion. T5's own
  `consistent (soft)` verdict against WIMP/axion direct-detection nulls still holds for the
  *surviving* candidates (the geon is undetectable by direct/indirect searches by construction;
  the demoted sterile remains a real sub-dominant relic, T5's original subject), but a reader citing
  T5 today should read it as "not falsified by WIMP/axion nulls," not as "the identity is settled to
  be the keV sterile" — the identity is the geon, per §22.2.7/§22.2.10. This staleness is not
  captured in F203's own text or in its claim card (CL177, still `review_state: unreviewed-seed`,
  §22.7 gap).
- **T4** is reinforced, not merely left standing, by F358's 2026 literature re-examination
  (§22.2.2): the Bullet-Cluster dark-source requirement is now independently corroborated by an
  outside 2026 MOND/QUMOND dispute reaching the same conclusion by a different route.

$$\boxed{\;\text{six tests as of 2026-06-30: 0 falsified, 3 under\_pressure (T1, T2, T3), 3 consistent (T4, T5, T6); T1/T2 subsequently CLOSED (not merely sharpened) by F205}\to\text{F237 into a clean exclusion of the keV sterile as 100\% DM; T5's identity framing is stale — the surviving 100\%-DM identity is the geon, not the sterile; T4 independently reinforced by F358; T3 unresolved, inherited from Chapter 21}\;}\tag{R22.14}$$

(F203, checks T1–T7, 7/7 PASS; CL177, `no_go`, `open`, `review_state: unreviewed-seed`. This
chapter's capstone: the battery's own honest three-way split — not falsified, but genuinely under
pressure in places — is exactly the state the sharper Group C/D findings leave the model in today,
with the identity question resolved and the abundance question honestly open for both surviving
candidates.)

## 22.3 Results table

| # | Result | Status | Exactness | Finding(s) |
|---|---|---|---|---|
| R22.1 | Rotation curves cannot discriminate dark halo vs. modified gravity; Bullet Cluster breaks the degeneracy, requiring a dark source | genuine derivation (toy, illustrative) | quantitative (toy) | F191; `test-results/F191_darkmatter.json` (3/3) |
| R22.2 | **No-go:** model-native emergent gravity FALSIFIED by the Bullet Cluster. **F194/F358 partial supersession (S23):** the "regardless of clump shape" sentence is WITHDRAWN; the dark-source-required conclusion is RETAINED IN FULL and independently reinforced | no-go, conclusion retained; one sub-claim withdrawn | quantitative (E1–E3) / toy-robust (E4–E5); F358 literature-only | F194 (5/5); F358 (analysis-only); CL168 |
| R22.3 | **No-go framework:** clustering DM requires a gapped branch; the $E_g$ condensate qualifies kinematically (VEV$\to$DE, gapped modes$\to$DM); F69 photon channel excluded (gapless) | genuine derivation (kinematic, exact) + toy demonstration | exact (EoS split) / illustrative (toy profile) | F197 (5/5); CL170 |
| R22.4 | **No-go (leg 1):** light angular mode under-produces $\Omega_\text{DM}$ by $\sim15$ orders (misalignment); heavy amplitude mode reaches the WIMP window via freeze-out | computed negative + computed positive candidate (superseded by R22.5) | standard scaling (exact) / order-of-magnitude (scale numbers) | F198 (5/5); CL171 |
| R22.5 | **No-go (leg 2, closes Group B):** amplitude mode decays in $\sim10^{-21}$ s (38–40 orders below cosmological) via its own defining lepton coupling; stability fails before abundance is reached; no conserved charge protects it | no-go, robust (dwarfs all input uncertainty) | standard Yukawa-scalar width (exact form) / representative masses | F199b (5/5); CL173 |
| R22.6 | Sterile-neutrino Boltzmann computation: non-resonant DW excluded by 2.55 dex; resonant reaches $\Omega_\text{DM}$ only for a warm spectrum at X-ray-allowed mixing; Lyman-$\alpha$ floor 9–41 keV $>$ model's 5.6–7.1 keV | quantified pressure, not yet decisive | quantitative (converged QKE quadrature) | F205 (8/8); CL179 |
| R22.7 | **Decisive: keV sterile EXCLUDED as 100% DM** (opposite-sign entropy-dilution scaling, mechanism-level); survives as a bounded sub-dominant relic; hands off 100%-DM identity to the geon | no-go for 100% DM; live for sub-dominant role | computed (exact rational exponents; 154-point grid) | F237 (7/7); CL208 |
| R22.8 | **No-go:** metric graviton exactly massless, no propagating second branch; a massive spin-2 must be a gauge-neutral bound state; kinematically a viable collisionless CDM candidate | no-go (native mode) + constructive corollary | exact (transversality, RG irrelevance) | F216 (7/7); CL190 |
| R22.9 | Graviton–graviton $J{=}2$ geon BINDS at $\mu\simeq\sqrt2\,M_\text{Pl}$; $\nu_R\nu_R\to J{=}2$ is a clean no-go | positive (binding) + no-go ($\nu_R\nu_R$) | machine-precision (binding, $1.3\times10^{-5}$) / order-of-magnitude (virial mass) / exact-algebraic ($\nu_R\nu_R$ no-go) | F223 (6/6); CL197 |
| R22.10 | Geon stable as the exact one-cell Planck-mass remnant $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$; PBH remnants are the sole viable production channel; every field-theoretic channel forbidden | positive identity/stability + mechanism no-go (all but one channel) | exact-algebraic ($M_\text{rem}$); machine-precision-validated (CGPP Bogoliubov); order-of-magnitude ($\beta$-band) | F228 (9/9); CL202 |
| R22.11 | **The chapter's second central honesty result:** geon abundance $\Omega_\text{DM}h^2=0.12$ is provably NOT DERIVABLE — traces to a required $\sim2\times10^6\times$ CMB-amplitude primordial spectral feature the model has no (and per F282, cannot have any) sector to produce | proven non-derivability (structural, not a placeholder) | derived bridge (Press–Schechter) / computed inversion / structural absence | F238 (7/7); CL209 |
| R22.12 | 2025 GW literature bounds the free input without fixing it: $M_\text{rem}$ untouched by any current mass-window plot; formation-mass ceiling $M_\text{form}\lesssim1.6\times10^8$ g (order-of-magnitude); weaker non-Gaussianity plausibility placement (corrected at review) | live prediction, bracketed | quantitative (formation-mass ceiling) / bracketed (non-Gaussianity leg) | F365 (6/6); CL301 |
| R22.13 | A structurally distinct, non-inflationary ($\mathbb Z_6$ domain-wall-collapse) production channel is not excluded; its Kibble-mechanism precondition is confirmed exact-algebraically; full derivation (4 pieces) untouched | reopening, scoped and partial — not a derivation | exact-algebraic (precondition) / structural (scope argument) / open (abundance) | F366 (4/4); CL302 |
| R22.14 | Falsifiability battery: 0/6 falsified as written; T1/T2 subsequently closed (not merely sharpened) by F205→F237; T5's identity framing is stale (geon, not sterile, is the surviving 100%-DM candidate); T4 independently reinforced; T3 (dark energy) unresolved | battery built; three of six results updated by later findings in this chapter | exact (margins as computed); status classifications robust | F203 (7/7); CL177 |

## 22.4 Comparison with measurement

- **Bullet Cluster (1E 0657−56, Clowe et al. 2006, $8\sigma$).** The single most decisive
  observational discriminator in this chapter. It excludes the model-native emergent-gravity route
  outright (R22.2) and is satisfied automatically, by construction, by both the sterile-neutrino and
  geon candidates (collisionless, gravitationally-coupled-only). F358's 2026 re-examination
  (arXiv:2601.22245, JWST-refined) *sharpens* the empirical offset measurement to $4^{+3}_{-2}$ kpc
  (BCG-to-halo centroid), roughly a threefold tightening over pre-JWST analyses — if anything
  strengthening, not weakening, the discriminator this chapter relies on throughout.
- **X-ray + Lyman-$\alpha$ bounds on the sterile neutrino.** F205's computed floor (9–41 keV
  depending on production channel) sits strictly above the model's 5.6–7.1 keV texture-preferred
  mass; F237's entropy-dilution scan closes the gap with zero surviving points at either benchmark
  mass, across a 154-point $(L,S)$ grid. The keV sterile is quantitatively, not merely
  qualitatively, excluded as 100% dark matter — reported precisely, not softened.
- **Gravitational-wave bounds on the geon.** No existing GW or compact-object mass-window
  measurement reaches the fixed relic mass $M_\text{rem}\approx2\times10^{-5}$ g directly (F365):
  detection is structurally hopeless (purely gravitational coupling, astronomically large number
  density). The two GW constraints that *do* apply act on the **production** side: an early-merger
  GW bound gives an order-of-magnitude formation-mass ceiling $M_\text{form}\lesssim1.6\times10^8$
  g, and a LIGO O3 Gaussian-Planck-relic exclusion places the model's own required primordial
  amplitude at or near (not decisively inside) an excluded band, depending on convention. Neither
  measurement fixes the abundance; both narrow, without closing, the space in which the free input
  $\beta(M_\text{form})$ must live.
- **DESI DR2 vs. $w=-1$.** Chapter 21's own unresolved tension (R21.5, T3 here) — the model's dark
  energy is a homogeneous holographic-vacuum residual predicting exactly $w=-1$; DESI DR2 prefers
  dynamical dark energy at $2.8$–$4.2\sigma$, dataset-dependent and below the conventional $5\sigma$
  discovery threshold. Left open, as in Chapter 21.
- **$S_8$/$\sigma_8$ structure-growth tension (Chapter 20, F288, R20.13) and dark-matter identity.**
  F288's own B2 result — cited here because it directly bears on this chapter's two candidates — is
  that $\sigma_8$ is **blind to the choice between the two candidates at the $10^{-6}$ level**: a
  5.6 keV sterile suppresses $\sigma_8$ by only $2.7\times10^{-6}$ relative to a pure Planck-mass
  geon, roughly $2.6$ decades below the $\sigma_8$ scale's own half-mode wavenumber. The observable
  that *is* sensitive is the Lyman-$\alpha$ forest ($k\sim1$–$20\,h\,\text{Mpc}^{-1}$) — exactly
  where F203/F205's 9–15 keV floor already places the sterile under pressure. This is a genuine
  cross-chapter handoff: the growth-of-structure sector cannot settle which candidate dominates; the
  keV-sterile production calculation in this chapter is the probe that does the discriminating work.

## 22.5 What was excluded, and why

**Group A — the pure gravity-only route (modified/emergent gravity as "dark matter without dark
matter").** Excluded in full by the Bullet Cluster (F194, R22.2): because any local, baryon-sourced
modified-gravity phantom-density functional tracks the baryon distribution, and the dominant baryon
component in a cluster merger (the X-ray gas) is spatially separated from the collisionless
component (the galaxies) whose lensing signature is actually observed, no such theory can put the
lensing peak on the galaxies. This is a *structural* failure of the entire class, not a parameter
tuning failure — the appealing $a_0$–$\rho_\Lambda$ coincidence (F194 E1, ratio $0.97$) is not
wasted, but it must enter physics as a shared scale for a genuine dark *source* (the geon's own
$a_0$-adjacent connections are not derived in this chapter), not as an IR-running of $G$. The one
overstated argument inside this exclusion — that the discriminator holds "regardless of clump
shape" — is withdrawn by F358 per S23, without touching the exclusion itself; §22.2.2 gives the
precise scope, directly from the supersession record's own `retained:`/`dead:` fields, and this
should not be conflated with a general softening of the Bullet-Cluster argument.

**Group B — the $E_g$ lepton-condensate route to a unified dark sector.** Excluded on two
independent legs, neither rescuable by retuning the condensate's own free parameters, because both
obstructions are set by the same scales that make the condensate the lepton-mass mechanism in the
first place. The light angular mode's natural decay constant ($f\simeq v/2=123$ GeV, the Chapter
12/15 electroweak Stueckelberg scale) is fifteen orders of magnitude below what a vacuum-misalignment
relic at any reasonable mass needs (F198, R22.4) — raising $f$ would require decoupling the mode
from the electroweak scale that gives it a mass in the first place, which is not a parameter
adjustment but a different physical object. The heavy amplitude mode's defining coupling to leptons
($g_\ell=m_\ell/f$, Chapter 15's F93 O1 crystal-field mechanism) is exactly what makes it decay in
$\sim10^{-21}$ s (F199b, R22.5) — removing that coupling would mean it is no longer the object that
sets lepton masses. This is the honest shape of a *closed* negative result: the condensate is
excellent, derived, load-bearing physics for the lepton sector (Chapter 15), and precisely the
features that make it so are the features that forbid it from also being dark matter.

**The keV sterile neutrino as 100% dark matter.** Excluded at the mechanism level by F237 (R22.7):
the two available production levers (resonant mixing angle, entropy dilution) move the X-ray and
Lyman-$\alpha$ constraints in opposite directions through the required mixing angle, with exact
opposite-sign scaling exponents ($+1$ vs. $-4/9$ in $\log S$). This is not a parameter-space gap
that a cleverer production history might close; the signs themselves forbid any solution. The
sterile neutrino is *not* excluded as a physical object — F201/F266 (Chapter 16) still stand, and
the particle is real, stable, and produced — only its claim to be the *entirety* of dark matter is
closed.

## 22.6 What is still open

**The abundance-freedom of both surviving dark-matter candidates is this section's central
content, and it is the single largest open item this chapter carries.** For the sterile neutrino
(now understood as a sub-dominant relic, F237), the precise surviving fraction $f<1$ requires a
full lepton-number-depletion quantum-kinetic code that neither F205 nor F237 builds — bounded, but
not computed. For the geon (the model's only surviving 100%-dark-matter candidate), F238 proves the
standard route cannot fix the abundance because the model has no primordial-spectrum sector, and
F282 (Chapter 20) proves no slow-roll inflaton can supply one on this lattice; F365 narrows the
allowed formation-mass window without deriving a value inside it; F366 opens a structurally distinct
non-inflationary channel (domain-wall collapse) whose one cheaply-checkable precondition (the exact
$\mathbb Z_6$ degeneracy of the already-derived $E_g$ clock potential) is satisfied, but whose full
derivation needs four separate, unbuilt pieces — a causally-early settling dynamics, confirmation of
a genuine phase transition, the wall tension in physical units (itself blocked on the open canonical-
kinetic-term question F282/F363 flag), and a network-collapse-fraction computation together with a
resolution of the generic domain-wall-overclosure problem. **None of this is a gap in calculation
technique; each item is a separate, honestly-named piece of physics the model does not yet have.**

This closes part, but only part, of Chapter 21's own open problem: R21.5 found $\Omega_\Lambda$'s
residual is identically $1-\Omega_m$, "blocked by this model's own open dark-sector abundance." This
chapter answers *which* sector supplies $\Omega_m$'s dark component (the geon, primarily, with the
sterile neutrino as a bounded minority contributor) but does not supply the missing $\Omega_m$
*number itself* — the abundance freedom identified here is exactly the freedom Chapter 21 was
blocked by, restated with a name and a mechanism rather than removed.

> **Gap [G-15]:** `docs/claims/CL177-the-dark-sector-falsifiability-battery-the-six-observational.md`
> (F203's claim card) still carries `review_state: unreviewed-seed` and `falsifier: unset`, mechanically
> extracted from F203's own title/status line at the 2026-08-04 claims-layer seeding pass and never
> independently reviewed since. Reading the card's own body confirms it: "This card's only evidence
> is the prose of its own finding... may not be cited as independent support." Substantively, the
> card's implicit T1/T2/T5 framing is now stale in the specific way §22.2.14 describes — T1/T2 have
> moved from `under_pressure` to a computed, mechanism-level exclusion (F205→F237), and T5's
> "relic is a keV sterile" identity framing no longer names the model's surviving 100%-dark-matter
> candidate (the geon does, per F237/F228). This is not a claims-layer *bookkeeping* artifact of the
> kind Chapters 8/12/19/17 found (a mechanical mis-transcription of a finding's own header) — F203's
> header is accurately reflected by CL177; the card is simply un-updated against three *later*
> findings that were never folded back into it, the same species of staleness Chapter 13b's own
> Gap [G-11] found for CL022/CL252 against F337/F340/F350. Not fixed here (documentation-only);
> flagged for whoever next promotes CL177 out of `unreviewed-seed` to state explicitly, in the
> card's own text, that T1/T2's `under_pressure` verdict has been superseded in substance by F237's
> clean exclusion and that T5 should be read as bearing on the sterile neutrino's *surviving
> sub-dominant role*, not the sector's *primary* identity.

## 22.7 Falsifiers

Consolidating F203's six-test battery (§22.2.14) with the sharper results this chapter derives, as
the chapter's synthesizing close:

1. **T1 (X-ray line).** A keV sterile at $m_s=5.6$–$7.1$ keV predicts a monochromatic line at
   $E_\gamma=m_s/2$. **Status: superseded by a mechanism-level exclusion (F237)** — the sterile
   cannot be 100% of dark matter through resonant or diluted production; a future sub-critical X-ray
   line at $m_s/2$ would *confirm* the surviving sub-dominant role rather than test the exclusion.
2. **T2 (Lyman-$\alpha$ warm-DM cutoff).** Same status: closed for the 100%-DM hypothesis by F237's
   opposite-sign scaling argument; a fractional-WDM Lyman-$\alpha$ fit for the bounded sub-dominant
   fraction is the concrete open item (§22.6).
3. **T3 (strict $w=-1$).** Unresolved, inherited from Chapter 21. Falsifier as stated there and in
   F203: a robust, dataset-independent $w\neq-1$ at $\ge5\sigma$ would falsify the pure-VEV dark-
   energy identity and, by R21.5's identity $\Omega_\Lambda\equiv1-\Omega_m$, would directly affect
   how this chapter's dark-matter abundance is read.
4. **T4 (Bullet-Cluster lensing on the collisionless component).** Consistent, and reinforced (F358):
   a future merger with lensing demonstrably on the gas would revive the modified-gravity route this
   chapter excludes; none is known.
5. **T5 (identity), restated.** The model's dark-matter identity is now the geon (primary) plus a
   bounded sterile-neutrino minority (secondary), not the sterile neutrino alone as F203 originally
   framed it (§22.2.14, Gap [G-15]). Falsifier: a confirmed GeV–TeV WIMP or QCD axion carrying the
   *full* relic abundance would still falsify both model candidates; a confirmed keV X-ray line at
   *super-critical* flux (inconsistent with the sub-dominant bound) would falsify the sterile
   neutrino's surviving role specifically.
6. **T6 ($a_0=cH_0/6$).** Diagnostic, not decisive (its underlying mechanism, emergent gravity, is
   independently falsified, R22.2) — retained only as an unexplained shared-scale coincidence.
7. **The geon's own falsifiers (new to this chapter, from F238/F365/F366).** (a) A future refinement
   of early-merger gravitational-wave bounds pushing the formation-mass ceiling (§22.2.12) below the
   minimum mass consistent with $M_\text{rem}$ itself would close the PBH-remnant route entirely,
   forcing a genuinely new production mechanism. (b) If a future model-native primordial-spectrum
   sector is ever built (contrary to F282's own no-go for the standard inflaton route — meaning this
   would have to be the F366 domain-wall channel or something not yet conceived) and is shown to
   produce *Gaussian* statistics at the PBH-formation scale, the LIGO O3 bound becomes a live,
   directly computable tension rather than the order-of-magnitude placement given here. (c) For the
   F366 domain-wall channel specifically: a demonstration that the wall network cannot avoid the
   generic domain-wall overclosure problem for any physically reasonable wall tension would close
   that channel on dynamical grounds even though its Kibble-mechanism precondition holds exactly;
   conversely, a full derivation of $\beta(M_\text{form})$ through that channel landing in the F228
   band would be the first derived geon abundance in the model.

**The chapter's own bottom line, stated once more.** Two structurally-motivated dark-matter
candidates; the identity question is closed for both (the sterile neutrino is real but sub-dominant,
the geon is the model's surviving 100%-dark-matter candidate); the abundance question is open for
both, for two different, precisely-named reasons (an unbuilt lepton-asymmetry/dilution history for
the sterile neutrino; a provably-absent primordial-spectrum sector for the geon, with one
structurally distinct alternative channel opened but not derived). No number in this chapter is
presented as more settled than that.

---

## Notation established in this chapter

*Harvested into the whole-monograph glossary at Appendix A5. Extends Chapters 1, 15, 16, 18, 19, 20
and 21's notation; nothing here is redefined.*

| Symbol | Meaning | First used / fixed here |
|---|---|---|
| $a_0$ | The MOND/emergent-gravity critical acceleration scale, $a_0=cH_0/6$ in the model's own construction; the route it belongs to is falsified (R22.2), retained only as an unexplained coincidence (T6). | §22.2.2 (F194) |
| $\rho_\text{dyn}$ | The QUMOND/emergent-gravity phantom density, a local functional of the baryon distribution; the object whose baryon-tracking property drives the Bullet-Cluster falsification. | §22.2.2 (F194) |
| $\delta$ | The $E_g$ second-shell condensate's clock/phase angle (Chapter 15); its potential $V(\delta)=\lambda_6e_\text{sat}^6\cos^23\delta$ is reused unmodified in both Group B (the angular dark-matter mode) and Group D (the F366 domain-wall precondition). | §22.2.3 (F197), §22.2.13 (F366) |
| $L$ | The lepton asymmetry driving resonant (Shi–Fuller) sterile-neutrino production. | §22.2.6 (F205) |
| $S$ | The post-production entropy-dilution factor from late $N_{2,3}$ decay, $S\equiv s_\text{after}/s_\text{before}\ge1$. | §22.2.7 (F237) |
| $\mu$ | The graviton–graviton geon's virial (bound-state) mass, $\mu\simeq\sqrt2\,M_\text{Pl}$. | §22.2.9 (F223) |
| $\alpha_g$ | The gravitational "fine structure constant" between two quanta of mass $m$, $\alpha_g=(m/M_\text{Pl})^2=Gm^2/\hbar c$. | §22.2.9 (F223) |
| $M_\text{rem}$ | The exact one-cell Planck-mass black-hole remnant mass, $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}\approx0.9306\,M_\text{Pl}$ — the geon's stable identity. | §22.2.10 (F228) |
| $\beta(M_\text{form})$ | The primordial-black-hole collapse fraction at formation mass $M_\text{form}$; the geon's sole free abundance input. | §22.2.10 (F228) |
| $\sigma(k)$ | The primordial curvature-perturbation RMS amplitude at comoving scale $k$; the quantity $\beta$ traces to, and which the model has no sector to fix (F238). | §22.2.11 (F238) |
