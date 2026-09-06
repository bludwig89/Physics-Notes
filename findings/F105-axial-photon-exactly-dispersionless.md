# F105 — Axis-aligned photons are exactly dispersionless: Ω_pair(k x̂) = |k|/√3 at all k

`2026-06-06 - 17:25`

**Status:** Confirmed (algebraic identity + machine-precision numerical check). Minor corollary, fell out of building the `photon_beam_all_fields` scenario.
**Test record:** record `F314-pair-group-velocity-closed-form` (tier gate) — `casim.engine.gauge.photon_packet`, entry `check_pair_group_velocity_closed_form`: its on-axis legs assert the pair velocity is exactly c_lat and the on-axis **curvature is zero**, i.e. this finding's identity, at gate tier. It already named F105 on its side of the join. `F129-blockspin-free-photon` and `F227-decoherence-floor` also name F105. Declared 2026-08-19.

**Cross-references:** [[F69-paired-spinor-photon]] (the pair law), [[F26-speed-of-light-as-rotation-rate]], [[F28-grb-dispersion-test]], [[F30-photon-dispersion-order-anisotropy-birefringence]].

## Statement

Along any cubic lattice axis the paired-photon rotation rate is exactly linear at **all** wavenumbers, not just in the k→0 limit:

$$\Omega_\text{pair}(k\,\hat{x}) = \omega^+(k/2) + \omega^-(k/2) = \frac{|k|}{\sqrt{3}}, \qquad 0 \le \frac{|k|}{\sqrt 3} \le \pi.$$

## Derivation (one line)

The BCC dispersion (Paper 1 Eq. 15) is $\omega^\pm = \arccos(c_x c_y c_z \pm s_x s_y s_z)$ with $c_i=\cos(k_i/\sqrt3)$, $s_i=\sin(k_i/\sqrt3)$. On an axis, $k_y=k_z=0 \Rightarrow c_y=c_z=1,\ s_y=s_z=0$, so

$$\omega^\pm(k\,\hat x) = \arccos(\cos(k/\sqrt3)) = |k|/\sqrt3$$

exactly — the ± branch term vanishes identically. Hence $\Omega_\text{pair} = 2\cdot(k/2)/\sqrt3 = |k|/\sqrt3$. Exact algebraic; numerically $\Omega_\text{pair}\sqrt3/k - 1 \le 3\times10^{-15}$ over $k \in [0.1, 1.2]$.

## Consequences

1. **No vacuum dispersion for axis-aligned propagation at any energy.** A photon travelling along a lattice axis has group velocity exactly $1/\sqrt3$ at every $k$ up to the zone edge — energy-dependent arrival-time delays (the GRB observable of F28) are *identically zero* on-axis. Lattice dispersion and anisotropy live entirely in the off-axis directions (the body diagonal is the familiar leading-order case).
2. **Beam optics on the lattice are purely diffractive on-axis.** A collimated beam's speed deficit comes only from its transverse angular spectrum, $\Delta v/v \approx 1/(2(k_0\sigma_\perp)^2)$ — verified in `photon_beam_all_fields` (predicted 2.3%, measured 2.5% at $k_0\sigma_\perp = 4.7$; the longitudinal packet does not spread).
3. Any future search for lattice-induced photon dispersion in this model should therefore be framed as a *directional* (anisotropy) search, not an on-axis energy-dependence search.

## Artifacts

- `ca-simulation/ca_photon_pair.py` — `build_beam_packet` (travelling one-sided F = E + iB packet), `group_velocity_at`
- `scenarios/photon_beam_all_fields.yaml`, `scenarios/bcc_fields_companion.yaml`
- `test-results/smoke_photon_beam_all_fields.json` (beam_track summary)
